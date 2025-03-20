from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg

_PAWNS = [
    RigidObjMetaCfg(
        name=f"{color}_pawn_{idx}",
        usd_path=f"roboverse_data/assets/rlbench/setup_chess/{color}_pawn_a/usd/{color}_pawn_a.usd",  # reuse the same asset for all pawns
        physics=PhysicStateType.RIGIDBODY,
    )
    for color in ["white", "black"]
    for idx in "abcdefgh"
]

_KINGS_AND_QUEENS = [
    RigidObjMetaCfg(
        name=f"{color}_{piece}",
        usd_path=f"roboverse_data/assets/rlbench/setup_chess/{color}_{piece}/usd/{color}_{piece}.usd",
        physics=PhysicStateType.RIGIDBODY,
    )
    for color in ["white", "black"]
    for piece in ["king", "queen"]
]

_OTHER_PIECES = [
    RigidObjMetaCfg(
        name=f"{color}_{side}_{piece}",
        usd_path=f"roboverse_data/assets/rlbench/setup_chess/{color}_kingside_{piece}/usd/{color}_kingside_{piece}.usd",  # reuse the same asset for both sides
        physics=PhysicStateType.RIGIDBODY,
    )
    for color in ["white", "black"]
    for piece in ["rook", "knight", "bishop"]
    for side in ["kingside", "queenside"]
]

_CHESS_BOARD = RigidObjMetaCfg(
    name="chess_board_base_visual",
    usd_path="roboverse_data/assets/rlbench/setup_chess/chess_board_base_visual/usd/chess_board_base_visual.usd",
    physics=PhysicStateType.GEOM,
)


@configclass
class SetupChessMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/setup_chess/v2"
    objects = [_CHESS_BOARD] + _PAWNS + _KINGS_AND_QUEENS + _OTHER_PIECES
    # TODO: add checker
