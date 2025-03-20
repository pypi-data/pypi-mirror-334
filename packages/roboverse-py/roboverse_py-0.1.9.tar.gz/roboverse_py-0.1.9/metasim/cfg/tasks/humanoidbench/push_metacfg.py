from __future__ import annotations

import torch

from metasim.cfg.checkers import PushChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.types import EnvState
from metasim.utils import configclass
from metasim.utils.h1_utils import left_hand_position

from .base_locomotion_env import HumanoidTaskMetaCfg


class SuccessReward:
    def __init__(self, robot_name="h1_simple_hand"):
        self._robot_name = robot_name
        if robot_name != "h1" and robot_name != "h1_simple_hand":
            raise ValueError(f"Unknown robot {robot_name} without hand")

    def __call__(self, states: list[EnvState]) -> float:
        state = states[0]
        box_pos = state["object"]["pos"]
        dest_pos = state["destination"]["pos"]
        dgoal = torch.norm(box_pos - dest_pos)
        return float(dgoal < 0.05)


class GoalDistanceReward:
    def __init__(self, robot_name="h1_simple_hand"):
        self._robot_name = robot_name

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        state = states[0]
        box_pos = state["object"]["pos"]
        dest_pos = state["destination"]["pos"]
        return -torch.norm(box_pos - dest_pos)


class HandDistanceReward:
    def __init__(self, robot_name="h1_simple_hand"):
        self._robot_name = robot_name
        if robot_name != "h1" and robot_name != "h1_simple_hand":
            raise ValueError(f"Unknown robot {robot_name} without hand")

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        state = states[0]
        box_pos = state["object"]["pos"]
        left_hand_pos = left_hand_position(state, self._robot_name)
        return -torch.norm(box_pos - left_hand_pos)


@configclass
class PushMetaCfg(HumanoidTaskMetaCfg):
    episode_length = 500  # Updated to match the specification
    objects = [
        RigidObjMetaCfg(
            name="table",
            mjcf_path="roboverse_data/assets/humanoidbench/push/table/mjcf/table.xml",
            physics=PhysicStateType.GEOM,
            fix_base_link=True,
        ),
        RigidObjMetaCfg(
            name="object",
            mjcf_path="roboverse_data/assets/humanoidbench/push/object/mjcf/object.xml",
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="destination",
            mjcf_path="roboverse_data/assets/humanoidbench/push/destination/mjcf/destination.xml",
            physics=PhysicStateType.GEOM,
            fix_base_link=True,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/humanoidbench/push/v2/initial_state_v2.json"
    checker = PushChecker()
    reward_weights = [1000, 1, 0.1]  # αs, αt, αh
    reward_functions = [SuccessReward, GoalDistanceReward, HandDistanceReward]
