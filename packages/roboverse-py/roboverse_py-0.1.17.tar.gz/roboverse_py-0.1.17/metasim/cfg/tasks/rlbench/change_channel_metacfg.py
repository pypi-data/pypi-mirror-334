from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class ChangeChannelMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/change_channel/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="tv_remote",
            usd_path="roboverse_data/assets/rlbench/change_channel/tv_remote/usd/tv_remote.usd",
        ),
        RigidObjMetaCfg(
            name="tv_frame",
            usd_path="roboverse_data/assets/rlbench/change_channel/tv_frame/usd/tv_frame.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
