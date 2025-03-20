from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class EmptyDishwasherMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 600
    traj_filepath = "roboverse_data/trajs/rlbench/empty_dishwasher/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="dishwasher",
            usd_path="roboverse_data/assets/rlbench/empty_dishwasher/dishwasher/usd/dishwasher.usd",
        ),
        RigidObjMetaCfg(
            name="dishwasher_plate_visual",
            usd_path="roboverse_data/assets/rlbench/empty_dishwasher/dishwasher_plate_visual/usd/dishwasher_plate_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
