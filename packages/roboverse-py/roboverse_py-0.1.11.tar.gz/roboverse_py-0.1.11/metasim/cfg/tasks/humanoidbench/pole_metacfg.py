from __future__ import annotations

import torch

from metasim.cfg.checkers import PoleChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.types import EnvState
from metasim.utils import configclass

from .base_locomotion_env import HumanoidTaskMetaCfg


class PoleReward:
    def __init__(self, robot_name="h1"):
        self.robot_name = robot_name

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        return torch.zeros(len(states))


@configclass
class PoleMetaCfg(HumanoidTaskMetaCfg):
    episode_length = 1000
    objects = [
        RigidObjMetaCfg(
            name="floor",
            mjcf_path="roboverse_data/assets/humanoidbench/pole/floor/mjcf/floor.xml",
            physics=PhysicStateType.GEOM,
            fix_base_link=True,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/humanoidbench/pole/v2/h1_initial_state_v2.json"
    checker = PoleChecker()
    reward_weights = [1.0]
    reward_functions = [PoleReward(robot_name="h1")]
