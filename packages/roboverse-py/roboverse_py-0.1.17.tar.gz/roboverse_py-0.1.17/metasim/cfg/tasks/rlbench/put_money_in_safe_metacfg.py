from metasim.cfg.objects import ArticulationObjMetaCfg, RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PutMoneyInSafeMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/put_money_in_safe/v2"
    objects = [
        RigidObjMetaCfg(
            name="dollar_stack",
            usd_path="roboverse_data/assets/rlbench/put_money_in_safe/dollar_stack/usd/dollar_stack.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        ArticulationObjMetaCfg(
            name="safe_body",
            usd_path="roboverse_data/assets/rlbench/put_money_in_safe/safe_body/usd/safe_body.usd",
        ),
    ]
    # TODO: add checker
