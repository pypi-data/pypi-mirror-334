from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg

_OBJECTS = [
    RigidObjMetaCfg(
        name="lamp_base",
        usd_path="roboverse_data/assets/rlbench/lamp_off/lamp_base/usd/lamp_base.usd",
        physics=PhysicStateType.GEOM,
    ),
    ArticulationObjMetaCfg(
        name="push_button_target",
        usd_path="roboverse_data/assets/rlbench/lamp_off/push_button_target/usd/push_button_target.usd",
    ),
]


@configclass
class LampOffMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/lamp_off/v2"
    objects = _OBJECTS
    # TODO: add checker


@configclass
class LampOnMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/lamp_on/v2"
    objects = _OBJECTS
    # TODO: add checker
