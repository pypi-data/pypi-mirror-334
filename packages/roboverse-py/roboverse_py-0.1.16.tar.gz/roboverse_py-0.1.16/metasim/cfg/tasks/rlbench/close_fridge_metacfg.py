from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg

_OBJECTS = [
    ArticulationObjMetaCfg(
        name="fridge_base",
        usd_path="roboverse_data/assets/rlbench/close_fridge/fridge_base/usd/fridge_base.usd",
    ),
]


@configclass
class CloseFridgeMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/close_fridge/v2"
    objects = _OBJECTS
    # TODO: add checker


@configclass
class OpenFridgeMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/open_fridge/v2"
    objects = _OBJECTS
    # TODO: add checker
