from __future__ import annotations

import torch

from metasim.cfg.checkers import MazeChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.types import EnvState
from metasim.utils import configclass

from .base_locomotion_env import HumanoidTaskMetaCfg


class MazeReward:
    def __init__(self, robot_name="h1"):
        self.robot_name = robot_name

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        return torch.zeros(len(states))


@configclass
class MazeMetaCfg(HumanoidTaskMetaCfg):
    episode_length = 1000
    objects = [
        RigidObjMetaCfg(
            name="maze",
            mjcf_path="roboverse_data/assets/humanoidbench/maze/wall/mjcf/wall.xml",
            physics=PhysicStateType.GEOM,
            fix_base_link=True,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/humanoidbench/maze/v2/h1_initial_state_v2.json"
    checker = MazeChecker()
    reward_weights = [1.0]
    reward_functions = [MazeReward(robot_name="h1")]
