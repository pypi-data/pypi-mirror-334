from metasim.cfg.objects import PrimitiveSphereMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class ReachTargetMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/reach_target/v2"
    objects = [
        PrimitiveSphereMetaCfg(
            name="target",
            radius=0.025,
            color=[1.0, 0.0, 0.0],
            physics=PhysicStateType.XFORM,
        ),
        PrimitiveSphereMetaCfg(
            name="distractor0",
            radius=0.025,
            color=[1.0, 0.0, 0.5],
            physics=PhysicStateType.XFORM,
        ),
        PrimitiveSphereMetaCfg(
            name="distractor1",
            radius=0.025,
            color=[1.0, 1.0, 0.0],
            physics=PhysicStateType.XFORM,
        ),
    ]
    # TODO: add checker
