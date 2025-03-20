from metasim.cfg.checkers import JointPosChecker
from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .metaworld_task_metacfg import MetaworldTaskMetaCfg


@configclass
class DrawerOpenMetaCfg(MetaworldTaskMetaCfg):
    episode_length = 500
    objects = [
        ArticulationObjMetaCfg(
            name="drawer",
            usd_path="roboverse_data/assets/metaworld/drawer_open/drawer/usd/drawer.usd",
            mjcf_path="data_isaaclab/assets_mujoco/metaworld/drawer.xml",
            fix_base_link=True,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/metaworld/drawer_open/v2/sawyer_v2.pkl.gz"

    checker = JointPosChecker(
        obj_name="drawer",
        joint_name="goal_slidey",
        mode="le",
        radian_threshold=-0.16,
    )
