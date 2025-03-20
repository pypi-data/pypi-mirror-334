"""Going through poles task for humanoid robots.

TODO: Not Implemented because of collision detection issues.
"""

from __future__ import annotations

import torch

from metasim.cfg.checkers import PoleChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.types import EnvState
from metasim.utils import configclass

from .base_metacfg import HumanoidTaskMetaCfg


class PoleReward:
    """Reward function for the pole task."""

    def __init__(self, robot_name="h1"):
        """Initialize the pole reward."""
        self.robot_name = robot_name

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        """Compute the pole reward."""
        return torch.zeros(len(states))


@configclass
class PoleMetaCfg(HumanoidTaskMetaCfg):
    """Going through poles task for humanoid robots."""

    episode_length = 1000
    objects = [
        RigidObjMetaCfg(
            name="floor",
            mjcf_path="roboverse_data/assets/humanoidbench/pole/floor/mjcf/floor.xml",
            physics=PhysicStateType.GEOM,
            fix_base_link=True,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/humanoidbench/pole/v2/initial_state_v2.json"
    checker = PoleChecker()
    reward_weights = [1.0]
    reward_functions = [PoleReward]
