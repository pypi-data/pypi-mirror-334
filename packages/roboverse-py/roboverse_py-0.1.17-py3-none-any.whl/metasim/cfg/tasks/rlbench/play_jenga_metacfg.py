from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PlayJengaMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/play_jenga/v2"
    objects = [
        RigidObjMetaCfg(
            name="Cuboid",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid0",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid1",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid2",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid3",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid4",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid5",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid6",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid7",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid8",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid9",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid10",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid11",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid12",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="target_cuboid",
            usd_path="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
