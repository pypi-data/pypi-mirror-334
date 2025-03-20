from __future__ import annotations

from metasim.utils import configclass

from .base_robot_metacfg import BaseActuatorMetaCfg, BaseRobotMetaCfg


@configclass
class GoogleRobotStaticMetaCfg(BaseRobotMetaCfg):
    name: str = "google_robot_static"
    num_joints: int = 11
    urdf_path: str = "roboverse_data/robots/googlerobot_description/google_robot_meta_sim_fix_wheel_fix_fingertip.urdf"
    enabled_gravity: bool = False
    enabled_self_collisions: bool = False
    actuators: dict[str, BaseActuatorMetaCfg] = {
        "joint_torso": BaseActuatorMetaCfg(velocity_limit=0.5),
        "joint_shoulder": BaseActuatorMetaCfg(velocity_limit=0.5),
        "joint_bicep": BaseActuatorMetaCfg(velocity_limit=0.5),
        "joint_elbow": BaseActuatorMetaCfg(velocity_limit=0.5),
        "joint_forearm": BaseActuatorMetaCfg(velocity_limit=0.5),
        "joint_wrist": BaseActuatorMetaCfg(velocity_limit=0.5),
        "joint_gripper": BaseActuatorMetaCfg(velocity_limit=0.5),
        "joint_finger_right": BaseActuatorMetaCfg(velocity_limit=0.5),
        "joint_finger_left": BaseActuatorMetaCfg(velocity_limit=0.5),
        "joint_head_pan": BaseActuatorMetaCfg(velocity_limit=0.5),
        "joint_head_tilt": BaseActuatorMetaCfg(velocity_limit=0.5),
    }
    # ee_prim_path: str = "panda_hand"
