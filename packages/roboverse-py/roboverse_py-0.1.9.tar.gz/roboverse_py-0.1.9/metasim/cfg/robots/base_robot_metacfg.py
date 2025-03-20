from __future__ import annotations

from dataclasses import MISSING

from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass


@configclass
class BaseActuatorMetaCfg:
    velocity_limit: float | None = None  # TODO: None means use the default value (USD joint prim value) or no limit?
    is_ee: bool = False
    damping: float = 40.0
    stiffness: float = 400.0


@configclass
class BaseRobotMetaCfg(ArticulationObjMetaCfg):
    # Articulation
    num_joints: int = MISSING
    actuators: dict[str, BaseActuatorMetaCfg] = {}
    ee_prim_path: str | None = None
    fix_base_link: bool = True
    joint_limits: dict[str, tuple[float, float]] = {}
    default_joint_positions: dict[str, float] = {}
    default_position: tuple[float, float, float] = (0.0, 0.0, 0.0)
    """
    Joint limits in the format of `{joint_name: (lower_limit, upper_limit)}`.
    Note that different simulators may have different order of joints, so you should not use the order in this dict!
    """
    ee_binary_action: bool = False
    gripper_release_q: list[float] = MISSING
    gripper_actuate_q: list[float] = MISSING

    # cuRobo Configs
    curobo_ref_cfg_name: str = MISSING
    curobo_tcp_rel_pos: tuple[float, float, float] = MISSING
    curobo_tcp_rel_rot: tuple[float, float, float] = MISSING

    # Simulation
    enabled_gravity: bool = True
    enabled_self_collisions: bool = True
    isaacgym_flip_visual_attachments: bool = True
