from metasim.cfg.checkers import DetectedChecker, Relative3DSphereDetector
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass

from .base_task_metacfg import BaseTaskMetaCfg


@configclass
class BinPickMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.METAWORLD
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 500
    objects = [
        RigidObjMetaCfg(
            name="obj",
            filepath="data_isaaclab/assets/metaworld/bin_pick/obj.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="binA",
            filepath="data_isaaclab/assets/metaworld/bin_pick/binA.usd",
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="binB",
            filepath="data_isaaclab/assets/metaworld/bin_pick/binB.usd",
            physics=PhysicStateType.GEOM,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/metaworld/rigid_body/bin_pick_v2.pkl"
    checker = DetectedChecker(
        obj_name="obj",
        detector=Relative3DSphereDetector(
            base_obj_name="binB",
            relative_pos=[0.0, 0.0, 0.0],
            radius=0.05,
        ),
    )
