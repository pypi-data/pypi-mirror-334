from __future__ import annotations

from metasim.utils import configclass

from .base_robot_metacfg import BaseActuatorMetaCfg, BaseRobotMetaCfg


@configclass
class FrankaWithGripperExtensionMetaCfg(BaseRobotMetaCfg):
    name: str = "franka_with_gripper_extension"
    num_joints: int = 9
    filepath: str = "roboverse_data/robots/franka_with_gripper_extension/usd/franka_with_gripper_extension_v1.usd"
    enabled_gravity: bool = False
    enabled_self_collisions: bool = False
    actuators: dict[str, BaseActuatorMetaCfg] = {
        "panda_joint1": BaseActuatorMetaCfg(velocity_limit=2.175),
        "panda_joint2": BaseActuatorMetaCfg(velocity_limit=2.175),
        "panda_joint3": BaseActuatorMetaCfg(velocity_limit=2.175),
        "panda_joint4": BaseActuatorMetaCfg(velocity_limit=2.175),
        "panda_joint5": BaseActuatorMetaCfg(velocity_limit=2.61),
        "panda_joint6": BaseActuatorMetaCfg(velocity_limit=2.61),
        "panda_joint7": BaseActuatorMetaCfg(velocity_limit=2.61),
        "panda_finger_joint1": BaseActuatorMetaCfg(velocity_limit=0.2, is_ee=True),
        "panda_finger_joint2": BaseActuatorMetaCfg(velocity_limit=0.2, is_ee=True),
    }
    joint_limits: dict[str, tuple[float, float]] = {
        "panda_joint1": (-2.8973, 2.8973),
        "panda_joint2": (-1.7628, 1.7628),
        "panda_joint3": (-2.8973, 2.8973),
        "panda_joint4": (-3.0718, -0.0698),
        "panda_joint5": (-2.8973, 2.8973),
        "panda_joint6": (-0.0175, 3.7525),
        "panda_joint7": (-2.8973, 2.8973),
        "panda_finger_joint1": (0.0, 0.04),  # 0.0 close, 0.04 open
        "panda_finger_joint2": (0.0, 0.04),  # 0.0 close, 0.04 open
    }
    ee_prim_path: str = "panda_hand"
    gripper_release_q = [0.04, 0.04]
    gripper_actuate_q = [0.0, 0.0]

    curobo_ref_cfg_name: str = "franka.yml"
    curobo_tcp_rel_pos: tuple[float, float, float] = [0.0, 0.0, 0.13312]
    curobo_tcp_rel_rot: tuple[float, float, float] = [0.0, 0.0, 0.0]
