from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class OpenWineBottleMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/open_wine_bottle/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="bottle",
            usd_path="roboverse_data/assets/rlbench/open_wine_bottle/bottle/usd/bottle.usd",
        ),
    ]
    # TODO: add checker
