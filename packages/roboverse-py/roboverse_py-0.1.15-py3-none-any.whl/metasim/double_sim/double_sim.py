from __future__ import annotations

from metasim.sim.base import BaseSimHandler, EnvWrapper
from metasim.types import Action, EnvState, Extra, Obs, Reward, Success, TimeOut


class DoubleSimEnv(EnvWrapper[BaseSimHandler]):
    def __init__(self, env_physics: type[EnvWrapper[BaseSimHandler]], env_render: type[EnvWrapper[BaseSimHandler]]):
        self.sim_env1 = env_physics  # physics
        self.sim_env2 = env_render  # render

    def reset(self, states: list[EnvState] | None = None):
        self.sim_env1.reset(states=states)
        return self.sim_env2.reset(states=states)

    def step(self, action: list[Action]) -> tuple[Obs, Reward, Success, TimeOut, Extra]:
        obs, reward, success, time_out, extra = self.sim_env1.step(action)
        states = self.sim_env1.handler.get_states()
        self.sim_env2.handler.set_states(states)
        self.sim_env2.handler.refresh_render()
        obs = self.sim_env2.handler.get_observation()
        return obs, reward, success, time_out, extra

    def render(self):
        self.sim_env2.render()

    def close(self):
        self.sim_env1.close()
        self.sim_env2.close()

    @property
    def handler(self) -> BaseSimHandler:
        # XXX: is it ok to return the physics handler?
        return self.sim_env1.handler
