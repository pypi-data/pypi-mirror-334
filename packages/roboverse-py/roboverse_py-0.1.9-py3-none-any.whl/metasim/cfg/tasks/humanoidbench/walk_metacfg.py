from metasim.cfg.checkers import WalkChecker
from metasim.utils import configclass

from .base_locomotion_env import BaseLocomotionReward, HumanoidTaskMetaCfg


class WalkReward(BaseLocomotionReward):
    _move_speed = 1
    success_bar = 700


@configclass
class WalkMetaCfg(HumanoidTaskMetaCfg):
    episode_length = 1000
    # traj_filepath = "roboverse_data/trajs/humanoidbench/walk/v2/h1_v2.pkl"
    traj_filepath = "roboverse_data/trajs/humanoidbench/walk/v2/initial_state_v2.json"
    checker = WalkChecker()
    reward_functions = [WalkReward]
    reward_weights = [1.0]
