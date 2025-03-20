from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PickUpCupMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/pick_up_cup/v2"
    objects = [
        RigidObjMetaCfg(
            name="cup1_visual",
            usd_path="roboverse_data/assets/rlbench/pick_up_cup/cup1_visual/usd/cup1_visual.usd",
            physics=PhysicStateType.XFORM,
        ),
        RigidObjMetaCfg(
            name="cup2_visual",
            usd_path="roboverse_data/assets/rlbench/pick_up_cup/cup2_visual/usd/cup2_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
