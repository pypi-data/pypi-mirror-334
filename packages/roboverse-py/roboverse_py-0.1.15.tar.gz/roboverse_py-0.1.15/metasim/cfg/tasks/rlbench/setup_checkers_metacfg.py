from metasim.cfg.objects import PrimitiveCylinderMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg
from .setup_chess_metacfg import _CHESS_BOARD

_WHITE_CHECKERS = [
    PrimitiveCylinderMetaCfg(
        name=f"checker{idx}",
        radius=0.017945,
        height=0.00718,
        color=[1.0, 1.0, 1.0],
        physics=PhysicStateType.RIGIDBODY,
    )
    for idx in range(12)
]

_RED_CHECKERS = [
    PrimitiveCylinderMetaCfg(
        name=f"checker{idx}",
        radius=0.017945,
        height=0.00718,
        color=[1.0, 0.0, 0.0],
        physics=PhysicStateType.RIGIDBODY,
    )
    for idx in range(12, 24)
]


@configclass
class SetupCheckersMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/setup_checkers/v2"
    objects = [_CHESS_BOARD] + _WHITE_CHECKERS + _RED_CHECKERS
    # TODO: add checker
