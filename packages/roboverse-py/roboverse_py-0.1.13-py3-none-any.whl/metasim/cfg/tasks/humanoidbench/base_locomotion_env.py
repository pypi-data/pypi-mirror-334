from __future__ import annotations

import logging

import numpy as np
import torch
from dm_control.utils import rewards
from loguru import logger as log
from rich.logging import RichHandler

from metasim.cfg.tasks.base_task_metacfg import BaseRLTaskMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.types import EnvState
from metasim.utils import configclass
from metasim.utils.h1_utils import (
    actuator_forces,
    center_of_mass_velocity,
    head_height,
    torso_upright,
)

logging.addLevelName(5, "TRACE")
log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])

########################################################
## Constants adapted from humanoid_bench/tasks/basic_locomotion_envs.py
########################################################

# Height of head above which stand reward is 1.
_H1_STAND_HEIGHT = 1.65
_H1_CRAWL_HEIGHT = 0.8
_G1_STAND_HEIGHT = 1.28
_G1_CRAWL_HEIGHT = 0.6


@configclass
class HumanoidTaskMetaCfg(BaseRLTaskMetaCfg):
    decimation: int = 10
    source_benchmark = BenchmarkType.HUMANOIDBENCH
    task_type = TaskType.LOCOMOTION
    episode_length = 800  # TODO: may change
    objects = []
    reward_weights = [1.0]

    @staticmethod
    def observation_space(envstates: list[EnvState]) -> torch.Tensor:
        # TODO: currently hardcoding to [-inf,inf] in gym_env_wrapper
        pass

    @staticmethod
    def observation_function(envstates: list[EnvState]) -> torch.Tensor:
        # TODO: align torch.tensor or numpy.array
        env_obs = []
        for envstate in envstates:
            flattened = []
            for obj_name, obj_state in envstate.items():
                if obj_name == "h1" or obj_name == "g1" or obj_name == "h1_simple_hand":
                    for key in ["pos", "rot", "vel", "ang_vel"]:
                        if key in obj_state and obj_state[key] is not None:
                            flattened.append(np.array(obj_state[key]).flatten())

                    if "dof_pos" in obj_state:
                        for _, value in obj_state["dof_pos"].items():
                            if isinstance(value, (np.ndarray, float)):
                                flattened.append(np.array(value).flatten())

                    if "dof_vel" in obj_state:
                        for key, value in obj_state["dof_vel"].items():
                            if isinstance(value, (np.ndarray, float)):
                                flattened.append(np.array(value).flatten())
                    continue

                elif not obj_name.startswith("metasim"):
                    # flatten pos, rot, vel, ang_vel for other object. (state-based observation)
                    for key in ["pos", "rot", "vel", "ang_vel"]:
                        if key in obj_state and obj_state[key] is not None:
                            flattened.append(obj_state[key].numpy())

                env_obs.append(np.concatenate([arr.flatten() for arr in flattened]))

        return env_obs


class BaseLocomotionReward:
    _move_speed = None
    htarget_low = np.array([-1.0, -1.0, 0.8])
    htarget_high = np.array([1000.0, 1.0, 2.0])
    success_bar = None

    def __init__(self, robot_name="h1"):
        self.robot_name = robot_name
        if robot_name == "h1" or robot_name == "h1_simple_hand":
            self._stand_height = _H1_STAND_HEIGHT
            self._crawl_height = _H1_CRAWL_HEIGHT
        elif robot_name == "g1":
            self._stand_height = _G1_STAND_HEIGHT
            self._crawl_height = _G1_CRAWL_HEIGHT
        else:
            raise ValueError(f"Unknown robot {robot_name}")

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        ret_rewards = []
        ret_infos = []
        for state in states:
            standing = rewards.tolerance(
                head_height(state, self.robot_name),
                bounds=(self._stand_height, float("inf")),
                margin=self._stand_height / 4,
            )
            upright = rewards.tolerance(
                torso_upright(state, self.robot_name),
                bounds=(0.9, float("inf")),
                sigmoid="linear",
                margin=1.9,
                value_at_margin=0,
            )
            stand_reward = standing * upright
            small_control = rewards.tolerance(
                actuator_forces(state, self.robot_name),
                margin=10,
                value_at_margin=0,
                sigmoid="quadratic",
            ).mean()
            small_control = (4 + small_control) / 5
            if self._move_speed == 0:
                horizontal_velocity = center_of_mass_velocity(state, self.robot_name)[[0, 1]]
                dont_move = rewards.tolerance(horizontal_velocity, margin=2).mean()
                ret_rewards.append(small_control * stand_reward * dont_move)
                ret_infos.append({
                    "small_control": small_control,
                    "stand_reward": stand_reward,
                    "dont_move": dont_move,
                    "standing": standing,
                    "upright": upright,
                })
            else:
                com_velocity = center_of_mass_velocity(state, self.robot_name)[0]
                move = rewards.tolerance(
                    com_velocity,
                    bounds=(self._move_speed, float("inf")),
                    margin=self._move_speed,
                    value_at_margin=0,
                    sigmoid="linear",
                )
                move = (5 * move + 1) / 6
                reward = small_control * stand_reward * move
                ret_rewards.append(reward)
                ret_infos.append({
                    "stand_reward": stand_reward,
                    "small_control": small_control,
                    "move": move,
                    "standing": standing,
                    "upright": upright,
                })
        ret_rewards = torch.tensor(ret_rewards)
        return ret_rewards  # , ret_infos
