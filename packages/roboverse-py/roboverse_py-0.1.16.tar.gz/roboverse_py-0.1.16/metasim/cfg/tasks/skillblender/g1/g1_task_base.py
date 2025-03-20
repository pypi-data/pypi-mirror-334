from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.utils import configclass


@configclass
class G1BaseTaskMetaCfg(BaseTaskMetaCfg):
    episode_length = 250
    objects = []
    traj_filepath = "/home/haoran/Project/RoboVerse/RoboVerse/metasim/cfg/tasks/skillblender/g1/g1_example_v2.json"
