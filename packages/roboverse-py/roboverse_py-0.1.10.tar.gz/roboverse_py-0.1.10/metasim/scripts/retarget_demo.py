from __future__ import annotations

#########################################
### Add command line arguments
#########################################
from dataclasses import dataclass

import tyro


@dataclass
class Args:
    source_robot: str
    target_robots: list[str]
    tasks: list[str] | None = None
    source_path: str | None = None
    target_path: str | None = None
    device: str = "cuda:0"
    ignore_ground_collision: bool = False
    viz: bool = False

    def __post_init__(self):
        assert self.tasks is not None or (self.source_path is not None and self.target_path is not None), (
            "Either tasks, or both source_path and target_path must be provided"
        )


args = tyro.cli(Args)


#########################################
### Normal code
#########################################
import os
from copy import deepcopy

import numpy as np
import rootutils
import torch
from curobo.types.math import Pose
from loguru import logger as log
from pytorch3d import transforms
from rich.logging import RichHandler
from tqdm import tqdm, trange

rootutils.setup_root(__file__, pythonpath=True)
log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])

from glob import glob

from metasim.utils.demo_util.loader import load_traj_file, save_traj_file
from metasim.utils.kinematics_utils import (
    ee_pose_from_tcp_pose,
    get_curobo_models,
    tcp_pose_from_ee_pose,
)
from metasim.utils.setup_util import get_robot, get_task

NUM_SEED = 20


def single(source_path, target_path):
    if args.viz:
        from plotly import graph_objects as go

        from metasim.utils.viz_utils import plot_point_cloud

    # Robot configurations
    src_cfg = get_robot(args.source_robot)
    target_robot_cfgs = [get_robot(r) for r in args.target_robots]

    src_kin, src_fk, src_ik = get_curobo_models(src_cfg, args.ignore_ground_collision)
    tgts_ik = [get_curobo_models(cfg, args.ignore_ground_collision)[2] for cfg in target_robot_cfgs]

    # Prepare file structure
    demo_data = load_traj_file(source_path)

    if "ur5e_2f85" in args.target_robots:
        assert len(args.target_robots) == 1, "Only one target robot is supported when retargetting to UR5e_2F85"
        for k, v in demo_data.items():
            for i in range(len(v)):
                demo_data[k][i]["actions"] = demo_data[k][i]["actions"][30:]
                if demo_data[k][i].get("states", None) is not None:
                    demo_data[k][i]["states"] = demo_data[k][i]["states"][30:]

    source_demo_data = demo_data[src_cfg.name]
    n_demo = len(source_demo_data)
    episode_lengths = torch.tensor(
        [len(source_demo["actions"]) for source_demo in source_demo_data], dtype=torch.int, device=args.device
    )
    max_episode_len = episode_lengths.max().item()

    # Compute source trajectory: (JS pose ->) EE pose -> TCP pose
    arm_joint_names = [jn for jn, jn_cfg in src_cfg.actuators.items() if not jn_cfg.is_ee]
    gripper_joint_names = [jn for jn, jn_cfg in src_cfg.actuators.items() if jn_cfg.is_ee]
    curobo_joints = src_ik.robot_config.cspace.joint_names

    robot_pos = np.stack(
        [np.array(source_demo["init_state"][src_cfg.name]["pos"]) for source_demo in source_demo_data],
        axis=0,
    )
    robot_quat = np.stack(
        [np.array(source_demo["init_state"][src_cfg.name]["rot"]) for source_demo in source_demo_data],
        axis=0,
    )
    robot_pos = torch.from_numpy(robot_pos).to(args.device).float()
    robot_quat = torch.from_numpy(robot_quat).to(args.device).float()
    robot_rotmat = transforms.quaternion_to_matrix(robot_quat)

    robot_q_traj = np.stack(
        [
            np.pad(
                np.asarray([
                    [a["dof_pos_target"][j] for j in (arm_joint_names + gripper_joint_names)]
                    for a in source_demo["actions"]
                ]),
                [(0, max_episode_len - len(source_demo["actions"])), (0, 0)],
                mode="edge",
            )
            for source_demo in source_demo_data
        ],
        axis=0,
    )

    # Align with cuRobo: Some robot does not have gripper joints
    robot_q_traj = torch.from_numpy(robot_q_traj).to(args.device).float()[..., : len(curobo_joints)]

    ee_act_traj = np.stack(
        [
            np.pad(
                np.asarray([[a["dof_pos_target"][j] for j in gripper_joint_names] for a in source_demo["actions"]]),
                [(0, max_episode_len - len(source_demo["actions"])), (0, 0)],
                mode="edge",
            )
            for source_demo in source_demo_data
        ],
        axis=0,
    )
    ee_act_traj = torch.from_numpy(ee_act_traj).to(args.device).float()

    if "ee_pose_target" in source_demo_data[0]["actions"][0]:
        src_ee_pos_traj = np.stack(
            [
                np.pad(
                    np.asarray([a["ee_pose_target"]["pos"] for a in source_demo["actions"]]),
                    [(0, max_episode_len - len(source_demo["actions"])), (0, 0)],
                    mode="edge",
                )
                for source_demo in source_demo_data
            ],
            axis=0,
        )
        src_ee_quat_traj = np.stack(
            [
                np.pad(
                    np.asarray([a["ee_pose_target"]["rot"] for a in source_demo["actions"]]),
                    [(0, max_episode_len - len(source_demo["actions"])), (0, 0)],
                    mode="edge",
                )
                for source_demo in source_demo_data
            ],
            axis=0,
        )
        ee_act_traj = np.stack(
            [
                np.pad(
                    np.array([a["ee_pose_target"]["gripper_joint_pos"] for a in source_demo["actions"]]),
                    [(0, max_episode_len - len(source_demo["actions"])), (0, 0)],
                    mode="edge",
                )
                for source_demo in source_demo_data
            ],
            axis=0,
        )
        src_ee_pos_traj = torch.from_numpy(src_ee_pos_traj).to(args.device).float()
        src_ee_quat_traj = torch.from_numpy(src_ee_quat_traj).to(args.device).float()
    else:
        # The EE information are missing, compute from JS pose
        log.warning("EE pose information is missing, computing from joint space pose")
        src_ee_pos_traj, src_ee_quat_traj = [], []
        for i_traj in trange(len(source_demo_data), desc=f"Computing EE pose for source robot: {src_cfg.name}"):
            # JS pose -> EE pose (local) -> EE pose (world)
            ee_traj, quat_traj = src_fk(robot_q_traj[i_traj].contiguous())
            ee_traj_world = torch.matmul(ee_traj, robot_rotmat[i_traj].T) + robot_pos[i_traj]
            quat_traj_world = transforms.quaternion_multiply(robot_quat[i_traj], quat_traj)
            # for i_step in range(len(source_demo_data[i_traj]["actions"])):
            #     source_demo_data[i_traj]["actions"][i_step]["ee_pose_target"] = {
            #         "pos": ee_traj_world[i_step].cpu().numpy().tolist(),
            #         "rot": quat_traj_world[i_step].cpu().numpy().tolist(),
            #         # Average joint pose of two fingers
            #         "gripper_joint_pos": ee_act_traj[i_traj, i_step].mean().item(),
            #     }
            src_ee_pos_traj.append(ee_traj.clone())
            src_ee_quat_traj.append(quat_traj.clone())

        # These are still in the robot's local frame (for solving IK)
        src_ee_pos_traj = torch.stack(src_ee_pos_traj, dim=0)
        src_ee_quat_traj = torch.stack(src_ee_quat_traj, dim=0)

    tcp_pos_traj, tcp_quat_traj = tcp_pose_from_ee_pose(src_cfg, src_ee_pos_traj, src_ee_quat_traj)

    tcp_pos_traj = tcp_pos_traj.reshape(n_demo, max_episode_len, 3)
    tcp_quat_traj = tcp_quat_traj.reshape(n_demo, max_episode_len, 4)

    # Visualziation
    to_plot = []
    if args.viz:
        # for i in range(0, len(src_ee_pos_traj), 32):
        #     robot_mesh = source_robot_kin_model.get_robot_as_mesh(robot_q_traj[0, i : i + 1].contiguous())
        #     to_plot.append(plot_mesh(robot_mesh))
        to_plot.append(
            plot_point_cloud(
                src_ee_pos_traj[0].cpu().numpy(),
                name=f"Source: {src_cfg.name}",
                marker=dict(color=ee_act_traj[0].cpu().numpy()),
            )
        )

    # For each target embodiment, compute target trajecotry via IK: TCP pose -> EE pose -> JS pose
    for i_robot, (tgt_cfg, tgt_ik) in enumerate(zip(target_robot_cfgs, tgts_ik)):
        tgt_robot_demo_data = deepcopy(source_demo_data)
        current_q = None
        succ = torch.ones([n_demo], dtype=torch.bool, device=args.device)

        target_dof = len(tgt_ik.robot_config.cspace.joint_names)
        result_q = torch.zeros([n_demo, max_episode_len, target_dof], device=args.device)

        tgt_ee_pos_traj = torch.zeros([n_demo, max_episode_len, 3], device=args.device)
        tgt_ee_quat_traj = torch.zeros([n_demo, max_episode_len, 4], device=args.device)

        log.info(f"Retargetting: {src_cfg.name} -> {tgt_cfg.name}")
        tt = trange(max_episode_len, desc=f"{src_cfg.name} -> {tgt_cfg.name}")

        for t in tt:
            # Only solve IK for unfinished and unfailed trajectories
            valid_idx = torch.where((t <= episode_lengths) * succ)[0]
            if len(valid_idx) == 0:
                log.error("gg")
                break

            n_succ, n_fail = ((t >= episode_lengths - 1) * succ).sum(), (~succ).sum()

            tgt_ee_pos_traj[valid_idx, t], tgt_ee_quat_traj[valid_idx, t] = ee_pose_from_tcp_pose(
                tgt_cfg, tcp_pos_traj[valid_idx, t], tcp_quat_traj[valid_idx, t]
            )

            seed_config = result_q[:, t - 1 : t].tile([1, NUM_SEED, 1])
            result = tgt_ik.solve_batch(
                Pose(tgt_ee_pos_traj[:, t], tgt_ee_quat_traj[:, t]), seed_config=seed_config if t > 0 else None
            )

            result_q[valid_idx, t] = result.solution[valid_idx, 0]
            succ[valid_idx] = succ[valid_idx] * result.success.squeeze()[valid_idx]

            tt.set_description(
                f"{src_cfg.name} -> {tgt_cfg.name} | {n_succ.item()!s} succ | {n_fail.item()!s} fail | {n_demo!s} total"
            )
            tt.refresh()

        if args.viz:
            to_plot.append(plot_point_cloud(tgt_ee_pos_traj[0].cpu().numpy(), name=tgt_cfg.name))

        src_release_q = torch.tensor([[src_cfg.gripper_release_q]]).to(args.device).tile([n_demo, max_episode_len, 1])
        src_actuate_q = torch.tensor([[src_cfg.gripper_actuate_q]]).to(args.device).tile([n_demo, max_episode_len, 1])
        tgt_release_q = torch.tensor([[tgt_cfg.gripper_release_q]]).to(args.device).tile([n_demo, max_episode_len, 1])
        tgt_actuate_q = torch.tensor([[tgt_cfg.gripper_actuate_q]]).to(args.device).tile([n_demo, max_episode_len, 1])
        src_ee_act_rel = torch.abs(ee_act_traj - src_release_q) / torch.abs(src_actuate_q - src_release_q)
        src_ee_act_rel = src_ee_act_rel.mean(axis=-1)  # Avg over two fingers

        if tgt_cfg.ee_binary_action:
            src_ee_act_rel = (src_ee_act_rel > 0.5).float()
        src_ee_act_rel = src_ee_act_rel.unsqueeze(-1).tile([1, 1, tgt_release_q.shape[-1]])
        ee_act_traj = src_ee_act_rel * tgt_actuate_q + (1 - src_ee_act_rel) * tgt_release_q
        result_q = torch.cat([result_q, ee_act_traj], dim=-1)
        tgt_robot_joints = list(tgt_cfg.actuators.keys())

        # tgt_ee_pos_traj_world = torch.matmul(tgt_ee_pos_traj, robot_rotmat.permute(0, 2, 1)) + robot_pos.unsqueeze(1)
        # tgt_ee_quat_traj_world = transforms.quaternion_multiply(robot_quat, tgt_ee_quat_traj)

        log.info(f"Success rate: {(succ.float().mean().item() * 100):.2f}%, saving trajectories...")
        for i_succ in tqdm(torch.where(succ)[0], desc=f"Saving trajectories for {tgt_cfg.name}"):
            for i_step in range(episode_lengths[i_succ]):
                tgt_robot_demo_data[i_succ]["actions"][i_step]["dof_pos_target"] = dict(
                    zip(tgt_robot_joints, result_q[i_succ, i_step].cpu().numpy().tolist())
                )
                # tgt_robot_demo_data[i_succ]["actions"][i_step]["ee_pose_target"] = {
                #     "pos": tgt_ee_pos_traj_world[i_succ, i_step].cpu().numpy().tolist(),
                #     "rot": tgt_ee_quat_traj_world[i_succ, i_step].cpu().numpy().tolist(),
                #     "gripper_joint_pos": ee_act_traj[i_succ, i_step].mean().item,
                # }
            tgt_robot_demo_data[i_succ]["init_state"][tgt_cfg.name] = {
                "dof_pos": dict(zip(tgt_robot_joints, result_q[i_succ, 0].cpu().numpy().tolist())),
                "pos": robot_pos[i_succ].cpu().numpy().tolist(),
                "rot": robot_quat[i_succ].cpu().numpy().tolist(),
            }
            del tgt_robot_demo_data[i_succ]["init_state"][src_cfg.name]

        # Remove failed demos
        fail_succ = torch.where(~succ)[0].cpu().numpy().tolist()
        fail_succ.reverse()
        for i in fail_succ:
            del tgt_robot_demo_data[i]

        log.info(f"Saving trajectories for {tgt_cfg.name}")

        if args.viz:
            go.Figure(to_plot).show()

        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
        save_traj_file({tgt_cfg.name: tgt_robot_demo_data}, target_path)
        log.info(f"Retarget finished -> {target_path}")


def main():
    if args.tasks is not None:
        for task_name in args.tasks:
            task = get_task(task_name)
            source_path = task.traj_filepath
            if os.path.isdir(source_path):
                paths = glob(os.path.join(source_path, f"{args.source_robot}_v2.*"))
                assert len(paths) >= 1, f"No trajectories found for {args.source_robot}"
                source_path = paths[0]
            target_path = os.path.join(os.path.dirname(source_path), f"{args.target_robots[0]}_v2.pkl.gz")
            single(source_path, target_path)
    else:
        single(args.source_path, args.target_path)


if __name__ == "__main__":
    main()
