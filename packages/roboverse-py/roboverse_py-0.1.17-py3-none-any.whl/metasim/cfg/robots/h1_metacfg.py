from __future__ import annotations

from metasim.utils import configclass

from .base_robot_metacfg import BaseActuatorMetaCfg, BaseRobotMetaCfg


@configclass
class H1MetaCfg(BaseRobotMetaCfg):
    name: str = "h1"
    num_joints: int = 26
    usd_path: str = "roboverse_data/robots/h1/usd/h1.usd"
    mjcf_path: str = "roboverse_data/robots/h1/mjcf/h1.xml"
    urdf_path: str = "roboverse_data/robots/h1/urdf/h1_wrist.urdf"
    enabled_gravity: bool = True
    freejoint: bool = True
    enabled_self_collisions: bool = False
    isaacgym_flip_visual_attachments: bool = False

    actuators: dict[str, BaseActuatorMetaCfg] = {
        "left_hip_yaw": BaseActuatorMetaCfg(),
        "left_hip_roll": BaseActuatorMetaCfg(),
        "left_hip_pitch": BaseActuatorMetaCfg(),
        "left_knee": BaseActuatorMetaCfg(),
        "left_ankle": BaseActuatorMetaCfg(),
        "right_hip_yaw": BaseActuatorMetaCfg(),
        "right_hip_roll": BaseActuatorMetaCfg(),
        "right_hip_pitch": BaseActuatorMetaCfg(),
        "right_knee": BaseActuatorMetaCfg(),
        "right_ankle": BaseActuatorMetaCfg(),
        "torso": BaseActuatorMetaCfg(),
        "left_shoulder_pitch": BaseActuatorMetaCfg(),
        "left_shoulder_roll": BaseActuatorMetaCfg(),
        "left_shoulder_yaw": BaseActuatorMetaCfg(),
        "left_elbow": BaseActuatorMetaCfg(),
        "right_shoulder_pitch": BaseActuatorMetaCfg(),
        "right_shoulder_roll": BaseActuatorMetaCfg(),
        "right_shoulder_yaw": BaseActuatorMetaCfg(),
        "right_elbow": BaseActuatorMetaCfg(),
    }
    joint_limits: dict[str, tuple[float, float]] = {
        "left_hip_yaw": (-0.43, 0.43),
        "left_hip_roll": (-0.43, 0.43),
        "left_hip_pitch": (-3.14, 2.53),
        "left_knee": (-0.26, 2.05),
        "left_ankle": (-0.87, 0.52),
        "right_hip_yaw": (-0.43, 0.43),
        "right_hip_roll": (-0.43, 0.43),
        "right_hip_pitch": (-3.14, 2.53),
        "right_knee": (-0.26, 2.05),
        "right_ankle": (-0.87, 0.52),
        "torso": (-2.35, 2.35),
        "left_shoulder_pitch": (-2.87, 2.87),
        "left_shoulder_roll": (-0.34, 3.11),
        "left_shoulder_yaw": (-1.3, 4.45),
        "left_elbow": (-1.25, 2.61),
        "right_shoulder_pitch": (-2.87, 2.87),
        "right_shoulder_roll": (-3.11, 0.34),
        "right_shoulder_yaw": (-4.45, 1.3),
        "right_elbow": (-1.25, 2.61),
    }
