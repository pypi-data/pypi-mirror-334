from __future__ import annotations

from metasim.utils import configclass

from .base_robot_metacfg import BaseActuatorMetaCfg, BaseRobotMetaCfg


@configclass
class SawyerMujocoMetaCfg(BaseRobotMetaCfg):
    name: str = "sawyer"
    num_joints: int = 9
    usd_path: str = "roboverse_data/robots/sawyer/usd/sawyer_mujoco_v1.usd"
    mjcf_path: str = "roboverse_data/robots/sawyer/mjcf/sawyer.xml"
    freejoint: bool = False
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
        "r_close": BaseActuatorMetaCfg(is_ee=True),
        "l_close": BaseActuatorMetaCfg(is_ee=True),
    }
    joint_limits: dict[str, tuple[float, float]] = {
        "right_j0": (-3.0503, 3.0503),
        "right_j1": (-3.8, -0.5),
        "right_j2": (-3.0426, 3.0426),
        "right_j3": (-3.0439, 3.0439),
        "right_j4": (-2.9761, 2.9761),
        "right_j5": (-2.9761, 2.9761),
        "right_j6": (-4.7124, 4.7124),
        "r_close": (0.0, 0.04),
        "l_close": (-0.03, 0),
    }
    # ee_prim_path: str = "sawyer_right_hand"
    # gripper_release_q = [0.020833, -0.020833]
    # gripper_actuate_q = [0.0, 0.0]

    # curobo_ref_cfg_name: str = "sawyer.yml"
    # curobo_tcp_rel_pos: tuple[float, float, float] = [0.0, 0.0, 0.105]
    # curobo_tcp_rel_rot: tuple[float, float, float] = [0.0, 0.0, 0.0]
