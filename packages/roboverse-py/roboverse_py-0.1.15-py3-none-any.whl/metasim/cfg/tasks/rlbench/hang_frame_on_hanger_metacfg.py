from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class HangFrameOnHangerMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 600
    traj_filepath = "roboverse_data/trajs/rlbench/hang_frame_on_hanger/v2"
    objects = [
        RigidObjMetaCfg(
            name="frame",
            usd_path="roboverse_data/assets/rlbench/hang_frame_on_hanger/frame/usd/frame.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hanger",
            usd_path="roboverse_data/assets/rlbench/hang_frame_on_hanger/hanger/usd/hanger.usd",
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="task_wall",
            usd_path="roboverse_data/assets/rlbench/hang_frame_on_hanger/task_wall/usd/task_wall.usd",
            physics=PhysicStateType.GEOM,
        ),
    ]
    # TODO: add checker
