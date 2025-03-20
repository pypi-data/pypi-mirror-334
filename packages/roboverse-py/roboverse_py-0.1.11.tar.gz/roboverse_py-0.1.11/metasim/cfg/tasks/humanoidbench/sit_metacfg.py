from __future__ import annotations

import torch

from metasim.cfg.checkers import SitChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.types import EnvState
from metasim.utils import configclass

from .base_locomotion_env import HumanoidTaskMetaCfg


class SitReward:
    def __init__(self, robot_name="h1"):
        self.robot_name = robot_name

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        return torch.zeros(len(states))


@configclass
class SitMetaCfg(HumanoidTaskMetaCfg):
    episode_length = 1000
    objects = [
        RigidObjMetaCfg(
            name="sit",
            mjcf_path="roboverse_data/assets/humanoidbench/sit/chair/mjcf/chair.xml",
            physics=PhysicStateType.GEOM,
            fix_base_link=True,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/humanoidbench/sit/v2/initial_state_v2.json"
    checker = SitChecker()
    reward_weights = [1.0]
    reward_functions = [SitReward]
