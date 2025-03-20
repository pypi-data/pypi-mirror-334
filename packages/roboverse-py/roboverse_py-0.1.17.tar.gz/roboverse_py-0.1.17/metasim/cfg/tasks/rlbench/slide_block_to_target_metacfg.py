from metasim.cfg.objects import PrimitiveCubeMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class SlideBlockToTargetMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/slide_block_to_target/v2"
    objects = [
        PrimitiveCubeMetaCfg(
            name="block",
            size=[0.05625, 0.05625, 0.05625],
            color=[1.0, 0.0, 0.0],
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="target",
            usd_path="roboverse_data/assets/rlbench/slide_block_to_target/target/usd/target.usd",
            physics=PhysicStateType.GEOM,
        ),
    ]
    # TODO: add checker
