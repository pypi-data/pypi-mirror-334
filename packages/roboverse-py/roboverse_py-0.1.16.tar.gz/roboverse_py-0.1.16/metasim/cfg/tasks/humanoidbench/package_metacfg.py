"""Package task for humanoid robots.

TODO: to be implemented
"""

from __future__ import annotations

import torch

from metasim.cfg.checkers import PackageChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.types import EnvState
from metasim.utils import configclass

from .base_metacfg import HumanoidTaskMetaCfg


class PackageReward:
    """Reward function for the package task."""

    def __init__(self, robot_name="h1"):
        """Initialize the package reward."""
        self.robot_name = robot_name

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        """Compute the package reward."""
        return torch.zeros(len(states))


@configclass
class PackageMetaCfg(HumanoidTaskMetaCfg):
    """Package task for humanoid robots."""

    episode_length = 1000
    objects = [
        RigidObjMetaCfg(
            name="package",
            mjcf_path="roboverse_data/assets/humanoidbench/package/package/mjcf/package.xml",
            physics=PhysicStateType.GEOM,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/humanoidbench/package/v2/initial_state_v2.json"
    checker = PackageChecker()
    reward_weights = [1.0]
    reward_functions = [PackageReward]
