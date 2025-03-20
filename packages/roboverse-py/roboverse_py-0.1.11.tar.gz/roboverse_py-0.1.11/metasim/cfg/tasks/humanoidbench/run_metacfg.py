from metasim.cfg.checkers import RunChecker
from metasim.utils import configclass

from .base_locomotion_env import BaseLocomotionReward, HumanoidTaskMetaCfg


class RunReward(BaseLocomotionReward):
    _move_speed = 5
    success_bar = 700


@configclass
class RunMetaCfg(HumanoidTaskMetaCfg):
    episode_length = 1000
    traj_filepath = "roboverse_data/trajs/humanoidbench/run/v2/initial_state_v2.json"
    checker = RunChecker()
    reward_functions = [RunReward]
    reward_weights = [1.0]
