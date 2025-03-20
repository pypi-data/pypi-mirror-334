from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg

_OVEN = ArticulationObjMetaCfg(
    name="oven_base",
    usd_path="roboverse_data/assets/rlbench/open_oven/oven_base/usd/oven_base.usd",
)
_TRAY = RigidObjMetaCfg(
    name="tray_visual",
    usd_path="roboverse_data/assets/rlbench/put_tray_in_oven/tray_visual/usd/tray_visual.usd",
    physics=PhysicStateType.RIGIDBODY,
)


@configclass
class OpenOvenMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/open_oven/v2"
    objects = [_OVEN]
    # TODO: add checker


@configclass
class PutTrayInOvenMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/put_tray_in_oven/v2"
    objects = [_OVEN, _TRAY]
    # TODO: add checker


@configclass
class TakeTrayOutOfOvenMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/take_tray_out_of_oven/v2"
    objects = [_OVEN, _TRAY]
    # TODO: add checker
