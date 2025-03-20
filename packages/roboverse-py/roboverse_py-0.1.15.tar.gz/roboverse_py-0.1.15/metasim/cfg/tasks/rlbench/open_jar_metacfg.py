from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class OpenJarMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/open_jar/v2"
    objects = [
        RigidObjMetaCfg(
            name="jar0",
            usd_path="roboverse_data/assets/rlbench/open_jar/jar0/usd/jar0.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="jar1",
            usd_path="roboverse_data/assets/rlbench/open_jar/jar1/usd/jar1.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="jar_lid0",
            usd_path="roboverse_data/assets/rlbench/open_jar/jar_lid0/usd/jar_lid0.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="jar_lid1",
            usd_path="roboverse_data/assets/rlbench/open_jar/jar_lid1/usd/jar_lid1.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="target",
            usd_path="roboverse_data/assets/rlbench/open_jar/target/usd/target.usd",
            physics=PhysicStateType.GEOM,
        ),
    ]
    # TODO: add checker
