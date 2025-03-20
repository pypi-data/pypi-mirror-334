from __future__ import annotations

import argparse
import logging
import os
import time

import numpy as np
import rootutils
import tqdm
from loguru import logger as log
from rich.logging import RichHandler

rootutils.setup_root(__file__, pythonpath=True)

logging.addLevelName(5, "TRACE")
log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, required=True)
    parser.add_argument("--robot", type=str, default="franka")
    parser.add_argument("--num_envs", type=int, default=1, help="Number of environments to simulate.")
    parser.add_argument("--num_trajs", type=int, default=10, help="Number of trajectories to play.")
    parser.add_argument(
        "--sim", type=str, default="isaaclab", choices=["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien"]
    )
    parser.add_argument("--object_states", action="store_true", help="Replay object states.")
    args = parser.parse_args()
    return args


###########################################################
## Utils
###########################################################
def get_actions(all_actions, action_idx: int, num_envs: int):
    envs_actions = all_actions[:num_envs]
    actions = [
        env_actions[action_idx] if action_idx < len(env_actions) else env_actions[-1] for env_actions in envs_actions
    ]
    return actions


def get_states(all_states, action_idx: int, num_envs: int):
    envs_states = all_states[:num_envs]
    states = [env_states[action_idx] if action_idx < len(env_states) else env_states[-1] for env_states in envs_states]
    return states


def save_obs(obs, step: int):
    from torchvision.utils import make_grid, save_image

    if obs is None:
        return

    rgb_data = obs["rgb"]  # (N, H, W, C), uint8
    image = make_grid(rgb_data.permute(0, 3, 1, 2) / 255, nrow=int(rgb_data.shape[0] ** 0.5))  # (C, H, W)
    os.makedirs("tmp", exist_ok=True)
    save_image(image, f"tmp/rgb_all_{step:04d}.png")


###########################################################
## Main
###########################################################
def main():
    args = parse_args()
    num_envs: int = args.num_envs

    # specificly for isaacgym
    if args.sim == "isaacgym":
        from isaacgym import gymapi, gymtorch, gymutil  # noqa: F401

    ## Import put here to support isaacgym

    from metasim.cfg.cameras import PinholeCameraMetaCfg
    from metasim.cfg.scenario import ScenarioMetaCfg
    from metasim.constants import SimType
    from metasim.utils.demo_util import get_traj
    from metasim.utils.setup_util import get_robot, get_sim_env_class, get_task

    gym_env_class = get_sim_env_class(SimType(args.sim))
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
    gym_env = gym_env_class(scenario, num_envs)

    ## Data
    tic = time.time()
    assert os.path.exists(task.traj_filepath), f"Trajectory file: {task.traj_filepath} does not exist."
    init_states, all_actions, all_states = get_traj(task, robot, gym_env)
    init_states = init_states[: args.num_trajs]
    all_actions = all_actions[: args.num_trajs]
    all_states = all_states[: args.num_trajs]
    toc = time.time()
    log.trace(f"Time to load data: {toc - tic:.2f}s")

    ########################################################
    ## Main
    ########################################################

    success_list = []
    episode_success_list = []

    with tqdm.tqdm(total=len(init_states)) as pbar:
        for init_state, action_list, state_list in zip(init_states, all_actions, all_states):
            ## Reset before first step
            if args.sim == "pyrep":
                log.warning("IsaacGym does not support getting init states, skipping...")
            else:
                gym_env.handler.set_states([init_state])

            ## Main loop
            step = 0
            episode_success = []

            for action, state in zip(action_list, state_list):
                if args.object_states:
                    if args.sim == "isaacgym":
                        raise NotImplementedError("IsaacGym does not support object states")
                    if all_states is None:
                        raise ValueError("All states are None, please check the trajectory file")
                    gym_env.handler.render()
                    gym_env.handler.set_states([state])

                    ## XXX: hackdemo_idx
                    success = gym_env.handler.task.checker.check(gym_env.handler)

                else:
                    obs, reward, success, time_out, extras = gym_env.step([action])

                    episode_success.append(success)
                    success_list.append(success)

            episode_success = np.stack(episode_success)
            episode_success = np.any(episode_success, axis=0)
            episode_success_list.append(episode_success)

            pbar.update(1)

    success_list = np.stack(success_list)
    episode_success_list = np.stack(episode_success_list)

    avg_success = np.mean(success_list, axis=0)
    avg_episode_success = np.mean(episode_success_list, axis=0)

    print("Avg success:", avg_success)
    print("Avg episode success", avg_episode_success)


if __name__ == "__main__":
    main()
