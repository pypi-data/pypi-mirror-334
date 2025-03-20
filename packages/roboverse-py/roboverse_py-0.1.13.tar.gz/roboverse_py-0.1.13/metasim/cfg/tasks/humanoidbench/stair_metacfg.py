from __future__ import annotations

import torch
from dm_control.utils import rewards

from metasim.cfg.checkers import StairChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.types import EnvState
from metasim.utils import configclass
from metasim.utils.h1_utils import (
    actuator_forces,
    center_of_mass_velocity,
    head_height,
    left_foot_height,
    right_foot_height,
    torso_upright,
)

from .base_locomotion_env import (
    _G1_CRAWL_HEIGHT,
    _G1_STAND_HEIGHT,
    _H1_CRAWL_HEIGHT,
    _H1_STAND_HEIGHT,
    HumanoidTaskMetaCfg,
)


class StairReward:
    def __init__(self, robot_name="h1"):
        self._robot_name = robot_name
        if robot_name == "h1" or robot_name == "h1_simple_hand":
            self._stand_height = _H1_STAND_HEIGHT
            self._crawl_height = _H1_CRAWL_HEIGHT
        elif robot_name == "g1":
            self._stand_height = _G1_STAND_HEIGHT
            self._crawl_height = _G1_CRAWL_HEIGHT
        else:
            raise ValueError(f"Unknown robot {robot_name}")

    def __call__(self, states: list[EnvState]) -> torch.FloatTensor:
        results = []
        for state in states:
            # Reward for controlled movement
            small_control = rewards.tolerance(
                actuator_forces(state, self._robot_name),
                margin=10,
                value_at_margin=0,
                sigmoid="quadratic",
            ).mean()
            small_control = (4 + small_control) / 5

            # Reward for sliding motion - encourage horizontal velocity
            root_x_speed = rewards.tolerance(
                center_of_mass_velocity(state, self._robot_name)[0],  # x-axis velocity
                bounds=(1.0, float("inf")),  # Adjust velocity threshold as needed
                margin=1.0,
                value_at_margin=0,
                sigmoid="linear",
            )

            # Reward for maintaining upright posture
            upright = rewards.tolerance(
                torso_upright(state, self._robot_name),
                bounds=(0.5, 1.0),
                sigmoid="linear",
                margin=1.9,
                value_at_margin=0,
            )

            # Left foot vertical distance
            head_z = head_height(state, self._robot_name)
            left_foot_z = left_foot_height(state, self._robot_name)
            right_foot_z = right_foot_height(state, self._robot_name)
            vertical_foot_left = rewards.tolerance(
                head_z - left_foot_z,
                bounds=(1.2, float("inf")),
                margin=0.45,
            )
            vertical_foot_right = rewards.tolerance(
                head_z - right_foot_z,
                bounds=(1.2, float("inf")),
                margin=0.45,
            )

            # Combine rewards
            reward = small_control * root_x_speed * upright * vertical_foot_left * vertical_foot_right

            # log.info(f"root_x_speed: {root_x_speed}, upright: {upright}, vertical_foot_left: {vertical_foot_left}, vertical_foot_right: {vertical_foot_right}")
            results.append(reward)
        return torch.tensor(results)


@configclass
class StairMetaCfg(HumanoidTaskMetaCfg):
    episode_length = 1000
    objects = [
        RigidObjMetaCfg(
            name="stair",
            mjcf_path="roboverse_data/assets/humanoidbench/stair/floor/mjcf/floor.xml",
            physics=PhysicStateType.GEOM,
            fix_base_link=True,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/humanoidbench/stair/v2/initial_state_v2.json"
    checker = StairChecker()
    reward_weights = [1.0]
    reward_functions = [StairReward]
