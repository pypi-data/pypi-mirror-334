import math

from metasim.cfg.checkers import (
    AndOp,
    DetectedChecker,
    Relative2DSphereDetector,
    RelativeBboxDetector,
)
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .metaworld_task_metacfg import MetaworldTaskMetaCfg


@configclass
class AssemblyMetaCfg(MetaworldTaskMetaCfg):
    episode_length = 500
    objects = [
        RigidObjMetaCfg(
            name="round_nut",
            usd_path="data_isaaclab/assets/metaworld/assembly/round_nut.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="peg",
            usd_path="data_isaaclab/assets/metaworld/assembly/peg.usd",
            physics=PhysicStateType.GEOM,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/metaworld/rigid_body/assembly_v2.pkl"
    checker = AndOp([
        DetectedChecker(
            obj_name="RoundNut",
            detector=RelativeBboxDetector(
                base_obj_name="peg",
                relative_pos=[0.0, 0.0, 0.05],
                relative_quat=[1.0, 0.0, 0.0, 0.0],
                checker_lower=[-math.inf, -math.inf, -math.inf],
                checker_upper=[math.inf, math.inf, 0.0],
                debug_vis=True,
            ),
        ),
        DetectedChecker(
            obj_name="RoundNut",
            detector=Relative2DSphereDetector(
                base_obj_name="peg",
                relative_pos=[0.0, 0.0, 0.05],
                aixs=[0, 1],
                radius=0.02,
            ),
        ),
    ])
