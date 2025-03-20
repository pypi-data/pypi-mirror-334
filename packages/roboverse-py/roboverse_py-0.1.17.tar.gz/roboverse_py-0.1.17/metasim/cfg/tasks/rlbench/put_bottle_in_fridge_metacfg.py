from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PutBottleInFridgeMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/put_bottle_in_fridge/v2"
    objects = [
        RigidObjMetaCfg(
            name="bottle_visual",
            usd_path="roboverse_data/assets/rlbench/put_bottle_in_fridge/bottle_visual/usd/bottle_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        ArticulationObjMetaCfg(
            name="fridge_base",
            usd_path="roboverse_data/assets/rlbench/put_bottle_in_fridge/fridge_base/usd/fridge_base.usd",
        ),
    ]
    # TODO: add checker
