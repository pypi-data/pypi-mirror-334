from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class LightBulbOutMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/light_bulb_out/v2"
    objects = [
        RigidObjMetaCfg(
            name="bulb",
            usd_path="roboverse_data/assets/rlbench/light_bulb_in/bulb0/usd/bulb0.usd",  # reuse light_bulb_in asset
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bulb_holder0",
            usd_path="roboverse_data/assets/rlbench/light_bulb_in/bulb_holder0/usd/bulb_holder0.usd",  # reuse light_bulb_in asset
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="bulb_holder1",
            usd_path="roboverse_data/assets/rlbench/light_bulb_in/bulb_holder1/usd/bulb_holder1.usd",  # reuse light_bulb_in asset
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="lamp_base",
            usd_path="roboverse_data/assets/rlbench/light_bulb_in/lamp_base/usd/lamp_base.usd",  # reuse light_bulb_in asset
            physics=PhysicStateType.GEOM,
        ),
    ]
    # TODO: add checker
