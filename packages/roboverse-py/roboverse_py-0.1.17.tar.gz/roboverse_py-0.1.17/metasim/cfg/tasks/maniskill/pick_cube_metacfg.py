## TODO:
## 1. The checker is not same as the original one
##    The original one checks if the cube is near the given target position
##    The current one checks if the cube is lifted up 0.1 meters

from metasim.cfg.checkers import PositionShiftChecker
from metasim.cfg.objects import PrimitiveCubeMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .maniskill_task_metacfg import ManiskillTaskMetaCfg


@configclass
class PickCubeMetaCfg(ManiskillTaskMetaCfg):
    """ManiSkill pick_cube task, migrated from https://github.com/haosulab/ManiSkill/blob/main/mani_skill/envs/tasks/tabletop/pick_cube.py"""

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
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_cube/trajectory-unified-retarget_v2.pkl"
    checker = PositionShiftChecker(
        obj_name="cube",
        distance=0.1,
        axis="z",
    )
