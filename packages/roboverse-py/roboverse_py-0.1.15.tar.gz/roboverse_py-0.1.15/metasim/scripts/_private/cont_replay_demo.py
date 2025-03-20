from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from typing import Literal

import rootutils
import tyro
from loguru import logger as log
from rich.logging import RichHandler

rootutils.setup_root(__file__, pythonpath=True)
from metasim.cfg.randomization import RandomizationMetaCfg

# 这行只是让 Python 识别 logging 的 TRACE 等级，可按需保留
logging.addLevelName(5, "TRACE")
log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])


@dataclass
class Args:
    random: RandomizationMetaCfg
    task: str
    robot: Literal[
        "franka",
        "franka_with_gripper_extension",
        "sawyer",
        "iiwa",
        "h1_2_without_hand",
        "ur5e_2f85",
    ] = "franka"
    num_envs: int = 1
    sim: Literal["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco"] = "isaaclab"
    render: Literal["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco"] | None = None
    object_states: bool = False
    save_obs: bool = True


def parse_args() -> Args:
    args = tyro.cli(Args)
    return args


###########################################################
## Utils
###########################################################
def get_actions(all_actions, action_idx: int, num_envs: int):
    # 按当前步索引各个 env 的动作，如果超出序列就取最后一个动作。
    envs_actions = all_actions[:num_envs]
    actions = [
        env_actions[action_idx] if action_idx < len(env_actions) else env_actions[-1] for env_actions in envs_actions
    ]
    return actions


def get_states(all_states, action_idx: int, num_envs: int):
    # 按当前步索引各个 env 的状态，如果超出序列就取最后一个状态。
    envs_states = all_states[:num_envs]
    states = [env_states[action_idx] if action_idx < len(env_states) else env_states[-1] for env_states in envs_states]
    return states


def save_obs(obs, step: int):
    # 保存观察到的图像，可按需修改、裁剪或注释掉。
    from torchvision.utils import make_grid, save_image

    if obs is None or obs.get("rgb", None) is None:
        return

    rgb_data = obs["rgb"]  # (N, H, W, C), uint8
    # 这里假设 env 数量比较小，所以直接拼成网格
    import torch

    tensor_data = torch.from_numpy(rgb_data).permute(0, 3, 1, 2)  # (N, C, H, W)
    image = make_grid(tensor_data / 255, nrow=int(rgb_data.shape[0] ** 0.5))  # (C, H, W)
    os.makedirs("tmp", exist_ok=True)
    save_image(image, f"tmp/rgb_all_{step:04d}.png")


###########################################################
## Main
###########################################################
def main():
    args = parse_args()
    num_envs: int = args.num_envs

    # 如果使用IsaacGym，需要在import前先做gym相关的初始化
    if args.sim == "isaacgym" or args.render == "isaacgym":
        from isaacgym import gymapi, gymtorch, gymutil  # noqa: F401

    # 一些 import 放后面以支持 isaacgym
    from metasim.cfg.cameras import PinholeCameraMetaCfg
    from metasim.cfg.scenario import ScenarioMetaCfg
    from metasim.constants import SimType
    from metasim.double_sim import DoubleSimEnv
    from metasim.utils.demo_util import get_traj
    from metasim.utils.setup_util import get_robot, get_sim_env_class, get_task

    # 构造 scenario
    task = get_task(args.task)
    robot = get_robot(args.robot)
    camera = PinholeCameraMetaCfg(
        name="camera",
        data_types=["rgb", "depth"],
        width=256,
        height=256,
        pos=(1.5, -1.5, 1.5),
        look_at=(0.0, 0.0, 0.0),
    )
    scenario = ScenarioMetaCfg(task=task, robot=robot, cameras=[camera], random=args.random)

    # 创建环境：单环境或DoubleSimEnv
    if args.render is None:
        env_class = get_sim_env_class(SimType(args.sim))
        env = env_class(scenario, num_envs)
    else:
        env_class_render = get_sim_env_class(SimType(args.render))
        env_render = env_class_render(scenario, num_envs)
        env_class_physics = get_sim_env_class(SimType(args.sim))
        env_physics = env_class_physics(scenario, num_envs)
        env = DoubleSimEnv(env_physics, env_render)

    # 从 pkl 读取多段 demo
    # 假设 get_traj 返回类似：
    #   init_states: List[init_state1, init_state2, ...]
    #   all_actions: List[action_seq1, action_seq2, ...]
    #   all_states:  List[state_seq1,  state_seq2,  ...]
    # 其中下标 i 对应第 i 段 demo
    assert os.path.exists(task.traj_filepath), f"Trajectory file: {task.traj_filepath} does not exist."

    tic = time.time()
    init_states_list, all_actions_list, all_states_list = get_traj(task, robot, env.handler)
    toc = time.time()
    log.trace(f"Time to load data: {toc - tic:.2f}s")

    # 逐段回放：直到所有 demo 播放完毕才退出
    for demo_idx in range(len(init_states_list)):
        log.info(f"========== Replaying Demo #{demo_idx} ==========")

        init_states = [init_states_list[demo_idx]]  # 若你有多个env，也可对该数据做相应扩展
        actions_seq = [all_actions_list[demo_idx]]
        states_seq = [all_states_list[demo_idx]]

        # 先reset到该demo的初始状态
        tic = time.time()
        obs, extras = env.reset(states=init_states[:num_envs])
        toc = time.time()
        log.trace(f"Time to reset Demo #{demo_idx}: {toc - tic:.2f}s")

        step = 0
        if args.save_obs:
            save_obs(obs, step)

        # 连续回放单个 demo
        while True:
            log.debug(f"Demo #{demo_idx}, Step={step}")
            if args.object_states:
                # 如果要直接回放 states
                if args.sim == "isaacgym":
                    raise NotImplementedError("IsaacGym does not support object states replay yet.")
                current_states = get_states(states_seq, step, num_envs)
                env.handler.set_states(current_states)
                env.handler.refresh_render()
                obs = env.handler.get_observation()

                # 判断是否完成
                success = env.handler.task.checker.check(env.handler)
                if success.any():
                    log.info(f"Env {success.nonzero().squeeze(-1).tolist()} succeeded!")
                if success.all():
                    break
            else:
                # 正常执行 actions
                current_actions = get_actions(actions_seq, step, num_envs)
                obs, reward, success, time_out, extras = env.step(current_actions)

                if success.any():
                    log.info(f"Env {success.nonzero().squeeze(-1).tolist()} succeeded!")
                if time_out.any():
                    log.info(f"Env {time_out.nonzero().squeeze(-1).tolist()} timed out!")

                if success.all() or time_out.all():
                    break

            if args.save_obs:
                save_obs(obs, step + 1)

            step += 1

        log.info(f"Demo #{demo_idx} finished at step={step}")

    log.info("All demos in the pkl file have been replayed. Exiting.")


if __name__ == "__main__":
    main()
