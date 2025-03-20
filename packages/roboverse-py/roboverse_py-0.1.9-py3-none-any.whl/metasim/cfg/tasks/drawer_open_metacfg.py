from metasim.cfg.checkers import JointPosChecker
from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.utils import configclass

from .base_task_metacfg import BaseTaskMetaCfg


@configclass
class DrawerOpenMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.METAWORLD
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 500
    objects = [
        ArticulationObjMetaCfg(
            name="drawer",
            filepath="data_isaaclab/assets/metaworld/drawer_open/drawer.usd",
            mjcf_path="data_isaaclab/assets_mujoco/metaworld/drawer.xml",
            fix_base_link=True,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/metaworld/rigid_body/drawer_open_v2.pkl"

    checker = JointPosChecker(
        obj_name="drawer",
        joint_name="goal_slidey",
        mode="le",
        radian_threshold=-0.16,
    )
