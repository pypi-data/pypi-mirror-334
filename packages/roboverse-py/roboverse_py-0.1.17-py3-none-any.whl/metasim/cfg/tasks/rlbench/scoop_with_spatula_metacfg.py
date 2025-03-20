from metasim.cfg.objects import PrimitiveCubeMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class ScoopWithSpatulaMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/scoop_with_spatula/v2"
    objects = [
        RigidObjMetaCfg(
            name="spatula_visual",
            usd_path="roboverse_data/assets/rlbench/scoop_with_spatula/spatula_visual/usd/spatula_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        PrimitiveCubeMetaCfg(
            name="Cuboid",
            size=[0.02, 0.02, 0.02],
            color=[0.85, 0.85, 1.0],
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
