from metasim.cfg.objects import PrimitiveCubeMetaCfg, PrimitiveSphereMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class HitBallWithQueueMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 600
    traj_filepath = "roboverse_data/trajs/rlbench/hit_ball_with_queue/v2"
    objects = [
        RigidObjMetaCfg(
            name="queue",
            usd_path="roboverse_data/assets/rlbench/hit_ball_with_queue/queue/usd/queue.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        PrimitiveSphereMetaCfg(
            name="ball",
            physics=PhysicStateType.RIGIDBODY,
            color=[0.96, 0.96, 0.96],
            radius=0.01,
        ),
        PrimitiveCubeMetaCfg(
            name="hit_ball_with_queue_pocket",
            size=[0.0075, 0.08, 0.005],
            physics=PhysicStateType.GEOM,
            color=[0.54, 1.0, 0.51],
        ),
        PrimitiveCubeMetaCfg(
            name="hit_ball_with_queue_pocket0",
            size=[0.0075, 0.08, 0.005],
            physics=PhysicStateType.GEOM,
            color=[0.54, 1.0, 0.51],
        ),
        PrimitiveCubeMetaCfg(
            name="hit_ball_with_queue_pocket1",
            size=[0.0075, 0.04, 0.005],
            physics=PhysicStateType.GEOM,
            color=[0.54, 1.0, 0.51],
        ),
        PrimitiveCubeMetaCfg(
            name="hit_ball_with_queue_stopper1",
            size=[0.0004, 0.016, 0.0004],
            physics=PhysicStateType.GEOM,
            color=[0.85, 0.85, 1.00],
        ),
        PrimitiveCubeMetaCfg(
            name="hit_ball_with_queue_stopper2",
            size=[0.0004, 0.016, 0.0004],
            physics=PhysicStateType.GEOM,
            color=[0.85, 0.85, 1.00],
        ),
    ]
    # TODO: add checker
