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
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid0",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid1",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid2",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid3",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid4",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid5",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid6",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid7",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid8",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid9",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid10",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid11",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="Cuboid12",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="target_cuboid",
            filepath="roboverse_data/assets/rlbench/play_jenga/Cuboid/usd/Cuboid.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
