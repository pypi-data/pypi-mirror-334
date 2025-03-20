from metasim.cfg.objects import ArticulationObjMetaCfg, PrimitiveCubeMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PutItemInDrawerMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/put_item_in_drawer/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="drawer_frame",
            usd_path="roboverse_data/assets/rlbench/put_item_in_drawer/drawer_frame/usd/drawer_frame.usd",
        ),
        PrimitiveCubeMetaCfg(
            name="item",
            size=[0.04, 0.04, 0.04],
            color=[0.85, 0.85, 1.0],
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
