from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.utils import configclass


@configclass
class H1BaseTaskMetaCfg(BaseTaskMetaCfg):
    episode_length = 250
    objects = []
    traj_filepath = "/home/haoran/Project/RoboVerse/RoboVerse/metasim/cfg/tasks/skillblender/h1/h1_example_v2.json"
