import math

import torch
from loguru import logger as log

from metasim.cfg.checkers import JointPosChecker
from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class CloseBoxMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 250
    objects = [
        ArticulationObjMetaCfg(
            name="box_base",
            fix_base_link=True,
            usd_path="metasim/data/quick_start/assets/rlbench/close_box/box_base/usd/box_base.usd",
            urdf_path="metasim/data/quick_start/assets/rlbench/close_box/box_base/urdf/box_base_unique.urdf",
            mjcf_path="metasim/data/quick_start/assets/rlbench/close_box/box_base/mjcf/box_base_unique.mjcf",
        ),
    ]
    traj_filepath = "metasim/data/quick_start/trajs/rlbench/close_box/v2"
    checker = JointPosChecker(
        obj_name="box_base",
        joint_name="box_joint",
        mode="le",
        radian_threshold=-14 / 180 * math.pi,
    )

    def reward_fn(self, states):
        # HACK: metasim_body_panda_hand may not be universal across all robots
        try:
            ee_poses = torch.stack([state["metasim_body_panda_hand"]["pos"] for state in states])
        except KeyError as e:
            log.error(f"KeyError: {e}")
            ee_poses = torch.zeros(len(states), 3)
        distance = torch.norm(ee_poses, dim=-1)
        return -distance
