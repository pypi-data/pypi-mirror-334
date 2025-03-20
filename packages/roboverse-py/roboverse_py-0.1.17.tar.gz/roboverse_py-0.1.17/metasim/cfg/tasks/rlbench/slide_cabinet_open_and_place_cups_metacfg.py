from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg

_CABINET = ArticulationObjMetaCfg(
    name="cabinet_base",
    usd_path="roboverse_data/assets/rlbench/slide_cabinet_open_and_place_cups/cabinet_base/usd/cabinet_base.usd",
)

_CUP = RigidObjMetaCfg(
    name="cup_visual",
    usd_path="roboverse_data/assets/rlbench/slide_cabinet_open_and_place_cups/cup_visual/usd/cup_visual.usd",
    physics=PhysicStateType.RIGIDBODY,
)


@configclass
class SlideCabinetOpenAndPlaceCupsMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/slide_cabinet_open_and_place_cups/v2"
    objects = [_CABINET, _CUP]
    # TODO: add checker


@configclass
class TakeCupOutFromCabinetMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/take_cup_out_from_cabinet/v2"
    objects = [_CABINET, _CUP]
    # TODO: add checker
