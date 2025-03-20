from metasim.cfg.objects import PrimitiveCubeMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PlaceShapeInShapeSorterMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/place_shape_in_shape_sorter/v2"
    objects = [
        RigidObjMetaCfg(
            name="shape_sorter",
            physics=PhysicStateType.RIGIDBODY,
            usd_path="roboverse_data/assets/rlbench/place_shape_in_shape_sorter/shape_sorter/usd/shape_sorter.usd",
        ),
        RigidObjMetaCfg(
            name="triangular_prism",
            physics=PhysicStateType.RIGIDBODY,
            usd_path="roboverse_data/assets/rlbench/pick_and_lift_small/triangular_prism/usd/triangular_prism.usd",  # reuse same asset
        ),
        RigidObjMetaCfg(
            name="star_visual",
            physics=PhysicStateType.XFORM,
            usd_path="roboverse_data/assets/rlbench/pick_and_lift_small/star_visual/usd/star_visual.usd",  # reuse same asset
        ),
        RigidObjMetaCfg(
            name="moon_visual",
            physics=PhysicStateType.XFORM,
            usd_path="roboverse_data/assets/rlbench/pick_and_lift_small/moon_visual/usd/moon_visual.usd",  # reuse same asset
        ),
        RigidObjMetaCfg(
            name="cylinder",
            physics=PhysicStateType.XFORM,
            usd_path="roboverse_data/assets/rlbench/pick_and_lift_small/cylinder/usd/cylinder.usd",  # reuse same asset
        ),
        PrimitiveCubeMetaCfg(
            name="cube",
            physics=PhysicStateType.RIGIDBODY,
            size=[0.02089, 0.02089, 0.02089],
            color=[0.0, 0.85, 1.0],
        ),
    ]
    # TODO: add checker
