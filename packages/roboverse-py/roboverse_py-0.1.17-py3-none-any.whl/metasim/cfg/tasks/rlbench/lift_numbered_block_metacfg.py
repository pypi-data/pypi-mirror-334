from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class LiftNumberedBlockMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/lift_numbered_block/v2"
    objects = [
        RigidObjMetaCfg(
            name="block1",
            usd_path="roboverse_data/assets/rlbench/lift_numbered_block/block1/usd/block1.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="block2",
            usd_path="roboverse_data/assets/rlbench/lift_numbered_block/block2/usd/block2.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="block3",
            usd_path="roboverse_data/assets/rlbench/lift_numbered_block/block3/usd/block3.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
