from __future__ import annotations

import importlib

import gymnasium as gym
from loguru import logger as log

from metasim.cfg.robots.base_robot_metacfg import BaseRobotMetaCfg
from metasim.cfg.scenes import SceneMetaCfg
from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.constants import SimType
from metasim.utils import is_camel_case, is_snake_case, to_camel_case, to_snake_case


def get_sim_env_class(sim: SimType):
    if sim == SimType.ISAACLAB:
        try:
            from metasim.sim.isaaclab import IsaaclabEnv

            return IsaaclabEnv
        except ImportError as e:
            log.error("IsaacLab is not installed, please install it first")
            raise e
    elif sim == SimType.ISAACGYM:
        try:
            from metasim.sim.isaacgym.isaacgym import IsaacgymEnv

            return IsaacgymEnv
        except ImportError as e:
            log.error("IsaacGym is not installed, please install it first")
            raise e
    elif sim == SimType.PYREP:
        try:
            from metasim.sim.pyrep import PyrepHandler

            return PyrepHandler
        except ImportError as e:
            log.error("PyRep is not installed, please install it first")
            raise e
    elif sim == SimType.PYBULLET:
        try:
            from metasim.sim.pybullet import PybulletEnv

            return PybulletEnv
        except ImportError as e:
            log.error("PyBullet is not installed, please install it first")
            raise e
    elif sim == SimType.SAPIEN:
        try:
            from metasim.sim.sapien import SapienEnv

            return SapienEnv
        except ImportError as e:
            log.error("Sapien is not installed, please install it first")
            raise e
    elif sim == SimType.MUJOCO:
        try:
            from metasim.sim.mujoco import MujocoEnv

            return MujocoEnv
        except ImportError as e:
            log.error("Mujoco is not installed, please install it first")
            raise e
    elif sim == SimType.BLENDER:
        try:
            from metasim.sim.blender import BlenderEnv

            return BlenderEnv
        except ImportError as e:
            log.error("Blender is not installed, please install it first")
            raise e
    else:
        raise ValueError(f"Invalid simulator type: {sim}")


def get_task(task_id: str) -> BaseTaskMetaCfg:
    if ":" in task_id:
        prefix, task_name = task_id.split(":")
    else:
        prefix, task_name = None, task_id

    if is_camel_case(task_name):
        task_name_camel = task_name
        task_name_snake = to_snake_case(task_name)
    elif is_snake_case(task_name):
        task_name_camel = to_camel_case(task_name, to="CC")
        task_name_snake = task_name
    else:
        raise ValueError(f"Invalid task name: {task_id}, should be in either camel case or snake case")

    import_path = f"metasim.cfg.tasks.{prefix}" if prefix is not None else "metasim.cfg.tasks"
    module = importlib.import_module(import_path)
    task_cls = getattr(module, f"{task_name_camel}MetaCfg")
    gym.register(
        task_name_camel,
        entry_point="metasim.scripts.train_ppo_vec:MetaSimVecEnv",
        kwargs={"task_name": task_name},
    )
    gym.register(
        task_name_snake,
        entry_point="metasim.scripts.train_ppo_vec:MetaSimVecEnv",
        kwargs={"task_name": task_name},
    )
    return task_cls()


def get_robot(robot_name: str) -> BaseRobotMetaCfg:
    if is_camel_case(robot_name):
        RobotName = robot_name
    elif is_snake_case(robot_name):
        RobotName = to_camel_case(robot_name, to="CC")
    else:
        raise ValueError(f"Invalid robot name: {robot_name}, should be in either camel case or snake case")
    module = importlib.import_module("metasim.cfg.robots")
    robot_cls = getattr(module, f"{RobotName}MetaCfg")
    return robot_cls()


def get_scene(scene_name: str) -> SceneMetaCfg:
    if is_snake_case(scene_name):
        scene_name = to_camel_case(scene_name, to="CC")
    try:
        module = importlib.import_module("metasim.cfg.scenes")
        scene_cls = getattr(module, f"{scene_name}MetaCfg")
        return scene_cls()
    except (ImportError, AttributeError) as e:
        raise ValueError(f"Scene {scene_name} not found: {e}") from e
