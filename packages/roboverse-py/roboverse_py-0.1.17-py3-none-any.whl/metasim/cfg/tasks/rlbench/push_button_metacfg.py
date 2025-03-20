from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PushButtonMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/push_button/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="push_button_target",
            usd_path="roboverse_data/assets/rlbench/push_button/push_button_target/usd/push_button_target.usd",
        ),
    ]
    # TODO: add checker
