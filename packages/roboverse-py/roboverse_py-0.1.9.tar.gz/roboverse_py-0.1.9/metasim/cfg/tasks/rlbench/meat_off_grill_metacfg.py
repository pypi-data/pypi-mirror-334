from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class MeatOffGrillMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/meat_off_grill/v2"
    objects = [
        RigidObjMetaCfg(
            name="grill_visual",
            filepath="roboverse_data/assets/rlbench/meat_off_grill/grill_visual/usd/grill_visual.usd",
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="chicken_visual",
            filepath="roboverse_data/assets/rlbench/meat_off_grill/chicken_visual/usd/chicken_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="steak_visual",
            filepath="roboverse_data/assets/rlbench/meat_off_grill/steak_visual/usd/steak_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
