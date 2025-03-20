from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class GetIceFromFridgeMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 600
    traj_filepath = "roboverse_data/trajs/rlbench/get_ice_from_fridge/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="fridge_base",
            filepath="roboverse_data/assets/rlbench/get_ice_from_fridge/fridge_base/usd/fridge_base.usd",
        ),
        RigidObjMetaCfg(
            name="cup_visual",
            filepath="roboverse_data/assets/rlbench/get_ice_from_fridge/cup_visual/usd/cup_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
