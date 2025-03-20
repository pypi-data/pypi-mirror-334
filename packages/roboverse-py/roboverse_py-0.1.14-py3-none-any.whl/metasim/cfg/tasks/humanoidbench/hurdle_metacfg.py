"""Hurdle task for humanoid robots.

TODO: Not Implemented because of collision detection issues.
"""

from __future__ import annotations

import torch

from metasim.cfg.checkers import HurdleChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.types import EnvState
from metasim.utils import configclass

from .base_metacfg import HumanoidTaskMetaCfg


class HurdleReward:
    """Reward function for the hurdle task."""

    def __init__(self, robot_name="h1"):
        """Initialize the hurdle reward."""
        self.robot_name = robot_name

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        """Compute the hurdle reward."""
        return torch.zeros(len(states))


@configclass
class HurdleMetaCfg(HumanoidTaskMetaCfg):
    """Hurdle task for humanoid robots."""

    episode_length = 1000
    objects = [
        RigidObjMetaCfg(
            name="hurdle",
            mjcf_path="roboverse_data/assets/humanoidbench/hurdle/bracket/mjcf/bracket.xml",
            physics=PhysicStateType.GEOM,
            fix_base_link=True,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/humanoidbench/hurdle/v2/initial_state_v2.json"
    checker = HurdleChecker()
    reward_weights = [1.0]
    reward_functions = [HurdleReward]
