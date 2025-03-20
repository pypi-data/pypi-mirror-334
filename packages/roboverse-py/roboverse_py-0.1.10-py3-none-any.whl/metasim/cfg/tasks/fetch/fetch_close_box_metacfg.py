import math

from metasim.cfg.checkers import JointPosChecker
from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.cfg.tasks import BaseTaskMetaCfg
from metasim.utils import configclass


@configclass
class FetchCloseBoxMetaCfg(BaseTaskMetaCfg):
    episode_length = 250
    objects = [
        ArticulationObjMetaCfg(
            name="box_base",
            filepath="roboverse_data/assets/rlbench/close_box/box_base/usd/box_base.usd",
            urdf_path="roboverse_data/assets/rlbench/close_box/box_base/urdf/box_base_unique.urdf",
            mjcf_path="roboverse_data/assets/rlbench/close_box/box_base/mjcf/box_base_unique.mjcf",
        ),
    ]
    traj_filepath = "metasim/cfg/tasks/fetch/fetch_example_v2.json"
    checker = JointPosChecker(
        obj_name="box_base",
        joint_name="box_joint",
        mode="le",
        radian_threshold=-14 / 180 * math.pi,
    )
