from metasim.cfg.checkers import JointPosChecker
from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass

from .base_task_metacfg import BaseTaskMetaCfg


@configclass
class HammerMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.METAWORLD
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 500
    objects = [
        RigidObjMetaCfg(
            name="hammer",
            filepath="data_isaaclab/assets/metaworld/hammer/hammer.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        ArticulationObjMetaCfg(
            name="hammer_block",
            filepath="data_isaaclab/assets/metaworld/hammer/hammer_block.usd",
            # physics=PhysicStateType.GEOM,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/metaworld/rigid_body/hammer_v2.pkl"
    checker = JointPosChecker(
        obj_name="hammer_block",
        joint_name="NailSlideJoint",
        mode="ge",
        radian_threshold=0.09,
    )
