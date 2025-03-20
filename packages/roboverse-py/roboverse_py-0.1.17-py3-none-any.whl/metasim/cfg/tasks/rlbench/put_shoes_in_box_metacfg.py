from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PutShoesInBoxMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 600
    traj_filepath = "roboverse_data/trajs/rlbench/put_shoes_in_box/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="box_base",
            usd_path="roboverse_data/assets/rlbench/put_shoes_in_box/box_base/usd/box_base.usd",
        ),
        RigidObjMetaCfg(
            name="shoe1_visual",
            usd_path="roboverse_data/assets/rlbench/put_shoes_in_box/shoe1_visual/usd/shoe1_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="shoe2_visual",
            usd_path="roboverse_data/assets/rlbench/put_shoes_in_box/shoe2_visual/usd/shoe2_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
