from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PlugChargerInPowerSupplyMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/plug_charger_in_power_supply/v2"
    objects = [
        RigidObjMetaCfg(
            name="charger",
            usd_path="roboverse_data/assets/rlbench/plug_charger_in_power_supply/charger/usd/charger.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="task_wall",
            usd_path="roboverse_data/assets/rlbench/plug_charger_in_power_supply/task_wall/usd/task_wall.usd",
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="plug",
            usd_path="roboverse_data/assets/rlbench/plug_charger_in_power_supply/plug/usd/plug.usd",
            physics=PhysicStateType.GEOM,
        ),
    ]
    # TODO: add checker
