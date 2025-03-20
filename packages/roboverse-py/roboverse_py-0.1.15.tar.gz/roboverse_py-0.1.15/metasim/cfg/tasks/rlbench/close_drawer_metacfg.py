from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg

_OBJECTS = [
    ArticulationObjMetaCfg(
        name="drawer_frame",
        usd_path="roboverse_data/assets/rlbench/close_drawer/drawer_frame/usd/drawer_frame.usd",
    ),
]


@configclass
class CloseDrawerMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/close_drawer/v2"
    objects = _OBJECTS
    # TODO: add checker


@configclass
class OpenDrawerMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/open_drawer/v2"
    objects = _OBJECTS
    # TODO: add checker
