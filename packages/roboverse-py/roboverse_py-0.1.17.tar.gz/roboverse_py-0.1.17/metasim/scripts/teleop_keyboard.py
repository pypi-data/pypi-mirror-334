from __future__ import annotations

import argparse
import os
import sys
import time

import pygame
import rootutils
from curobo.types.math import Pose
from loguru import logger as log
from rich.logging import RichHandler

rootutils.setup_root(__file__, pythonpath=True)
log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])
from pytorch3d import transforms

from metasim.cfg.scenario import ScenarioMetaCfg
from metasim.utils.kinematics_utils import get_curobo_models
from metasim.utils.teleop_utils import PygameKeyboardClient, process_kb_input


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, required=True)
    parser.add_argument("--robot", type=str, default="franka")
    parser.add_argument("--num_envs", type=int, default=1, help="Number of environments to simulate.")
    parser.add_argument(
        "--sim",
        type=str,
        default="isaaclab",
        choices=["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco"],
    )
    parser.add_argument(
        "--render",
        type=str,
        choices=["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco"],
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    num_envs: int = args.num_envs

    # specificly for isaacgym
    if args.sim == "isaacgym":
        from isaacgym import gymapi, gymtorch, gymutil  # noqa: F401

    ## Import put here to support isaacgym

    import torch

    device = "cuda:0"

    from metasim.cfg.cameras import PinholeCameraMetaCfg
    from metasim.constants import SimType
    from metasim.double_sim import DoubleSimEnv
    from metasim.utils.demo_util import get_traj
    from metasim.utils.setup_util import get_robot, get_sim_env_class, get_task

    task = get_task(args.task)
    robot = get_robot(args.robot)
    camera = PinholeCameraMetaCfg(
        name="camera",
        data_types=["rgb", "depth"],
        width=256,
        height=256,
        pos=(1.5, 0.0, 1.5),
        look_at=(0.0, 0.0, 0.0),
    )
    scenario = ScenarioMetaCfg(task=task, robot=robot, cameras=[camera])

    tic = time.time()
    if args.render is None:
        env_class = get_sim_env_class(SimType(args.sim))
        env = env_class(scenario, num_envs)
    else:
        # print(args.sim, args.render)
        env_class_render = get_sim_env_class(SimType(args.render))
        env_render = env_class_render(scenario, num_envs)
        env_class_physics = get_sim_env_class(SimType(args.sim))
        env_physics = env_class_physics(scenario, num_envs)
        env = DoubleSimEnv(env_physics, env_render)
    toc = time.time()
    log.trace(f"Time to launch: {toc - tic:.2f}s")

    # data
    tic = time.time()
    assert os.path.exists(task.traj_filepath), f"Trajectory file: {task.traj_filepath} does not exist."
    init_states, all_actions, all_states = get_traj(task, robot, env.handler)
    toc = time.time()
    log.trace(f"Time to load data: {toc - tic:.2f}s")

    # reset before first step
    tic = time.time()
    obs, extras = env.reset(states=init_states[:num_envs])
    toc = time.time()
    log.trace(f"Time to reset: {toc - tic:.2f}s")

    # cuRobo IKSysFont()
    *_, robot_ik = get_curobo_models(robot)
    curobo_n_dof = len(robot_ik.robot_config.cspace.joint_names)
    ee_n_dof = len(robot.gripper_release_q)

    keyboard_client = PygameKeyboardClient(width=670, height=870, title="Keyboard Control")
    gripper_actuate_tensor = torch.tensor(robot.gripper_actuate_q, dtype=torch.float32, device=device)
    gripper_release_tensor = torch.tensor(robot.gripper_release_q, dtype=torch.float32, device=device)

    for line, instruction in enumerate(keyboard_client.instructions):
        log.info(f"{line:2d}: {instruction}")

    step = 0
    running = True
    while running:
        # update keyboard events every frame
        running = keyboard_client.update()
        if not running:
            break

        if keyboard_client.is_pressed(pygame.K_ESCAPE):
            log.debug("Exiting simulation...")
            running = False
            break

        keyboard_client.draw_instructions()

        obs = env.handler.get_observation()

        # compute target
        curr_robot_q = obs["joint_qpos"].cuda()
        robot_ee_state = obs["robot_ee_state"].cuda()
        robot_root_state = obs["robot_root_state"].cuda()
        robot_pos, robot_quat = robot_root_state[:, 0:3], robot_root_state[:, 3:7]
        curr_ee_pos, curr_ee_quat = robot_ee_state[:, 0:3], robot_ee_state[:, 3:7]

        curr_ee_pos = transforms.quaternion_apply(transforms.quaternion_invert(robot_quat), curr_ee_pos - robot_pos)
        curr_ee_quat_local = transforms.quaternion_multiply(transforms.quaternion_invert(robot_quat), curr_ee_quat)

        d_pos, d_rot_local, close_gripper = process_kb_input(keyboard_client, dpos=0.01, drot=0.05)
        d_pos_tensor = torch.tensor(d_pos, dtype=torch.float32, device=device)
        d_rot_tensor = torch.tensor(d_rot_local, dtype=torch.float32, device=device)
        gripper_q = gripper_actuate_tensor if close_gripper else gripper_release_tensor
        # delta quaternion
        d_rot_mat_local = transforms.euler_angles_to_matrix(d_rot_tensor.unsqueeze(0), "XYZ")
        d_quat_local = transforms.matrix_to_quaternion(d_rot_mat_local)[0]  # (4,)
        ee_pos_target = curr_ee_pos + d_pos_tensor
        ee_quat_target_local = transforms.quaternion_multiply(curr_ee_quat_local, d_quat_local)

        seed_config = curr_robot_q[:, :curobo_n_dof].unsqueeze(1).tile([1, robot_ik._num_seeds, 1])
        result = robot_ik.solve_batch(
            Pose(ee_pos_target.unsqueeze(0), ee_quat_target_local.unsqueeze(0)), seed_config=seed_config
        )

        ik_succ = result.success.squeeze(1)
        q = curr_robot_q.clone()  # shape: [num_envs, robot.num_joints]
        q[ik_succ, :curobo_n_dof] = result.solution[ik_succ, 0].clone()
        q[:, -ee_n_dof:] = gripper_q

        # XXX: this may not work for all simulators, since the order of joints may be different
        actions = [
            {"dof_pos_target": dict(zip(robot.joint_limits.keys(), q[i_env].tolist()))} for i_env in range(num_envs)
        ]
        env.handler.step(actions)
        env.handler.render()

        step += 1
        log.debug(f"Step {step}")

    keyboard_client.close()
    env.handler.close()
    sys.exit()


if __name__ == "__main__":
    main()
