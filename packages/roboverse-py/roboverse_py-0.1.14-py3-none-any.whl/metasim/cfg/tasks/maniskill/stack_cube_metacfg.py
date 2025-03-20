from metasim.cfg.checkers import DetectedChecker, RelativeBboxDetector
from metasim.cfg.objects import PrimitiveCubeMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .maniskill_task_metacfg import ManiskillTaskMetaCfg


@configclass
class StackCubeMetaCfg(ManiskillTaskMetaCfg):
    """ManiSkill stack_cube task, migrated from https://github.com/haosulab/ManiSkill/blob/main/mani_skill/envs/tasks/tabletop/stack_cube.py"""

    episode_length = 250
    objects = [
        PrimitiveCubeMetaCfg(
            name="cube",
            size=[0.04, 0.04, 0.04],
            mass=0.02,
            physics=PhysicStateType.RIGIDBODY,
            color=[1.0, 0.0, 0.0],
            mjcf_path="roboverse_data/assets/maniskill/cube/cube.mjcf",
        ),
        PrimitiveCubeMetaCfg(
            name="base",
            size=[0.04, 0.04, 0.04],
            mass=0.02,
            physics=PhysicStateType.RIGIDBODY,
            color=[0.0, 0.0, 1.0],
            mjcf_path="roboverse_data/assets/maniskill/cube/base.mjcf",
        ),
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/stack_cube/v2"

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
