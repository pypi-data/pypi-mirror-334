from metasim.cfg.checkers import DetectedChecker, Relative3DSphereDetector
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .metaworld_task_metacfg import MetaworldTaskMetaCfg


@configclass
class BinPickMetaCfg(MetaworldTaskMetaCfg):
    episode_length = 500
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="data_isaaclab/assets/metaworld/bin_pick/obj.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="binA",
            usd_path="data_isaaclab/assets/metaworld/bin_pick/binA.usd",
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="binB",
            usd_path="data_isaaclab/assets/metaworld/bin_pick/binB.usd",
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
