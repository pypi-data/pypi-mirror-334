from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class CloseGrillMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/close_grill/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="grill",
            usd_path="roboverse_data/assets/rlbench/close_grill/grill/usd/grill.usd",
        ),
    ]
    # TODO: add checker
