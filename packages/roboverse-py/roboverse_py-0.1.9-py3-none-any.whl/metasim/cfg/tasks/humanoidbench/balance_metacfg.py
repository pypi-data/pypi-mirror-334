from metasim.utils import configclass

from .base_locomotion_env import HumanoidTaskMetaCfg


@configclass
class BalanceMetaCfg(HumanoidTaskMetaCfg):
    episode_length = 1000
