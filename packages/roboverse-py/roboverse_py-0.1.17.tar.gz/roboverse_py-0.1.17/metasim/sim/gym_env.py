from __future__ import annotations

from typing import Any, TypeVar

import gymnasium as gym
import numpy as np

from metasim.cfg.scenario import ScenarioMetaCfg
from metasim.types import Action, Extra, Obs

Terminated = TypeVar("Terminated", list[bool])
Truncated = TypeVar("Truncated", list[bool])
RenderFrame = TypeVar("RenderFrame")


class GymEnv(gym.Env):
    def __init__(self, scenario: ScenarioMetaCfg):
        self.scenario = scenario

    ###########################################################
    ## Gym methods
    ###########################################################
    def reset(self, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[Obs, Extra]:
        pass

    def step(self, action: Action) -> tuple[Obs, float, bool, bool, Extra]:
        pass

    def render(self) -> RenderFrame | list[RenderFrame] | None:
        pass

    def close(self):
        pass

    ###########################################################
    ## Gym properties
    ###########################################################
    ## These properties are not implemented in IsaacLab's DirectRLEnv
    @property
    def action_space(self) -> gym.Space:
        raise NotImplementedError

    @property
    def observation_space(self) -> gym.Space:
        raise NotImplementedError

    @property
    def reward_range(self) -> tuple[float, float]:
        raise NotImplementedError

    @property
    def metadata(self) -> dict[str, Any]:
        raise NotImplementedError

    @property
    def np_random(self) -> np.random.Generator:
        raise NotImplementedError
