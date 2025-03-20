from __future__ import annotations

import argparse
import json
import os
import time

import isaacgym  # noqa: F401
import numpy as np
import rootutils
import torch
from curobo.types.math import Pose
from loguru import logger as log
from pytorch3d import transforms
from rich.logging import RichHandler

rootutils.setup_root(__file__, pythonpath=True)
log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_envs", type=int, default=1)
    parser.add_argument("--sim", type=str, default="isaaclab", choices=["isaaclab", "isaacgym", "mujoco"])
    parser.add_argument("--task", type=str, default="PickCube")
    parser.add_argument(
        "--robot",
        type=str,
        default="franka",
        choices=[
            "franka",
            "ur5e_2f85",
            "sawyer",
            "franka_with_gripper_extension",
            "h1_2_without_hand",
            "h1",
            "h1_simple_hand",
            "sawyer_mujoco",
            "fetch",
        ],
    )
    parser.add_argument("--add_table", action="store_true")
    parser.add_argument(
        "--joints", default=None, nargs="+", type=str, help="Joints to randomize, if None, randomize all joints"
    )
    args = parser.parse_args()
    return args


def get_gapartnet_anno(anno_path):
    """
    Get gapartnet annotation
    """
    info = {}
    # load object annotation
    anno = json.loads(open(anno_path).read())
    num_link_anno = len(anno)
    gapart_raw_valid_anno = []
    for link_i in range(num_link_anno):
        anno_i = anno[link_i]
        if anno_i["is_gapart"]:
            gapart_raw_valid_anno.append(anno_i)
    info["gapart_cates"] = [anno_i["category"] for anno_i in gapart_raw_valid_anno]
    info["gapart_init_bboxes"] = np.array([np.asarray(anno_i["bbox"]) for anno_i in gapart_raw_valid_anno])
    info["gapart_link_names"] = [anno_i["link_name"] for anno_i in gapart_raw_valid_anno]
    return info


def control_to_pose(
    env,
    num_envs,
    robot,
    ee_pos_target,
    rotation,
    gripper_widths,
    robot_ik,
    curobo_n_dof,
    ee_n_dof,
    seed_config,
    steps=3,
):
    pass
    # Solve IK
    result = robot_ik.solve_batch(Pose(ee_pos_target, rotation=rotation), seed_config=seed_config)

    q = torch.zeros((num_envs, robot.num_joints), device="cuda:0")
    ik_succ = result.success.squeeze(1)
    q[ik_succ, :curobo_n_dof] = result.solution[ik_succ, 0].clone()
    q[:, -ee_n_dof:] = gripper_widths

    actions = [{"dof_pos_target": dict(zip(robot.actuators.keys(), q[i_env].tolist()))} for i_env in range(num_envs)]

    for i_step in range(steps):
        env.step(actions)
        env.render()
    return actions


def main():
    args = parse_args()
    num_envs: int = args.num_envs

    # specificly for isaacgym
    if args.sim == "isaacgym":
        from isaacgym import gymapi, gymtorch, gymutil  # noqa: F401

    ## Import put here to support isaacgym

    import torch

    from metasim.cfg.scenario import ScenarioMetaCfg
    from metasim.constants import SimType
    from metasim.utils.demo_util import get_traj
    from metasim.utils.kinematics_utils import get_curobo_models
    from metasim.utils.setup_util import get_robot, get_sim_env_class

    scenario = ScenarioMetaCfg(task=args.task, robot=args.robot, try_add_table=args.add_table, sim=args.sim)

    robot = get_robot(args.robot)
    *_, robot_ik = get_curobo_models(robot)
    curobo_n_dof = len(robot_ik.robot_config.cspace.joint_names)
    ee_n_dof = len(robot.gripper_release_q)

    log.info(f"Using simulator: {args.sim}")
    env_class = get_sim_env_class(SimType(args.sim))
    env = env_class(scenario, num_envs)

    ## Main
    tic = time.time()
    assert os.path.exists(scenario.task.traj_filepath), (
        f"Trajectory file: {scenario.task.traj_filepath} does not exist."
    )
    init_states, all_actions, all_states = get_traj(scenario.task, scenario.robot, env.handler)
    toc = time.time()
    log.trace(f"Time to load data: {toc - tic:.2f}s")
    ## Reset before first step
    tic = time.time()
    obs, extras = env.reset(states=init_states[:num_envs])
    toc = time.time()
    log.trace(f"Time to reset: {toc - tic:.2f}s")

    # Generate random actions
    urdf_path = scenario.task.objects[0].urdf_path
    anno_path = urdf_path.replace("mobility_annotation_gapartnet.urdf", "link_annotation_gapartnet.json")
    gapartnet_anno = get_gapartnet_anno(anno_path)

    ee_rot_target = torch.rand((num_envs, 3), device="cuda:0") * torch.pi
    ee_quat_target = transforms.matrix_to_quaternion(transforms.euler_angles_to_matrix(ee_rot_target, "XYZ"))

    # Compute targets
    curr_robot_q = obs["joint_qpos"].cuda()
    robot_root_state = obs["robot_root_state"].cuda()
    robot_pos, robot_quat = robot_root_state[:, 0:3], robot_root_state[:, 3:7]
    seed_config = curr_robot_q[:, :curobo_n_dof].unsqueeze(1).tile([1, robot_ik._num_seeds, 1])

    bbox_id = -1
    all_bbox_now = gapartnet_anno["gapart_init_bboxes"] * scenario.task.objects[0].scale + np.array(
        init_states[0]["cabinet"]["pos"]
    )
    # get the part bbox and calculate the handle direction
    all_bbox_now = torch.tensor(all_bbox_now, dtype=torch.float32).to("cuda:0").reshape(-1, 8, 3)
    all_bbox_center_front_face = torch.mean(all_bbox_now[:, 0:4, :], dim=1)
    handle_out = all_bbox_now[:, 0, :] - all_bbox_now[:, 4, :]
    handle_out /= torch.norm(handle_out, dim=1, keepdim=True)
    handle_long = all_bbox_now[:, 0, :] - all_bbox_now[:, 1, :]
    handle_long /= torch.norm(handle_long, dim=1, keepdim=True)
    handle_short = all_bbox_now[:, 0, :] - all_bbox_now[:, 3, :]
    handle_short /= torch.norm(handle_short, dim=1, keepdim=True)

    init_position = all_bbox_center_front_face[bbox_id]
    handle_out_ = handle_out[bbox_id]

    gripper_widths = torch.tensor(robot.gripper_release_q).to("cuda:0")

    rotation_transform_for_franka = torch.tensor(
        [
            [0.0, 0.0, 1.0],
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0],
        ],
        device="cuda:0",
    )
    rotation_target = torch.stack(
        [
            -handle_out[bbox_id],
            -handle_short[bbox_id],
            handle_long[bbox_id],
        ],
        dim=0,
    )
    rotation = rotation_target @ rotation_transform_for_franka
    log.info("move to pre-grasp position")
    for i in range(30):
        control_to_pose(
            env,
            num_envs,
            robot,
            init_position + 0.2 * handle_out_,
            rotation,
            gripper_widths,
            robot_ik,
            curobo_n_dof,
            ee_n_dof,
            seed_config,
        )
    # move the object to the grasp position
    log.info("move to grasp position")
    for i in range(20):
        actions = control_to_pose(
            env,
            num_envs,
            robot,
            init_position + (0.1 - 0.015 * i) * handle_out_,
            rotation,
            gripper_widths,
            robot_ik,
            curobo_n_dof,
            ee_n_dof,
            seed_config,
            steps=3,
        )

    # close the gripper
    log.info("close the gripper")

    gripper_widths = torch.tensor(robot.gripper_release_q)
    gripper_widths[:] = 0.0
    actions[0]["dof_pos_target"]["panda_finger_joint1"] = 0.0
    actions[0]["dof_pos_target"]["panda_finger_joint2"] = 0.0
    for i in range(10):
        env.step(actions)
        env.render()

    # move the object to the lift position]
    log.info("move the object to the lift position")
    for i in range(30):
        control_to_pose(
            env,
            num_envs,
            robot,
            init_position + (-0.2 + i * 0.01) * handle_out_,
            rotation,
            gripper_widths,
            robot_ik,
            curobo_n_dof,
            ee_n_dof,
            seed_config,
        )

    log.info("done")


if __name__ == "__main__":
    main()
