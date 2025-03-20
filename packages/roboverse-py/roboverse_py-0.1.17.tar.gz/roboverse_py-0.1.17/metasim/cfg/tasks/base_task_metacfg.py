"""Sub-module containing the base task configuration."""

from __future__ import annotations

from dataclasses import MISSING

import gymnasium as gym
import torch

from metasim.cfg.checkers import BaseChecker
from metasim.cfg.objects import BaseObjMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.types import EnvState
from metasim.utils import configclass


@configclass
class BaseTaskMetaCfg:
    """Base task configuration."""

    decimation: int = 3
    episode_length: int = MISSING
    objects: list[BaseObjMetaCfg] = MISSING
    traj_filepath: str = MISSING
    source_benchmark: BenchmarkType = MISSING
    task_type: TaskType = MISSING
    step_repeat: int = 1  # how many simulation steps to run for each step() call
    checker: BaseChecker = BaseChecker()
    can_tabletop: bool = False
    reward_functions: list[callable[[list[EnvState], str | None], torch.FloatTensor]] = MISSING
    reward_weights: list[float] = MISSING


@configclass
class BaseRLTaskMetaCfg(BaseTaskMetaCfg):
    """Base RL task configuration."""

    # action_space: gym.spaces.Space, can be inferenced from robot (joint_limits)
    observation_space: gym.spaces.Space = MISSING
    observation_function: callable[[list[EnvState]], torch.FloatTensor] = MISSING  # [dummy_obs]

    reward_range: tuple[float, float] = (-float("inf"), float("inf"))
