from __future__ import annotations

from dataclasses import MISSING

import gymnasium as gym
import torch

from metasim.cfg.checkers import BaseChecker
from metasim.cfg.objects import BaseObjMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.types import EnvState
from metasim.utils import configclass


## TODO: move this to object definition
@configclass
class SiteMetaCfg:
    base_name: str = MISSING
    relative_pos: list[float] = MISSING
    relative_quat: list[float] = MISSING


@configclass
class BaseTaskMetaCfg:
    decimation: int = 3
    episode_length: int = MISSING
    objects: list[BaseObjMetaCfg] = MISSING
    traj_filepath: str = MISSING
    source_benchmark: BenchmarkType = MISSING
    task_type: TaskType = MISSING
    checker: BaseChecker = BaseChecker()
    can_tabletop: bool = False
    reward_functions: list[callable[[list[EnvState], str | None], torch.FloatTensor]] = MISSING
    reward_weights: list[float] = MISSING


@configclass
class BaseRLTaskMetaCfg(BaseTaskMetaCfg):
    # action_space: gym.spaces.Space, can be inferenced from robot (joint_limits)
    observation_space: gym.spaces.Space = MISSING
    observation_function: callable[[list[EnvState]], torch.FloatTensor] = MISSING  # [dummy_obs]

    reward_range: tuple[float, float] = (-float("inf"), float("inf"))
