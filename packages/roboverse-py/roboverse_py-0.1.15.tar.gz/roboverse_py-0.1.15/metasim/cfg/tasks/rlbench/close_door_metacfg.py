from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg

OBJECTS = [
    ArticulationObjMetaCfg(
        name="door_frame",
        usd_path="roboverse_data/assets/rlbench/close_door/door_frame/usd/door_frame.usd",
    ),
]


@configclass
class CloseDoorMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/close_door/v2"
    objects = OBJECTS
    # TODO: add checker


@configclass
class OpenDoorMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/open_door/v2"
    objects = OBJECTS
    # TODO: add checker
