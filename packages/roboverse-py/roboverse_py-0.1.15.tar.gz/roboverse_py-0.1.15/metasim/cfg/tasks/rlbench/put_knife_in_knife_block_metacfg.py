from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg

_OBJECTS = [
    RigidObjMetaCfg(
        name="chopping_board_visual",
        usd_path="roboverse_data/assets/rlbench/put_knife_in_knife_block/chopping_board_visual/usd/chopping_board_visual.usd",
        physics=PhysicStateType.RIGIDBODY,
    ),
    RigidObjMetaCfg(
        name="knife_block_visual",
        usd_path="roboverse_data/assets/rlbench/put_knife_in_knife_block/knife_block_visual/usd/knife_block_visual.usd",
        physics=PhysicStateType.GEOM,
    ),
    RigidObjMetaCfg(
        name="knife_visual",
        usd_path="roboverse_data/assets/rlbench/put_knife_in_knife_block/knife_visual/usd/knife_visual.usd",
        physics=PhysicStateType.RIGIDBODY,
    ),
]


@configclass
class PutKnifeInKnifeBlockMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/put_knife_in_knife_block/v2"
    objects = _OBJECTS
    # TODO: add checker


@configclass
class PutKnifeOnChoppingBoardMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/put_knife_on_chopping_board/v2"
    objects = _OBJECTS
    # TODO: add checker
