from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from typing import Literal

import rootutils
import tyro
from loguru import logger as log
from rich.logging import RichHandler

rootutils.setup_root(__file__, pythonpath=True)
from metasim.cfg.randomization import RandomizationMetaCfg
from metasim.cfg.render import RenderMetaCfg

logging.addLevelName(5, "TRACE")
log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])


@dataclass
class Args:
    random: RandomizationMetaCfg
    render: RenderMetaCfg
    task: str
    robot: Literal[
        "franka",
        "franka_with_gripper_extension",
        "sawyer",
        "iiwa",
        "h1_2_without_hand",
        "ur5e_2f85",
    ] = "franka"
    num_envs: int = 1
    sim: Literal["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco"] = "isaaclab"
    renderer: Literal["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco"] | None = None
    object_states: bool = False
    save_obs: bool = True


def parse_args() -> Args:
    args = tyro.cli(Args)
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

    if obs is None or obs.get("rgb", None) is None:
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
    if args.sim == "isaacgym" or args.render == "isaacgym":
        from isaacgym import gymapi, gymtorch, gymutil  # noqa: F401

    ## Import put here to support isaacgym

    from metasim.cfg.cameras import PinholeCameraMetaCfg
    from metasim.cfg.scenario import ScenarioMetaCfg
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
        pos=(1.5, -1.5, 1.5),  # near
        # pos=(12.0, -12.0, 20.0),  # far
        look_at=(0.0, 0.0, 0.0),
    )
    scenario = ScenarioMetaCfg(task=task, robot=robot, cameras=[camera], random=args.random, render=args.render)

    tic = time.time()
    if args.renderer is None:
        log.info(f"Using simulator: {args.sim}")
        env_class = get_sim_env_class(SimType(args.sim))
        env = env_class(scenario, num_envs)
    else:
        log.info(f"Using simulator: {args.sim}, renderer: {args.renderer}")
        env_class_render = get_sim_env_class(SimType(args.renderer))
        env_render = env_class_render(scenario, num_envs)  # Isaaclab must launch right after import
        env_class_physics = get_sim_env_class(SimType(args.sim))
        env_physics = env_class_physics(scenario, num_envs)  # Isaaclab must launch right after import
        env = DoubleSimEnv(env_physics, env_render)
    toc = time.time()
    log.trace(f"Time to launch: {toc - tic:.2f}s")

    ## Data
    tic = time.time()
    assert os.path.exists(task.traj_filepath), f"Trajectory file: {task.traj_filepath} does not exist."
    init_states, all_actions, all_states = get_traj(task, robot, env.handler)
    toc = time.time()
    log.trace(f"Time to load data: {toc - tic:.2f}s")

    ########################################################
    ## Main
    ########################################################

    ## Reset before first step
    tic = time.time()
    obs, extras = env.reset(states=init_states[:num_envs])
    toc = time.time()
    log.trace(f"Time to reset: {toc - tic:.2f}s")
    save_obs(obs, 0)

    ## Main loop
    step = 0
    while True:
        log.debug(f"Step {step}")
        tic = time.time()
        if args.object_states:
            ## TODO: merge states replay into env.step function
            if args.sim == "isaacgym":
                raise NotImplementedError("IsaacGym does not support object states")
            if all_states is None:
                raise ValueError("All states are None, please check the trajectory file")
            states = get_states(all_states, step, num_envs)

            env.handler.set_states(states)
            env.handler.refresh_render()
            obs = env.handler.get_observation()

            ## XXX: hack
            success = env.handler.task.checker.check(env.handler)
            if success.any():
                log.info(f"Env {success.nonzero().squeeze(-1).tolist()} succeeded!")
            if success.all():
                break

        else:
            actions = get_actions(all_actions, step, num_envs)
            obs, reward, success, time_out, extras = env.step(actions)

            if success.any():
                log.info(f"Env {success.nonzero().squeeze(-1).tolist()} succeeded!")

            if time_out.any():
                log.info(f"Env {time_out.nonzero().squeeze(-1).tolist()} timed out!")

            if success.all() or time_out.all():
                break

        toc = time.time()
        log.trace(f"Time to step: {toc - tic:.2f}s")

        tic = time.time()
        if args.save_obs:
            save_obs(obs, step + 1)
        toc = time.time()
        log.trace(f"Time to save obs: {toc - tic:.2f}s")
        step += 1

        if step == 30:
            # print(env.handler.get_states()[0].keys()) # get scene object keys
            print(
                "chocolate_pudding pos z:", env.handler.get_states()[0]["chocolate_pudding"]["pos"][2]
            )  # get scene object keys
            print("basket pos z:", env.handler.get_states()[0]["basket"]["pos"][2])
            print("orange_juice pos z:", env.handler.get_states()[0]["orange_juice"]["pos"][2])
            print("milk pos z:", env.handler.get_states()[0]["milk"]["pos"][2])
            print("cream_cheese pos z:", env.handler.get_states()[0]["cream_cheese"]["pos"][2])
            print("tomato_sauce pos z:", env.handler.get_states()[0]["tomato_sauce"]["pos"][2])
            print("butter pos z:", env.handler.get_states()[0]["butter"]["pos"][2])
            print("franka pos z: ", env.handler.get_states()[0]["franka"]["pos"][2])

            exit()


if __name__ == "__main__":
    main()
