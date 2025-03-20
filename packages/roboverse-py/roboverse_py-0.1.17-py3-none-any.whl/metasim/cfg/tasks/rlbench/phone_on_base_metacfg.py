from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PhoneOnBaseMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/phone_on_base/v2"
    objects = [
        RigidObjMetaCfg(
            name="phone_visual",
            usd_path="roboverse_data/assets/rlbench/phone_on_base/phone_visual/usd/phone_visual.usd",
            physics=PhysicStateType.XFORM,
        ),
        RigidObjMetaCfg(
            name="phone_case_visual",
            usd_path="roboverse_data/assets/rlbench/phone_on_base/phone_case_visual/usd/phone_case_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
