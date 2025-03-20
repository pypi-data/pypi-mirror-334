from __future__ import annotations

from metasim.utils import configclass

from .base_robot_metacfg import BaseActuatorMetaCfg, BaseRobotMetaCfg


@configclass
class SawyerMetaCfg(BaseRobotMetaCfg):
    name: str = "sawyer"
    num_joints: int = 10
    usd_path: str = "roboverse_data/robots/sawyer/usd/sawyer_v2.usd"
    enabled_gravity: bool = False
    enabled_self_collisions: bool = False
    actuators: dict[str, BaseActuatorMetaCfg] = {
        "right_j0": BaseActuatorMetaCfg(),
        "right_j1": BaseActuatorMetaCfg(),
        "right_j2": BaseActuatorMetaCfg(),
        "right_j3": BaseActuatorMetaCfg(),
        "right_j4": BaseActuatorMetaCfg(),
        "right_j5": BaseActuatorMetaCfg(),
        "right_j6": BaseActuatorMetaCfg(),
        "head_pan": BaseActuatorMetaCfg(),
        "right_gripper_l_finger_joint": BaseActuatorMetaCfg(is_ee=True),
        "right_gripper_r_finger_joint": BaseActuatorMetaCfg(is_ee=True),
    }
    joint_limits: dict[str, tuple[float, float]] = {
        "right_j0": (-3.05, 3.05),
        "right_j1": (-3.8094999, 2.2736),
        "right_j2": (-3.0425998, 3.0425998),
        "right_j3": (-3.0438999, 3.0438999),
        "right_j4": (-2.9760998, 2.9760998),
        "right_j5": (-2.9760998, 2.9760998),
        "right_j6": (-4.7123996, 4.7123996),
        "head_pan": (-5.095, 0.9064),
        "right_gripper_l_finger_joint": (0.0, 0.020833),
        "right_gripper_r_finger_joint": (-0.020833, 0),
    }
    ee_prim_path: str = "sawyer_right_hand"
    gripper_release_q = [0.020833, -0.020833]
    gripper_actuate_q = [0.0, 0.0]

    curobo_ref_cfg_name: str = "sawyer.yml"
    curobo_tcp_rel_pos: tuple[float, float, float] = [0.0, 0.0, 0.105]
    curobo_tcp_rel_rot: tuple[float, float, float] = [0.0, 0.0, 0.0]
