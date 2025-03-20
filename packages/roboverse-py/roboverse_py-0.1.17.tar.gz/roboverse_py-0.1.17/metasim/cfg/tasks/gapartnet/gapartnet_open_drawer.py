import math

from metasim.cfg.checkers import JointPosChecker
from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .gapartnet_task_metacfg import GAPartNetTaskMetaCfg


@configclass
class GapartnetOpenDrawerMetaCfg(GAPartNetTaskMetaCfg):
    episode_length = 250
    objects = [
        ArticulationObjMetaCfg(
            name="cabinet",
            fix_base_link=True,
            urdf_path="roboverse_data/assets/gapartnet/45661/mobility_annotation_gapartnet.urdf",
            scale=0.4,
        ),
    ]
    traj_filepath = "metasim/cfg/tasks/gapartnet/open_drawer_45661_v2.json"
    checker = JointPosChecker(
        obj_name="cabinet",
        joint_name="joint_0",
        mode="ge",
        radian_threshold=30 / 180 * math.pi,
    )
