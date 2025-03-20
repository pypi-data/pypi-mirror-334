from metasim.cfg.checkers import StandChecker
from metasim.utils import configclass

from .base_locomotion_env import BaseLocomotionReward, HumanoidTaskMetaCfg


class StandReward(BaseLocomotionReward):
    _move_speed = 0
    success_bar = 800


@configclass
class StandMetaCfg(HumanoidTaskMetaCfg):
    episode_length = 1000
    # traj_filepath = "roboverse_data/trajs/humanoidbench/stand/v2/h1_v2.pkl"
    traj_filepath = "roboverse_data/trajs/humanoidbench/stand/v2/initial_state_v2.json"
    checker = StandChecker()
    reward_weights = [1.0]
    reward_functions = [StandReward]
