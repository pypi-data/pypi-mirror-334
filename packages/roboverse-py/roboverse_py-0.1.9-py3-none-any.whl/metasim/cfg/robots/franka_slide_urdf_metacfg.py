from __future__ import annotations

from metasim.utils import configclass

from .base_robot_metacfg import BaseActuatorMetaCfg, BaseRobotMetaCfg


@configclass
class FrankaSlideUrdfMetaCfg(BaseRobotMetaCfg):
    name: str = "franka"
    num_joints: int = 9
    urdf_path: str = "assets/franka_description/robots/franka_panda_slider_longer.urdf"
    enabled_gravity: bool = False
    enabled_self_collisions: bool = False
    actuators: dict[str, BaseActuatorMetaCfg] = {
        "z_free_base1": BaseActuatorMetaCfg(velocity_limit=5.0),
        "z_free_base2": BaseActuatorMetaCfg(velocity_limit=5.0),
        "panda_joint1": BaseActuatorMetaCfg(velocity_limit=2.175),
        "panda_joint2": BaseActuatorMetaCfg(velocity_limit=2.175),
        "panda_joint3": BaseActuatorMetaCfg(velocity_limit=2.175),
        "panda_joint4": BaseActuatorMetaCfg(velocity_limit=2.175),
        "panda_joint5": BaseActuatorMetaCfg(velocity_limit=2.61),
        "panda_joint6": BaseActuatorMetaCfg(velocity_limit=2.61),
        "panda_joint7": BaseActuatorMetaCfg(velocity_limit=2.61),
        "panda_finger_joint1": BaseActuatorMetaCfg(velocity_limit=0.2),
        "panda_finger_joint2": BaseActuatorMetaCfg(velocity_limit=0.2),
    }
    ee_prim_path: str = "panda_hand"
