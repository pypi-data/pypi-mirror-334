"""Helper functions for humanoid robots, including h1 and h1_simple_hand."""

import torch

_METASIM_BODY_PREFIX = "metasim_body_"
_METASIM_SITE_PREFIX = "metasim_site_"
# robot_name = "h1"
# robot_name = "h1_simple_hand"


def torso_upright(envstate, robot_name: str):
    """Returns projection from z-axes of torso to the z-axes of world."""
    # env.handler.physics.named.data.xmat[f"{robot_name}/torso_link", "zz"]
    xmat = quaternion_to_matrix(envstate[f"{_METASIM_BODY_PREFIX}{robot_name}/torso_link"]["rot"])
    return xmat[2, 2]


def head_height(envstate, robot_name: str):
    """Returns the height of the torso."""
    # env.handler.physics.named.data.site_xpos[f"{robot_name}/head", "z"]
    return envstate[f"{_METASIM_SITE_PREFIX}{robot_name}/head"]["pos"][2]


def left_foot_height(envstate, robot_name: str):
    """Returns the height of the left foot."""
    # env.handler.physics.named.data.site_xpos[f"{robot_name}/left_foot", "z"]
    return envstate[f"{_METASIM_SITE_PREFIX}{robot_name}/left_foot"]["pos"][2]


def right_foot_height(envstate, robot_name: str):
    """Returns the height of the right foot."""
    # env.handler.physics.named.data.site_xpos[f"{robot_name}/right_foot", "z"]
    return envstate[f"{_METASIM_SITE_PREFIX}{robot_name}/right_foot"]["pos"][2]


def center_of_mass_position(envstate, robot_name: str):
    """Returns position of the center-of-mass."""
    # env.handler.physics.named.data.subtree_com[f"{robot_name}/pelvis"].copy()
    return envstate[f"{_METASIM_BODY_PREFIX}{robot_name}/pelvis"]["com"]


def center_of_mass_velocity(envstate, robot_name: str):
    """Returns the velocity of the center-of-mass."""
    # env.handler.physics.named.data.sensordata[f"{robot_name}/pelvis_subtreelinvel"].copy()
    return envstate[f"{_METASIM_BODY_PREFIX}{robot_name}/pelvis"]["com_vel"]


def center_of_mass_rotation(envstate, robot_name: str):
    """Returns the rotation of the center-of-mass."""
    # env.handler.physics.named.data.subtree_com[f"{robot_name}/pelvis"].copy()
    return envstate[f"{_METASIM_BODY_PREFIX}{robot_name}/pelvis"]["rot"]


def body_velocity(envstate, robot_name: str):
    """Returns the velocity of the torso in local frame."""
    # env.handler.physics.named.data.sensordata[f"{robot_name}/body_velocimeter"].copy()
    return envstate[f"{_METASIM_SITE_PREFIX}{robot_name}/com"][f"{robot_name}/body_velocimeter"]


def imu_position(envstate, robot_name: str):
    """Returns the position of the IMU."""
    # env.handler.physics.named.data.site_xpos[f"{robot_name}/imu"].copy()
    return envstate[f"{_METASIM_SITE_PREFIX}{robot_name}/imu"]["pos"]


def torso_vertical_orientation(envstate, robot_name: str):
    """Returns the z-projection of the torso orientation matrix."""
    # env.handler.physics.named.data.xmat[f"{robot_name}/torso_link", ["zx", "zy", "zz"]]
    xmat = quaternion_to_matrix(envstate[f"{_METASIM_BODY_PREFIX}{robot_name}/torso_link"]["rot"])
    return xmat[2, :]


@DeprecationWarning
def joint_angles(envstate, robot_name: str):
    """Returns the state without global orientation or position."""
    # Skip the 7 DoFs of the free root joint.
    # env.data.qpos[7 : self.dof].copy()
    return "joint_angles not implemented. Used for perception in humanoid_bench."


@DeprecationWarning
def joint_velocities(envstate, robot_name: str):
    """Returns the joint velocities."""
    # env.data.qvel[6 : self.dof - 1].copy()
    return "joint_velocities not implemented. Used for perception in humanoid_bench."


@DeprecationWarning
def control(envstate, robot_name: str):
    """Returns a copy of the control signals for the actuators."""
    # env.data.ctrl.copy()
    return "control not implemented. Used for perception in humanoid_bench."


def actuator_forces(envstate, robot_name: str):
    """Returns a copy of the forces applied by the actuators."""
    # env.handler.data.actuator_force.copy()
    return torch.tensor([
        x for x in envstate[f"{robot_name}"]["dof_torque"].values()
    ])  # envstate[f"{robot_name}"]["dof_torque"]


def left_hand_position(envstate, robot_name: str):
    """Returns the position of the left hand."""
    # env.handler.physics.named.data.site_xpos[f"{robot_name}/left_hand"]
    return envstate[f"{_METASIM_SITE_PREFIX}{robot_name}/left_hand"]["pos"]


def left_hand_velocity(envstate, robot_name: str):
    """Returns the velocity of the left hand."""
    # env.handler.physics.named.data.sensordata[f"{robot_name}/left_hand_subtreelinvel"].copy()
    return envstate[f"{_METASIM_BODY_PREFIX}{robot_name}/left_hand"][f"{robot_name}/left_hand_subtreelinvel"]


def left_hand_orientation(envstate, robot_name: str):
    """Returns the orientation of the left hand."""
    # env.handler.physics.named.data.site_xmat[f"{robot_name}/left_hand"]
    return envstate[f"{_METASIM_SITE_PREFIX}{robot_name}/left_hand"]["rot"]


def right_hand_position(envstate, robot_name: str):
    """Returns the position of the right hand."""
    # env.handler.physics.named.data.site_xpos[f"{robot_name}/right_hand"]
    return envstate[f"{_METASIM_SITE_PREFIX}{robot_name}/right_hand"]["pos"]


def right_hand_velocity(envstate, robot_name: str):
    """Returns the velocity of the right hand."""
    # env.handler.physics.named.data.sensordata["right_hand_subtreelinvel"].copy()
    return envstate[f"{_METASIM_BODY_PREFIX}{robot_name}/right_hand"][f"{robot_name}/right_hand_subtreelinvel"]


def right_hand_orientation(envstate, robot_name: str):
    """Returns the orientation of the right hand."""
    # env.handler.physics.named.data.site_xmat["right_hand"]
    return envstate[f"{_METASIM_SITE_PREFIX}{robot_name}/right_hand"]["rot"]


#######################################################
## Extra functions
#######################################################


def z_height(envstate, robot_name: str):
    """Returns the z-coordinate of the robot's position."""
    return envstate[f"{robot_name}"]["pos"][2]


#######################################################
## Helper functions
#######################################################


def quaternion_to_matrix(quat: torch.Tensor):
    """Converts a quaternion to a rotation matrix."""
    q_w, q_x, q_y, q_z = quat
    R = torch.tensor(
        [
            [1 - 2 * (q_y**2 + q_z**2), 2 * (q_x * q_y - q_w * q_z), 2 * (q_x * q_z + q_w * q_y)],
            [2 * (q_x * q_y + q_w * q_z), 1 - 2 * (q_x**2 + q_z**2), 2 * (q_y * q_z - q_w * q_x)],
            [2 * (q_x * q_z - q_w * q_y), 2 * (q_y * q_z + q_w * q_x), 1 - 2 * (q_x**2 + q_y**2)],
        ],
        dtype=quat.dtype,
    )
    return R
