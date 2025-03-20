import torch
from curobo.cuda_robot_model.cuda_robot_model import CudaRobotModel
from curobo.geom.types import Cuboid, WorldConfig
from curobo.types.base import TensorDeviceType
from curobo.types.robot import RobotConfig
from curobo.util_file import (
    get_robot_path,
    join_path,
    load_yaml,
)
from curobo.wrap.reacher.ik_solver import IKSolver, IKSolverConfig
from pytorch3d import transforms

from metasim.cfg.robots.base_robot_metacfg import BaseRobotMetaCfg


def get_curobo_models(robot_cfg: BaseRobotMetaCfg, no_gnd=False):
    tensor_args = TensorDeviceType()
    config_file = load_yaml(join_path(get_robot_path(), robot_cfg.curobo_ref_cfg_name))["robot_cfg"]
    curobo_robot_cfg = RobotConfig.from_dict(config_file, tensor_args)
    world_cfg = WorldConfig(
        cuboid=[
            Cuboid(
                name="ground",
                pose=[0.0, 0.0, -0.4, 1, 0.0, 0.0, 0.0],
                dims=[10.0, 10.0, 0.8],
            )
        ]
    )
    ik_config = IKSolverConfig.load_from_robot_config(
        curobo_robot_cfg,
        None if no_gnd else world_cfg,
        rotation_threshold=0.05,
        position_threshold=0.005,
        num_seeds=20,
        self_collision_check=True,
        self_collision_opt=True,
        tensor_args=tensor_args,
        use_cuda_graph=True,
    )

    ik_solver = IKSolver(ik_config)
    kin_model = CudaRobotModel(curobo_robot_cfg.kinematics)

    def do_fk(q: torch.Tensor):
        robot_state = kin_model.get_state(q, config_file["kinematics"]["ee_link"])
        return robot_state.ee_position, robot_state.ee_quaternion

    return kin_model, do_fk, ik_solver


# TODO: Add relative rot; currently all are 0
def ee_pose_from_tcp_pose(robot_cfg: BaseRobotMetaCfg, tcp_pos: torch.Tensor, tcp_quat: torch.Tensor):
    tcp_rel_pos = torch.tensor(robot_cfg.curobo_tcp_rel_pos).unsqueeze(0).to(tcp_pos.device)
    ee_pos = tcp_pos + torch.matmul(transforms.quaternion_to_matrix(tcp_quat), -tcp_rel_pos.unsqueeze(-1)).squeeze()
    return ee_pos, tcp_quat


def tcp_pose_from_ee_pose(robot_cfg: BaseRobotMetaCfg, ee_pos: torch.Tensor, ee_quat: torch.Tensor):
    ee_rotmat = transforms.quaternion_to_matrix(ee_quat)
    tcp_rel_pos = torch.tensor(robot_cfg.curobo_tcp_rel_pos).unsqueeze(0).to(ee_rotmat.device)
    tcp_pos = ee_pos + torch.matmul(ee_rotmat, tcp_rel_pos.unsqueeze(-1)).squeeze()
    return tcp_pos, ee_quat
