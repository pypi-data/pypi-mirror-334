from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class OpenWindowMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/open_window/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="window_main",
            usd_path="roboverse_data/assets/rlbench/open_window/window_main/usd/window_main.usd",
        ),
    ]
    # TODO: add checker
