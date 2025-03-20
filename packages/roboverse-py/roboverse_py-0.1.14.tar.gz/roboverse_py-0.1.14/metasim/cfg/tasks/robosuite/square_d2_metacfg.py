import math

from metasim.cfg.checkers import AndOp, DetectedChecker, Relative2DSphereDetector, RelativeBboxDetector
from metasim.cfg.objects import PrimitiveCubeMetaCfg, RigidObjMetaCfg
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass

from ..base_task_metacfg import BaseTaskMetaCfg


@configclass
class SquareD2MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.ROBOSUITE
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 200
    traj_filepath = "data_isaaclab/source_data/robosuite/square_d2/square_d2_v2.pkl"
    objects = [
        RigidObjMetaCfg(
            name="peg1",
            usd_path="data_isaaclab/assets/robosuite/square_d0/pegs_arena/peg1.usd",
            physics=PhysicStateType.XFORM,
        ),
        PrimitiveCubeMetaCfg(
            name="table",
            # texture = 'data_isaaclab/robosuite/textures/ceramic.png',
            size=[0.8, 0.8, 0.05],
            physics=PhysicStateType.GEOM,
            color=[1.0, 1.0, 1.0],
        ),
        RigidObjMetaCfg(
            name="SquareNut",
            usd_path="data_isaaclab/assets/robosuite/square_d0/square_nut/square_nut.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    checker = AndOp([
        DetectedChecker(
            obj_name="SquareNut",
            detector=RelativeBboxDetector(
                base_obj_name="peg1",
                relative_pos=[0.0, 0.0, 0.05],
                relative_quat=[1.0, 0.0, 0.0, 0.0],
                checker_lower=[-math.inf, -math.inf, -math.inf],
                checker_upper=[math.inf, math.inf, 0.0],
                debug_vis=True,
            ),
        ),
        DetectedChecker(
            obj_name="SquareNut",
            detector=Relative2DSphereDetector(
                base_obj_name="peg1",
                relative_pos=[0.0, 0.0, 0.05],
                aixs=[0, 1],
                radius=0.02,
            ),
        ),
    ])
