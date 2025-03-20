from metasim.cfg.objects import PrimitiveCubeMetaCfg, PrimitiveSphereMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PickAndLiftSmallMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/pick_and_lift_small/v2"
    objects = [
        RigidObjMetaCfg(
            name="triangular_prism",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/rlbench/pick_and_lift_small/triangular_prism/usd/triangular_prism.usd",
        ),
        RigidObjMetaCfg(
            name="star_visual",
            physics=PhysicStateType.XFORM,
            filepath="roboverse_data/assets/rlbench/pick_and_lift_small/star_visual/usd/star_visual.usd",
        ),
        RigidObjMetaCfg(
            name="moon_visual",
            physics=PhysicStateType.XFORM,
            filepath="roboverse_data/assets/rlbench/pick_and_lift_small/moon_visual/usd/moon_visual.usd",
        ),
        RigidObjMetaCfg(
            name="cylinder",
            physics=PhysicStateType.XFORM,
            filepath="roboverse_data/assets/rlbench/pick_and_lift_small/cylinder/usd/cylinder.usd",
        ),
        PrimitiveCubeMetaCfg(
            name="cube",
            physics=PhysicStateType.RIGIDBODY,
            size=[0.02089, 0.02089, 0.02089],
            color=[0.0, 0.85, 1.0],
        ),
        PrimitiveSphereMetaCfg(
            name="success_visual",
            physics=PhysicStateType.XFORM,
            color=[1.0, 0.14, 0.14],
            radius=0.04,
        ),
    ]
    # TODO: add checker
