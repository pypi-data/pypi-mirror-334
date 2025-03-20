from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PushButtonsMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 500
    traj_filepath = "roboverse_data/trajs/rlbench/push_buttons/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="push_buttons_target0",
            usd_path="roboverse_data/assets/rlbench/push_buttons/push_buttons_target0/usd/push_buttons_target0.usd",
        ),
        ArticulationObjMetaCfg(
            name="push_buttons_target1",
            usd_path="roboverse_data/assets/rlbench/push_buttons/push_buttons_target1/usd/push_buttons_target1.usd",
        ),
        ArticulationObjMetaCfg(
            name="push_buttons_target2",
            usd_path="roboverse_data/assets/rlbench/push_buttons/push_buttons_target2/usd/push_buttons_target2.usd",
        ),
    ]
    # TODO: add checker
