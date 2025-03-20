from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class LampOnMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/lamp_on/v2"
    objects = [
        RigidObjMetaCfg(
            name="lamp_base",
            filepath="roboverse_data/assets/rlbench/lamp_off/lamp_base/usd/lamp_base.usd",  # reuse lamp_off assets
            physics=PhysicStateType.GEOM,
        ),
        ArticulationObjMetaCfg(
            name="push_button_target",
            filepath="roboverse_data/assets/rlbench/lamp_off/push_button_target/usd/push_button_target.usd",  # reuse lamp_off assets
        ),
    ]
    # TODO: add checker
