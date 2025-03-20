from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PlaceCupsMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/place_cups/v2"
    objects = [
        RigidObjMetaCfg(
            name="place_cups_holder_base",
            filepath="roboverse_data/assets/rlbench/place_cups/place_cups_holder_base/usd/place_cups_holder_base.usd",
            physics=PhysicStateType.XFORM,
        ),
        RigidObjMetaCfg(
            name="mug_visual0",
            filepath="roboverse_data/assets/rlbench/place_cups/mug_visual1/usd/mug_visual1.usd",  # reuse same asset
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug_visual1",
            filepath="roboverse_data/assets/rlbench/place_cups/mug_visual1/usd/mug_visual1.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug_visual2",
            filepath="roboverse_data/assets/rlbench/place_cups/mug_visual1/usd/mug_visual1.usd",  # reuse same asset
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug_visual3",
            filepath="roboverse_data/assets/rlbench/place_cups/mug_visual1/usd/mug_visual1.usd",  # reuse same asset
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
