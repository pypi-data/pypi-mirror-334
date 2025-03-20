import gymnasium as gym
import numpy as np
import rootutils
import torch
from gymnasium import spaces
from loguru import logger as log
from rich.logging import RichHandler
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

rootutils.setup_root(__file__, pythonpath=True)
log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])

from metasim.cfg.scenario import ScenarioMetaCfg
from metasim.constants import SimType
from metasim.sim.base import BaseSimHandler
from metasim.utils.setup_util import get_robot, get_sim_env_class, get_task


class MetaSimGymEnv(gym.Env):
    """Vectorized environment for MetaSim that supports parallel RL training"""

    def __init__(self, scenario: ScenarioMetaCfg, num_envs: int = 1, sim_type: SimType = SimType.ISAACLAB):
        super().__init__()

        self.num_envs = num_envs
        env_class = get_sim_env_class(sim_type)
        env = env_class(scenario, num_envs)
        self.handler: BaseSimHandler = env.handler

        # Get joint limits for action space
        joint_limits = scenario.robot.joint_limits
        self.action_space = spaces.Box(
            low=np.array([lim[0] for lim in joint_limits.values()]),
            high=np.array([lim[1] for lim in joint_limits.values()]),
            dtype=np.float32,
        )

        # Observation space: joint positions + end effector position
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(len(joint_limits) + 3,),  # joints + XYZ
            dtype=np.float32,
        )

        self.max_episode_steps = 500
        self.current_step = 0

    def reset(self, seed=None):
        log.info("Resetting environments")
        """Reset all environments"""
        self.current_step = 0
        init_states = self._get_default_states()
        self.handler.set_states(init_states)
        self.handler.reset()
        return self._get_obs(), None

    def step(self, actions):
        """Step through all environments"""
        self.current_step += 1

        # Convert numpy actions to handler format
        ## TODO: action should support vectorized actions
        action_dicts = [{"dof_pos_target": dict(zip(self.handler.robot.joint_limits.keys(), actions))}]

        # Step the simulation
        self.handler.step(action_dicts)

        # Get new observations and calculate rewards
        obs = self._get_obs()
        rewards = self._calculate_rewards()
        timeout = np.array([self.current_step >= self.max_episode_steps] * self.num_envs)
        success = np.zeros_like(timeout)

        return obs, rewards, success, timeout, {}

    def _get_obs(self):
        """Get current observations for all environments"""
        states = self.handler.get_states()
        joint_pos = np.array([
            [state[self.handler.robot.name]["dof_pos"][j] for j in self.handler.robot.joint_limits.keys()]
            for state in states
        ])

        # Get end effector positions (assuming 'ee' is the end effector subpath)
        ee_pos = np.array([state["metasim_body_panda_hand"]["pos"] for state in states])

        return np.concatenate([joint_pos, ee_pos], axis=1)

    def _calculate_rewards(self):
        """Calculate rewards based on distance to origin"""
        states = self.handler.get_states()
        ee_pos = np.array([state["metasim_body_panda_hand"]["pos"] for state in states])
        distances = np.linalg.norm(ee_pos, axis=1)
        return -distances  # Negative distance as reward

    def _get_default_states(self):
        """Generate default reset states"""
        return [
            {
                self.handler.robot.name: {
                    "dof_pos": {j: 0.0 for j in self.handler.robot.joint_limits.keys()},
                    "pos": torch.tensor([0.0, 0.0, 0.0]),
                    "rot": torch.tensor([1.0, 0.0, 0.0, 0.0]),
                }
            }
            for _ in range(self.num_envs)
        ]

    def close(self):
        self.handler.close()


def train_ppo():
    """Training procedure for PPO"""
    # Environment setup
    scenario = ScenarioMetaCfg(
        task=get_task("PickCube"),
        robot=get_robot("franka_stable"),
    )

    env = MetaSimGymEnv(scenario, num_envs=1)
    env = DummyVecEnv([lambda: env])

    # PPO configuration
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
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
