from __future__ import annotations

#########################################
## Setup logging
#########################################
from loguru import logger as log
from rich.logging import RichHandler

log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])

#########################################
### Add command line arguments
#########################################
from dataclasses import dataclass
from typing import Literal

import tyro


@dataclass
class Args:
    robot: str = "franka"
    js: bool = False
    """Directly generate joint space random actions."""
    num_envs: int = 1
    sim: Literal["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco"] = "isaaclab"


args = tyro.cli(Args)

#########################################
### Normal code
#########################################

import rootutils

rootutils.setup_root(__file__, pythonpath=True)


def main():
    num_envs: int = args.num_envs

    # specificly for isaacgym
    if args.sim == "isaacgym":
        from isaacgym import gymapi, gymtorch, gymutil  # noqa: F401

    import torch
    from curobo.types.math import Pose
    from pytorch3d import transforms

    ## Import put here to support isaacgym
    from metasim.cfg.cameras import PinholeCameraMetaCfg
    from metasim.cfg.scenario import ScenarioMetaCfg
    from metasim.constants import SimType
    from metasim.utils.kinematics_utils import get_curobo_models
    from metasim.utils.setup_util import get_robot, get_sim_env_class, get_task

    task = get_task("pick_cube")
    robot = get_robot(args.robot)
    camera = PinholeCameraMetaCfg(
        name="camera",
        data_types=["rgb", "depth"],
        width=256,
        height=256,
        pos=(1.5, 0.0, 1.5),
        look_at=(0.0, 0.0, 0.0),
    )
    scenario = ScenarioMetaCfg(task=task, robot=robot, cameras=[camera], sim=args.sim)

    env_class = get_sim_env_class(SimType(args.sim))
    env = env_class(scenario, num_envs)

    from omni.isaac.core.objects import FixedSphere
    from omni.isaac.core.prims import XFormPrim

    ## Reset
    obs, extras = env.reset()

    ## cuRobo controller
    if not args.js:
        *_, robot_ik = get_curobo_models(robot)
        curobo_n_dof = len(robot_ik.robot_config.cspace.joint_names)
        ee_n_dof = len(robot.gripper_release_q)

        if args.sim == "isaaclab":
            FixedSphere(
                prim_path="/World/envs/env_0/target",
                name="target",
                scale=torch.tensor([0.05, 0.05, 0.05]),
                position=torch.tensor([0.0, 0.0, 0.0]),
                color=torch.tensor([1.0, 0.0, 0.0]),
            )

    step = 0
    q_min = torch.ones(len(robot.joint_limits.values()), device="cuda:0") * 100
    q_max = torch.ones(len(robot.joint_limits.values()), device="cuda:0") * -100
    while True:
        log.debug(f"Step {step}")

        # Generate random action
        if args.js:
            # XXX: this could have bug when dict key order is not same as joint name order
            j_limits = torch.tensor(list(robot.joint_limits.values()))
            j_ranges = j_limits[:, 1] - j_limits[:, 0]
            q = j_ranges.unsqueeze(0) * torch.rand((num_envs, robot.num_joints)) + j_limits[:, 0].unsqueeze(0)
            assert q.shape == (num_envs, robot.num_joints)
            assert torch.all(q >= j_limits[:, 0]) and torch.all(q <= j_limits[:, 1])
            q = q.to("cuda:0")

        else:
            # Generate random actions
            random_gripper_widths = torch.rand((num_envs, len(robot.gripper_release_q)))
            random_gripper_widths = torch.tensor(robot.gripper_release_q) + random_gripper_widths * (
                torch.tensor(robot.gripper_actuate_q) - torch.tensor(robot.gripper_release_q)
            )

            ee_rot_target = torch.rand((num_envs, 3), device="cuda:0") * torch.pi
            ee_quat_target = transforms.matrix_to_quaternion(transforms.euler_angles_to_matrix(ee_rot_target, "XYZ"))

            # Compute targets
            curr_robot_q = obs["joint_qpos"].cuda()
            robot_root_state = obs["robot_root_state"].cuda()
            robot_pos, robot_quat = robot_root_state[:, 0:3], robot_root_state[:, 3:7]

            if robot.name == "iiwa":
                ee_pos_target = torch.distributions.Uniform(-0.5, 0.5).sample((num_envs, 3)).to("cuda:0")
                ee_pos_target[:, 2] += 0.5
            elif robot.name == "franka":
                ee_pos_target = torch.distributions.Uniform(-0.5, 0.5).sample((num_envs, 3)).to("cuda:0")
                ee_pos_target[:, 2] += 0.5
            elif robot.name == "sawyer":
                ee_pos_target = torch.stack(
                    [
                        torch.distributions.Uniform(-0.8, 0.8).sample((num_envs, 1)),
                        torch.distributions.Uniform(-0.8, 0.8).sample((num_envs, 1)),
                        torch.distributions.Uniform(0.2, 0.8).sample((num_envs, 1)),
                    ],
                    dim=-1,
                ).to("cuda:0")
            else:
                raise ValueError(f"Unsupported robot: {robot.name}")

            target_prim = XFormPrim("/World/envs/env_0/target", name="target")
            target_prim.set_world_pose(
                position=transforms.quaternion_apply(transforms.quaternion_invert(robot_quat), ee_pos_target)
                + robot_pos
            )

            # Solve IK
            seed_config = curr_robot_q[:, :curobo_n_dof].unsqueeze(1).tile([1, robot_ik._num_seeds, 1])
            result = robot_ik.solve_batch(Pose(ee_pos_target, ee_quat_target), seed_config=seed_config)

            # Compose robot command
            q = curr_robot_q.clone()
            ik_succ = result.success.squeeze(1)
            q[ik_succ, :curobo_n_dof] = result.solution[ik_succ, 0].clone()
            q[:, -ee_n_dof:] = random_gripper_widths

        actions = [
            {"dof_pos_target": dict(zip(robot.actuators.keys(), q[i_env].tolist()))} for i_env in range(num_envs)
        ]
        q_min = torch.min(torch.stack([q_min, q[0]], -1), -1)[0]
        q_max = torch.max(torch.stack([q_max, q[0]], -1), -1)[0]

        log.info(f"q: {[f'{x:.2f}' for x in q[0].tolist()]}")
        log.info(f"q_min: {[f'{x:.2f}' for x in q_min.tolist()]}")
        log.info(f"q_max: {[f'{x:.2f}' for x in q_max.tolist()]}")

        for _ in range(1 if args.js else 30):
            env.handler.step(actions)
            env.handler.render()
        step += 1

        obs = env.handler.get_observation()

    env.handler.close()


if __name__ == "__main__":
    main()
    main()
