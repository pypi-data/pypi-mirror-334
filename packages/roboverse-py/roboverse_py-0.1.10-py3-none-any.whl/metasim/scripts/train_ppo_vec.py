from __future__ import annotations

import random
from dataclasses import dataclass

import gymnasium as gym
import numpy as np
import rootutils
import torch
import tyro
from gymnasium import spaces
from gymnasium.vector import VectorEnv
from loguru import logger as log
from rich.logging import RichHandler
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecEnv

rootutils.setup_root(__file__, pythonpath=True)
log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])

from metasim.cfg.scenario import ScenarioMetaCfg
from metasim.constants import SimType
from metasim.sim.base import BaseSimHandler
from metasim.utils.demo_util import get_traj
from metasim.utils.setup_util import get_sim_env_class


@dataclass
class Args(ScenarioMetaCfg):
    task: str = "reach_origin"
    robot: str = "franka"
    num_envs: int = 16


args = tyro.cli(Args)


class MetaSimVecEnv(VectorEnv):
    """Vectorized environment for MetaSim that supports parallel RL training"""

    def __init__(
        self,
        scenario: ScenarioMetaCfg | None = None,
        sim_type: SimType = SimType.ISAACLAB,
        task_name: str | None = None,
        num_envs: int | None = 4,
    ):
        if scenario is None:
            scenario = ScenarioMetaCfg(task="pick_cube", robot="franka")
            scenario.task = task_name
            scenario.num_envs = num_envs
            scenario = ScenarioMetaCfg(**vars(scenario))
        self.num_envs = scenario.num_envs
        env_class = get_sim_env_class(sim_type)
        env = env_class(scenario, scenario.num_envs)
        self.handler: BaseSimHandler = env.handler
        self.render_mode = None  # XXX
        self.scenario = scenario

        # Get candidate states
        self.candidate_init_states, _, _ = get_traj(scenario.task, scenario.robot)

        # XXX: is the inf space ok?
        super().__init__(self.num_envs, spaces.Box(-np.inf, np.inf), spaces.Box(-np.inf, np.inf))

    ############################################################
    ## Gym-like interface
    ############################################################
    def reset(self, seed: int | None = None):
        init_states = self.unwrapped._get_default_states(seed)
        self.handler.set_states(init_states)
        self.handler.reset()
        return self.unwrapped._get_obs(), {}

    def step(self, actions: list[dict]):
        _, _, success, timeout, _ = self.handler.step(actions)
        obs = self.unwrapped._get_obs()
        rewards = self.unwrapped._calculate_rewards()
        return obs, rewards, success, timeout, {}

    def render(self):
        return self.handler.render()

    def close(self):
        self.handler.close()

    ############################################################
    ## Helper methods
    ############################################################
    def _get_obs(self):
        ## TODO: put this function into task definition?
        ## TODO: use torch instead of numpy
        """Get current observations for all environments"""
        states = self.handler.get_states()
        joint_pos = torch.tensor([
            [state[self.handler.robot.name]["dof_pos"][j] for j in self.handler.robot.joint_limits.keys()]
            for state in states
        ])

        # Get end effector positions (assuming 'ee' is the end effector subpath)
        ee_pos = torch.stack([state["metasim_body_panda_hand"]["pos"] for state in states])

        return torch.cat([joint_pos, ee_pos], dim=1)

    def _calculate_rewards(self):
        """Calculate rewards based on distance to origin"""
        states = self.handler.get_states()
        tot_reward = torch.zeros(self.num_envs)
        for reward_fn, weight in zip(self.scenario.task.reward_functions, self.scenario.task.reward_weights):
            tot_reward += weight * reward_fn(states)
        return tot_reward

    def _get_default_states(self, seed: int | None = None):
        """Generate default reset states"""
        ## TODO: use non-reqeatable random choice when there is enough candidate states?
        return random.Random(seed).choices(self.candidate_init_states, k=self.num_envs)


class StableBaseline3VecEnv(VecEnv):
    def __init__(self, env: MetaSimVecEnv):
        joint_limits = env.scenario.robot.joint_limits

        # TODO: customize action space?
        self.action_space = spaces.Box(
            low=np.array([lim[0] for lim in joint_limits.values()]),
            high=np.array([lim[1] for lim in joint_limits.values()]),
            dtype=np.float32,
        )

        # TODO: customize observation space?
        # Observation space: joint positions + end effector position
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(len(joint_limits) + 3,),  # joints + XYZ
            dtype=np.float32,
        )

        self.env = env
        self.render_mode = None  # XXX
        super().__init__(self.env.num_envs, self.observation_space, self.action_space)

    ############################################################
    ## Gym-like interface
    ############################################################
    def reset(self):
        obs, _ = self.env.reset()
        return obs.numpy()

    def step_async(self, actions: np.ndarray) -> None:
        self.action_dicts = [
            {"dof_pos_target": dict(zip(self.env.scenario.robot.joint_limits.keys(), action))} for action in actions
        ]

    def step_wait(self):
        obs, rewards, success, timeout, _ = self.env.step(self.action_dicts)

        dones = success | timeout
        if dones.any():
            init_states = self.env.unwrapped._get_default_states()
            self.env.handler.set_states(init_states, env_ids=np.nonzero(dones)[0].tolist())
            self.env.handler.reset(dones.nonzero().squeeze(-1).tolist())

        extra = [{} for _ in range(self.num_envs)]
        for env_id in range(self.num_envs):
            if dones[env_id]:
                extra[env_id]["terminal_observation"] = obs[env_id]
            extra[env_id]["TimeLimit.truncated"] = timeout[env_id] and not success[env_id]

        obs = self.env.unwrapped._get_obs()

        return obs.numpy(), rewards.numpy(), dones.numpy(), extra

    def render(self):
        return self.env.render()

    def close(self):
        self.env.close()

    ############################################################
    ## Abstract methods
    ############################################################
    def get_images(self):
        raise NotImplementedError

    def get_attr(self, attr_name, indices=None):
        if indices is None:
            indices = list(range(self.num_envs))
        return [getattr(self.env.handler, attr_name)] * len(indices)

    def set_attr(self, attr_name: str, value, indices=None) -> None:
        raise NotImplementedError

    def env_method(self, method_name: str, *method_args, indices=None, **method_kwargs):
        raise NotImplementedError

    def env_is_wrapped(self, wrapper_class, indices=None):
        raise NotImplementedError


def train_ppo():
    ## Choice 1: use scenario config to initialize the environment
    # scenario = ScenarioMetaCfg(**vars(args))
    # metasim_env = MetaSimVecEnv(scenario)

    ## Choice 2: use gym.make to initialize the environment
    metasim_env = gym.make("reach_origin", num_envs=args.num_envs)
    env = StableBaseline3VecEnv(metasim_env)

    # PPO configuration
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=128,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        device="cuda" if torch.cuda.is_available() else "cpu",
    )

    # Start training
    model.learn(total_timesteps=1_000_000)
    model.save("ppo_reach")


if __name__ == "__main__":
    train_ppo()
