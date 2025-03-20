"""Exit Door task for humanoid robots.

TODO: to be implemented
"""

from __future__ import annotations

import torch

from metasim.cfg.checkers import DoorChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.types import EnvState
from metasim.utils import configclass

from .base_metacfg import HumanoidTaskMetaCfg


class DoorReward:
    """Reward function for the door task."""

    def __init__(self, robot_name="h1"):
        """Initialize the door reward."""
        self.robot_name = robot_name

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        """Compute the door reward."""
        return torch.zeros(len(states))


@configclass
class DoorMetaCfg(HumanoidTaskMetaCfg):
    """Door task for humanoid robots."""

    episode_length = 1000
    objects = [
        RigidObjMetaCfg(
            name="door",
            mjcf_path="roboverse_data/assets/humanoidbench/door/door/mjcf/door.xml",
            physics=PhysicStateType.GEOM,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/humanoidbench/door/v2/initial_state_v2.json"
    checker = DoorChecker()
    reward_weights = [1.0]
    reward_functions = [DoorReward]
