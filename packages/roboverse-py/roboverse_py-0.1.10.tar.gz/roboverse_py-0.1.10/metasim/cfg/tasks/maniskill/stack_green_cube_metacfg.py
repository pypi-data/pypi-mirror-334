from metasim.cfg.checkers import DetectedChecker, RelativeBboxDetector
from metasim.cfg.objects import (
    PrimitiveCubeMetaCfg,
)
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .maniskill_task_metacfg import ManiskillTaskMetaCfg


@configclass
class StackGreenCubeMetaCfg(ManiskillTaskMetaCfg):
    episode_length = 250
    objects = [
        PrimitiveCubeMetaCfg(
            name="cube",
            size=[0.04, 0.04, 0.04],
            mass=0.02,
            physics=PhysicStateType.RIGIDBODY,
            color=[0.0, 1.0, 0.0],
            mjcf_path="data_isaaclab/assets_mujoco/maniskill2/stack_cube/cube.mjcf",
        ),
        PrimitiveCubeMetaCfg(
            name="base",
            size=[0.04, 0.04, 0.04],
            mass=0.02,
            physics=PhysicStateType.RIGIDBODY,
            color=[0.0, 0.0, 1.0],
            mjcf_path="data_isaaclab/assets_mujoco/maniskill2/stack_cube/base.mjcf",
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/maniskill2/rigid_body/StackCube-v0/trajectory-unified_v2.pkl"

    ## TODO: detect velocity
    checker = DetectedChecker(
        obj_name="cube",
        detector=RelativeBboxDetector(
            base_obj_name="base",
            relative_pos=(0.0, 0.0, 0.04),
            relative_quat=(1.0, 0.0, 0.0, 0.0),
            checker_lower=(-0.02, -0.02, -0.02),
            checker_upper=(0.02, 0.02, 0.02),
            ignore_base_ori=True,
        ),
    )
