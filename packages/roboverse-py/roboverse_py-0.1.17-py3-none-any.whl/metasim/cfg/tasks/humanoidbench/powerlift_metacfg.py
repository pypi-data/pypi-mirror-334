"""Powerlift task for humanoid robots.

TODO: to be implemented
"""

from __future__ import annotations

import torch

from metasim.cfg.checkers import PowerliftChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.types import EnvState
from metasim.utils import configclass

from .base_metacfg import HumanoidTaskMetaCfg


class PowerliftReward:
    """Reward function for the powerlift task."""

    def __init__(self, robot_name="h1"):
        """Initialize the powerlift reward."""
        self.robot_name = robot_name

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        """Compute the powerlift reward."""
        return torch.zeros(len(states))


@configclass
class PowerliftMetaCfg(HumanoidTaskMetaCfg):
    """Powerlift task for humanoid robots."""

    episode_length = 1000
    objects = [
        RigidObjMetaCfg(
            name="powerlift",
            mjcf_path="roboverse_data/assets/humanoidbench/powerlift/powerlift/mjcf/powerlift.xml",
            physics=PhysicStateType.GEOM,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/humanoidbench/powerlift/v2/initial_state_v2.json"
    checker = PowerliftChecker()
    reward_weights = [1.0]
    reward_functions = [PowerliftReward]
