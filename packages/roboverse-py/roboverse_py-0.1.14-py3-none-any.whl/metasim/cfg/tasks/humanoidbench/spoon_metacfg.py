"""Spoon in cup task for humanoid robots.

TODO: to be implemented
"""

from __future__ import annotations

import torch

from metasim.cfg.checkers import SpoonChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.types import EnvState
from metasim.utils import configclass

from .base_metacfg import HumanoidTaskMetaCfg


class SpoonReward:
    """Reward function for the spoon task."""

    def __init__(self, robot_name="h1"):
        """Initialize the spoon reward."""
        self.robot_name = robot_name

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        """Compute the spoon reward."""
        return torch.zeros(len(states))


@configclass
class SpoonMetaCfg(HumanoidTaskMetaCfg):
    """Spoon in cup task for humanoid robots."""

    episode_length = 1000
    objects = [
        RigidObjMetaCfg(
            name="spoon",
            mjcf_path="roboverse_data/assets/humanoidbench/spoon/spoon/mjcf/spoon.xml",
            physics=PhysicStateType.GEOM,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/humanoidbench/spoon/v2/initial_state_v2.json"
    checker = SpoonChecker()
    reward_weights = [1.0]
    reward_functions = [SpoonReward]
