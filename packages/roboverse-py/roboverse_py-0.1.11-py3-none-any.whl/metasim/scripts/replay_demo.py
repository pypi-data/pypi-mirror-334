from __future__ import annotations

import logging
import os
import time
from typing import Literal

import imageio as iio
import numpy as np
import rootutils
import tyro
from loguru import logger as log
from numpy.typing import NDArray
from rich.logging import RichHandler
from tyro import MISSING

logging.addLevelName(5, "TRACE")
log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])
rootutils.setup_root(__file__, pythonpath=True)

from metasim.cfg.randomization import RandomizationMetaCfg
from metasim.cfg.render import RenderMetaCfg
from metasim.utils import configclass


@configclass
class Args:
    task: str = MISSING
    robot: str = "franka"
    scene: str | None = None
    render: RenderMetaCfg = RenderMetaCfg()
    random: RandomizationMetaCfg = RandomizationMetaCfg()

    ## Handlers
    sim: Literal["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco", "blender"] = "isaaclab"
    renderer: Literal["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco", "blender"] | None = None

    ## Others
    num_envs: int = 1
    try_add_table: bool = True
    object_states: bool = False
    split: Literal["train", "val", "test", "all"] = "all"
    headless: bool = False

    ## Only in args
    save_image_dir: str | None = "tmp"
    save_video_path: str | None = None
    stop_on_runout: bool = False

    def __post_init__(self):
        log.info(f"Args: {self}")


args = tyro.cli(Args)


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


def get_runout(all_actions, action_idx: int):
    runout = all([action_idx >= len(all_actions[i]) for i in range(len(all_actions))])
    return runout


class ObsSaver:
    def __init__(self, image_dir: str | None = None, video_path: str | None = None):
        assert image_dir is not None or video_path is not None
        self.image_dir = image_dir
        self.video_path = video_path
        self.images: list[NDArray] = []

        self.image_idx = 0

    def add(self, obs: dict):
        from torchvision.utils import make_grid, save_image

        if obs is None or obs.get("rgb", None) is None:
            return

        rgb_data = obs["rgb"]  # (N, H, W, C), uint8
        image = make_grid(rgb_data.permute(0, 3, 1, 2) / 255, nrow=int(rgb_data.shape[0] ** 0.5))  # (C, H, W)

        if self.image_dir is not None:
            os.makedirs(self.image_dir, exist_ok=True)
            save_image(image, os.path.join(self.image_dir, f"rgb_{self.image_idx:04d}.png"))
            self.image_idx += 1

        image = image.cpu().numpy().transpose(1, 2, 0)  # (H, W, C)
        image = (image * 255).astype(np.uint8)
        self.images.append(image)

    def save(self):
        if self.video_path is not None:
            log.info(f"Saving video of {len(self.images)} frames to {self.video_path}")
            os.makedirs(os.path.dirname(self.video_path), exist_ok=True)
            iio.mimsave(self.video_path, self.images, fps=30)


###########################################################
## Main
###########################################################
def main():
    # specificly for isaacgym
    if args.sim == "isaacgym" or args.render == "isaacgym":
        from isaacgym import gymapi, gymtorch, gymutil  # noqa: F401

    ## Import put here to support isaacgym
    from metasim.cfg.cameras import PinholeCameraMetaCfg
    from metasim.cfg.scenario import ScenarioMetaCfg
    from metasim.constants import SimType
    from metasim.double_sim import DoubleSimEnv
    from metasim.utils.demo_util import get_traj
    from metasim.utils.setup_util import get_sim_env_class

    camera = PinholeCameraMetaCfg(
        name="camera",
        data_types=["rgb", "depth"],
        width=256,
        height=256,
        pos=(1.5, -1.5, 1.5),  # near
        # pos=(12.0, -12.0, 20.0),  # far
        look_at=(0.0, 0.0, 0.0),
    )
    scenario = ScenarioMetaCfg(
        task=args.task,
        robot=args.robot,
        scene=args.scene,
        cameras=[camera],
        random=args.random,
        render=args.render,
        sim=args.sim,
        renderer=args.renderer,
        num_envs=args.num_envs,
        try_add_table=args.try_add_table,
        object_states=args.object_states,
        split=args.split,
        headless=args.headless,
    )

    num_envs: int = scenario.num_envs

    tic = time.time()
    if scenario.renderer is None:
        log.info(f"Using simulator: {scenario.sim}")
        env_class = get_sim_env_class(SimType(scenario.sim))
        env = env_class(scenario, num_envs, headless=scenario.headless)
    else:
        log.info(f"Using simulator: {scenario.sim}, renderer: {scenario.renderer}")
        env_class_render = get_sim_env_class(SimType(scenario.renderer))
        env_render = env_class_render(scenario, num_envs)  # Isaaclab must launch right after import
        env_class_physics = get_sim_env_class(SimType(scenario.sim))
        env_physics = env_class_physics(scenario, num_envs)  # Isaaclab must launch right after import
        env = DoubleSimEnv(env_physics, env_render)
    toc = time.time()
    log.trace(f"Time to launch: {toc - tic:.2f}s")

    ## Data
    tic = time.time()
    assert os.path.exists(scenario.task.traj_filepath), (
        f"Trajectory file: {scenario.task.traj_filepath} does not exist."
    )
    init_states, all_actions, all_states = get_traj(scenario.task, scenario.robot, env.handler)
    toc = time.time()
    log.trace(f"Time to load data: {toc - tic:.2f}s")

    ########################################################
    ## Main
    ########################################################

    obs_saver = ObsSaver(image_dir=args.save_image_dir, video_path=args.save_video_path)

    ## Reset before first step
    tic = time.time()
    obs, extras = env.reset(states=init_states[:num_envs])
    toc = time.time()
    log.trace(f"Time to reset: {toc - tic:.2f}s")
    obs_saver.add(obs)

    ## Main loop
    step = 0
    while True:
        log.debug(f"Step {step}")
        tic = time.time()
        if scenario.object_states:
            ## TODO: merge states replay into env.step function
            if scenario.sim == "isaacgym":
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
        obs_saver.add(obs)
        toc = time.time()
        log.trace(f"Time to save obs: {toc - tic:.2f}s")
        step += 1

        if args.stop_on_runout and get_runout(all_actions, step):
            log.info("Run out of actions, stopping")
            break

    obs_saver.save()


if __name__ == "__main__":
    main()
