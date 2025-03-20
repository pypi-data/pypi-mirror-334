from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar

import numpy as np
import torch
from loguru import logger as log

from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.cfg.scenario import ScenarioMetaCfg
from metasim.types import Action, Dof, EnvState, Extra, Obs, Reward, Success, Termination, TimeOut


class BaseSimHandler:
    def __init__(self, scenario: ScenarioMetaCfg, num_envs: int = 1, headless: bool = False):
        self.scenario = scenario
        self._num_envs = num_envs
        self.demo_idxs: list[int] = list(range(num_envs))
        self.init_state_idxs: list[int] = list(range(num_envs))
        self.headless = headless

        ## For quick reference
        self.task = scenario.task
        self.robot = scenario.robot
        self.cameras = scenario.cameras
        self.objects = scenario.task.objects
        self.object_dict = {obj.name: obj for obj in self.objects}

        # For reference robot
        self.object_dict[self.robot.name] = self.robot

    def launch(self) -> None:
        pass

    ############################################################
    ## Gymnasium main methods
    ############################################################
    @abstractmethod
    def step(self, action: list[Action]) -> tuple[Obs, Reward, Success, TimeOut, Extra]:
        pass

    @abstractmethod
    def reset(self, env_ids: list[int] | None = None) -> tuple[Obs, Extra]:
        """
        Reset the environment.

        Args:
            env_ids: The indices of the environments to reset. If None, all environments are reset.

        Return:
            obs: The observation of the environment. Currently all the environments are returned. Do we need to return only the reset environments?
            extra: Extra information. Currently is empty.
        """
        pass

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    ############################################################
    ## Set states
    ############################################################
    @abstractmethod
    def set_states(self, states: list[EnvState], env_ids: list[int] | None = None) -> None:
        pass

    @abstractmethod
    def set_dof_targets(self, obj_name: str, target: torch.Tensor) -> None:
        pass

    def set_pose(self, obj_name: str, pos: torch.Tensor, rot: torch.Tensor, env_ids: list[int] | None = None) -> None:
        states = [
            {
                obj_name: {
                    "pos": pos[env_id],
                    "rot": rot[env_id],
                }
            }
            for env_id in range(self.num_envs)
        ]
        self.set_states(states, env_ids=env_ids)

    ############################################################
    ## Get states
    ############################################################
    @abstractmethod
    def get_states(self, env_ids: list[int] | None = None) -> list[EnvState]:
        ## TODO: Add caching mechanism to speed up
        pass

    # Push from boshi, don't know if should delete
    #     def get_pos(self, obj_name: str, obj_subpath: str | None = None) -> torch.FloatTensor:
    #         return torch.stack([self.get_states()[env_id][obj_name]["pos"] for env_id in range(self.num_envs)])

    #     def get_rot(self, obj_name: str) -> torch.FloatTensor:
    #         return torch.stack([self.get_states()[env_id][obj_name]["rot"] for env_id in range(self.num_envs)])

    #     def get_dof_pos(self, obj_name: str, joint_name: str) -> torch.FloatTensor:
    #         states = self.get_states()
    #         return torch.Tensor([states[env_id][obj_name]["dof_pos"][joint_name] for env_id in range(self.num_envs)])

    def get_pos(
        self, obj_name: str, obj_subpath: str | None = None, env_ids: list[int] | None = None
    ) -> torch.FloatTensor:
        if self.num_envs > 1:
            log.warning(
                "You are using the unoptimized get_pos method, which could be slow, please contact the maintainer to"
                " support the optimized version if necessary"
            )
        if env_ids is None:
            env_ids = list(range(self.num_envs))

        states = self.get_states(env_ids=env_ids)
        return torch.stack([env_state[obj_name]["pos"] for env_state in states])

    def get_rot(self, obj_name: str, env_ids: list[int] | None = None) -> torch.FloatTensor:
        if self.num_envs > 1:
            log.warning(
                "You are using the unoptimized get_rot method, which could be slow, please contact the maintainer to"
                " support the optimized version if necessary"
            )
        if env_ids is None:
            env_ids = list(range(self.num_envs))

        states = self.get_states(env_ids=env_ids)
        return torch.stack([env_state[obj_name]["rot"] for env_state in states])

    def get_dof_pos(self, obj_name: str, joint_name: str, env_ids: list[int] | None = None) -> torch.FloatTensor:
        if self.num_envs > 1:
            log.warning(
                "You are using the unoptimized get_dof_pos method, which could be slow, please contact the maintainer"
                " to support the optimized version if necessary"
            )
        if env_ids is None:
            env_ids = list(range(self.num_envs))

        states = self.get_states(env_ids=env_ids)
        if isinstance(states[0][obj_name]["dof_pos"][joint_name], torch.Tensor):
            return torch.stack([env_state[obj_name]["dof_pos"][joint_name] for env_state in states])
        else:
            return torch.Tensor([env_state[obj_name]["dof_pos"][joint_name] for env_state in states])

    ############################################################
    ## Simulate
    ############################################################
    @abstractmethod
    def simulate(self):
        pass

    ############################################################
    ## Utils
    ############################################################
    @abstractmethod
    def refresh_render(self) -> None:
        pass

    @abstractmethod
    def get_observation(self) -> Obs:
        pass

    @abstractmethod
    def get_reward(self) -> Reward:
        pass

    @abstractmethod
    def get_success(self) -> Success:
        pass

    @abstractmethod
    def get_time_out(self) -> TimeOut:
        pass

    @abstractmethod
    def get_termination(self) -> Termination:
        pass

    ############################################################
    ## Misc
    ############################################################
    def is_running(self) -> bool:
        pass

    def get_object_joint_names(self, object: ArticulationObjMetaCfg) -> list[str]:
        assert isinstance(object, ArticulationObjMetaCfg)
        pass

    def get_robot_joint_limits(self) -> tuple[Dof, Dof]:
        pass

    @property
    def num_envs(self) -> int:
        return self._num_envs

    @property
    def episode_length_buf(self) -> list[int]:
        """
        The timestep of each environment, restart from 0 when reset, plus 1 at each step.
        """
        raise NotImplementedError


#     Push from boshi, don't know if should delete
#     def reset(self) -> tuple[Obs, Extra]:
#         obs = self.handler.get_states()
#         return obs, None

#     def step(self, actions: Action) -> tuple[Obs, Reward, Success, TimeOut, Extra]:
#         self.handler.set_dof_targets(self.handler.robot.name, actions)
#         self.handler.simulate()
#         obs = self.handler.get_states()
#         return (
#             obs,
#             None,
#             self.handler.scenario.task.checker.check(self.handler),
#             np.zeros(self.handler.num_envs),
#             np.zeros(self.handler.num_envs),
#         )

THandler = TypeVar("THandler", bound=BaseSimHandler)


class EnvWrapper(Generic[THandler]):
    handler: THandler

    def __init__(self, *args, **kwargs) -> None: ...
    def reset(self, states: list[EnvState] | None = None) -> tuple[Obs, Extra]: ...
    def step(self, action: list[Action]) -> tuple[Obs, Reward, Success, TimeOut, Extra]: ...
    def render(self) -> None: ...
    def close(self) -> None: ...


def IdentityEnvWrapper(cls: type[THandler]) -> type[EnvWrapper[THandler]]:
    class IdentityEnv(EnvWrapper[THandler]):
        def __init__(self, *args, **kwargs):
            self.handler = cls(*args, **kwargs)
            self.handler.launch()

        def reset(self, states: list[EnvState] | None = None) -> tuple[Obs, Extra]:
            if states is not None:
                self.handler.set_states(states)
            return self.handler.reset()

        def step(self, action: list[Action]) -> tuple[Obs, Reward, Success, TimeOut, Extra]:
            return self.handler.step(action)

        def render(self) -> None:
            self.handler.render()

        def close(self) -> None:
            self.handler.close()

    return IdentityEnv


def GymEnvWrapper(cls: type[THandler]) -> type[EnvWrapper[THandler]]:
    class GymEnv:
        def __init__(self, *args, **kwargs):
            self.handler = cls(*args, **kwargs)
            self.handler.launch()

        def observation(self, states: list[EnvState]) -> Obs:
            states_v2 = states
            cameras = states_v2["cameras"].values()
            first_camera = next(iter(cameras))
            obs_rgb = torch.from_numpy(
                np.array([first_camera["rgb"][..., :3] for env_id in range(self.handler.num_envs)])
            )
            obs = {"rgb": obs_rgb}

            return obs

        def reset(self, states: list[EnvState] | None = None) -> tuple[Obs, Extra]:
            if states is not None:
                self.handler.set_states(states)
                self.handler.simulate()
            ## TODO: obs should follow unified format
            # obs = {"states": self.handler.get_states()}
            obs = self.observation(self.handler.get_states())
            return obs, None

        def step(self, actions: list[Action]) -> tuple[Obs, Reward, Success, TimeOut, Extra]:
            self.handler.set_dof_targets(self.handler.robot.name, actions)
            self.handler.simulate()

            states_v2 = self.handler.get_states()
            obs = self.observation(states_v2)
            ## TODO: implement reward, success, time_out
            return (
                obs,
                None,
                torch.zeros(self.handler.num_envs, dtype=torch.bool),
                torch.zeros(self.handler.num_envs, dtype=torch.bool),
                None,
            )

        def render(self) -> None:
            ## TODO: implement render
            pass

        def close(self) -> None:
            self.handler.close()

    return GymEnv
