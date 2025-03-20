from __future__ import annotations

from metasim.utils import configclass

from .base_robot_metacfg import BaseActuatorMetaCfg, BaseRobotMetaCfg


@configclass
class Ur5E2F85MetaCfg(BaseRobotMetaCfg):
    name: str = "ur5e_2f85"
    num_joints: int = 12
    usd_path: str = "data_isaaclab/robots/UniversalRobots/ur5e/ur5e_2f85_fix.usd"
    enabled_gravity: bool = False
    enabled_self_collisions: bool = False
    actuators: dict[str, BaseActuatorMetaCfg] = {
        "shoulder_pan_joint": BaseActuatorMetaCfg(velocity_limit=2.175),
        "shoulder_lift_joint": BaseActuatorMetaCfg(velocity_limit=2.175),
        "elbow_joint": BaseActuatorMetaCfg(velocity_limit=2.175),
        "wrist_1_joint": BaseActuatorMetaCfg(velocity_limit=2.175),
        "wrist_2_joint": BaseActuatorMetaCfg(velocity_limit=2.61),
        "wrist_3_joint": BaseActuatorMetaCfg(velocity_limit=2.61),
        # "finger_joint": BaseActuatorMetaCfg(velocity_limit=2.61, is_ee=True),
        # "left_inner_finger_joint": BaseActuatorMetaCfg(velocity_limit=2.61, is_ee=True),
        # "left_inner_knuckle_joint": BaseActuatorMetaCfg(velocity_limit=2.61, is_ee=True),
        # "right_inner_finger_joint": BaseActuatorMetaCfg(velocity_limit=2.61, is_ee=True),
        # "right_inner_knuckle_joint": BaseActuatorMetaCfg(velocity_limit=2.61, is_ee=True),
        # "right_outer_knuckle_joint": BaseActuatorMetaCfg(velocity_limit=2.61, is_ee=True),
    }
    joint_limits: dict[str, tuple[float, float]] = {
        "shoulder_pan_joint": (-6.28319, 6.28319),
        "shoulder_lift_joint": (-6.28319, 6.28319),
        "elbow_joint": (-3.14159, 3.14159),
        "wrist_1_joint": (-6.28319, 6.28319),
        "wrist_2_joint": (-6.28319, 6.28319),
        "wrist_3_joint": (-6.28319, 6.28319),
        # "finger_joint": (0.0, 0.785398),
        # "left_inner_finger_joint": (0.0, 0.785398),
        # "left_inner_knuckle_joint": (0.0, 0.785398),
        # "right_inner_finger_joint": (0.0, 0.785398),
        # "right_inner_knuckle_joint": (0.0, 0.785398),
        # "right_outer_knuckle_joint": (0.0, 0.785398),
    }
    ee_prim_path: str = "wrist_3_link"
    gripper_release_q = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    gripper_actuate_q = [0.785398, 0.785398, 0.785398, 0.785398, 0.785398, 0.785398]
    curobo_ref_cfg_name: str = "ur5e_robotiq_2f_140.yml"
    curobo_tcp_rel_pos: tuple[float, float, float] = [0.0, 0.0, -0.0635]
    curobo_tcp_rel_rot: tuple[float, float, float] = [0.0, 0.0, 0.0]
