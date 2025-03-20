from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg

_OBJECTS = [
    ArticulationObjMetaCfg(
        name="microwave_frame_resp",
        usd_path="roboverse_data/assets/rlbench/close_microwave/microwave_frame_resp/usd/microwave_frame_resp.usd",
    ),
]


@configclass
class CloseMicrowaveMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/close_microwave/v2"
    objects = _OBJECTS
    # TODO: add checker


@configclass
class OpenMicrowaveMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/open_microwave/v2"
    objects = _OBJECTS
    # TODO: add checker
