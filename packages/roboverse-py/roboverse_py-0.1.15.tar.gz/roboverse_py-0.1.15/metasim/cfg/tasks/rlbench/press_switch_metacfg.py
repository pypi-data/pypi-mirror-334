from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PressSwitchMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/press_switch/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="switch_main",
            usd_path="roboverse_data/assets/rlbench/press_switch/switch_main/usd/switch_main.usd",
        ),
        RigidObjMetaCfg(
            name="task_wall",
            usd_path="roboverse_data/assets/rlbench/press_switch/task_wall/usd/task_wall.usd",
            physics=PhysicStateType.GEOM,
        ),
    ]
    # TODO: add checker
