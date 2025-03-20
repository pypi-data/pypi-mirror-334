from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class BeatTheBuzzMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/beat_the_buzz/v2"
    objects = [
        RigidObjMetaCfg(
            name="wand",
            usd_path="roboverse_data/assets/rlbench/beat_the_buzz/wand/usd/wand.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid",
            usd_path="roboverse_data/assets/rlbench/beat_the_buzz/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.GEOM,
        ),
    ]
    # TODO: add checker
