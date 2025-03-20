from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class ChangeClockMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/change_clock/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="clock",
            usd_path="roboverse_data/assets/rlbench/change_clock/clock/usd/clock.usd",
        ),
    ]
    # TODO: add checker
