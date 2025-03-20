import argparse
import time
from typing import Type

import gymnasium as gym
import torch
from loguru import logger as log
from omni.isaac.lab.app import AppLauncher

from metasim.cfg.objects import ArticulationObjMetaCfg, BaseObjMetaCfg, RigidObjMetaCfg
from metasim.cfg.robots import BaseRobotMetaCfg
from metasim.cfg.scenario import ScenarioMetaCfg
from metasim.types import Action, Dof, EnvState, Extra, Obs, Reward, Success, Termination, TimeOut

from ..base import BaseSimHandler, EnvWrapper, IdentityEnvWrapper
from .env_overwriter import IsaaclabEnvOverwriter
from .isaaclab_helper import get_pose, joint_is_implicit_actuator

try:
    from .empty_env import EmptyEnv
except:
    pass


class IsaaclabHandler(BaseSimHandler):
    def __init__(self, scenario: ScenarioMetaCfg, num_envs: int = 1, headless: bool = False):
        super().__init__(scenario, num_envs, headless)
        self.checker_debug_viewers = scenario.task.checker.get_debug_viewers()

    def launch(self) -> None:
        super().launch()
        TaskName = self.task.__class__.__name__.removesuffix("MetaCfg")
        env_overwriter = IsaaclabEnvOverwriter(self.scenario)
        gym.register(
            id=TaskName,
            entry_point="metasim.sim.isaaclab.empty_env:EmptyEnv",
            disable_env_checker=True,
            order_enforce=False,
            kwargs={
                "env_cfg_entry_point": "metasim.sim.isaaclab.empty_env:EmptyEnvCfg",
                "_setup_scene": env_overwriter._setup_scene,
                "_reset_idx": env_overwriter._reset_idx,
                "_pre_physics_step": env_overwriter._pre_physics_step,
                "_apply_action": env_overwriter._apply_action,
                "_get_observations": env_overwriter._get_observations,
                "_get_rewards": env_overwriter._get_rewards,
                "_get_dones": env_overwriter._get_dones,
            },
        )
        parser = argparse.ArgumentParser()
        AppLauncher.add_app_launcher_args(parser)
        args = parser.parse_args([])
        args.enable_cameras = True
        args.headless = self.headless

        ## Only set args.renderer seems not enough
        if self.scenario.render.mode == "raytracing":
            args.renderer = "RayTracedLighting"
        elif self.scenario.render.mode == "pathtracing":
            args.renderer = "PathTracing"
        elif self.scenario.render.mode == "rasterization":
            raise ValueError("Isaaclab does not support rasterization")
        else:
            raise ValueError(f"Unknown render mode: {self.scenario.render.mode}")

        app_launcher = AppLauncher(args)
        self.simulation_app = app_launcher.app

        from omni.isaac.lab_tasks.utils import parse_env_cfg

        env_cfg = parse_env_cfg(TaskName)
        env_cfg.scene.num_envs = self.num_envs
        env_cfg.decimation = self.task.decimation
        env_cfg.episode_length_s = self.task.episode_length * (1 / 60) * self.task.decimation

        self.env: EmptyEnv = gym.make(TaskName, cfg=env_cfg)

        ## Render mode setting, must be done after isaaclab is launched
        ## For more info, see the import below
        import carb
        import omni.replicator.core as rep

        # from omni.rtx.settings.core.widgets.pt_widgets import PathTracingSettingsFrame

        rep.settings.set_render_rtx_realtime()  # fix noising rendered images

        settings = carb.settings.get_settings()
        if self.scenario.render.mode == "pathtracing":
            settings.set_string("/rtx/rendermode", "PathTracing")
        elif self.scenario.render.mode == "raytracing":
            settings.set_string("/rtx/rendermode", "RayTracedLighting")
        elif self.scenario.render.mode == "rasterization":
            raise ValueError("Isaaclab does not support rasterization")
        else:
            raise ValueError(f"Unknown render mode: {self.scenario.render.mode}")

        log.info(f"Render mode: {settings.get_as_string('/rtx/rendermode')}")
        log.info(f"Render totalSpp: {settings.get('/rtx/pathtracing/totalSpp')}")
        log.info(f"Render spp: {settings.get('/rtx/pathtracing/spp')}")
        log.info(f"Render adaptiveSampling/enabled: {settings.get('/rtx/pathtracing/adaptiveSampling/enabled')}")
        log.info(f"Render maxBounces: {settings.get('/rtx/pathtracing/maxBounces')}")

    ############################################################
    ## Gymnasium main methods
    ############################################################
    def step(self, action: list[Action]) -> tuple[Obs, Reward, Success, TimeOut, Extra]:
        joint_names = self.get_object_joint_names(self.robot)
        action_env_tensors = torch.zeros((self.num_envs, len(joint_names)), device=self.env.device)
        for env_id in range(self.num_envs):
            action_env = action[env_id]
            for i, joint_name in enumerate(joint_names):
                # Convert numpy float32 to torch tensor and move to correct device
                action_env_tensors[env_id, i] = torch.tensor(
                    action_env["dof_pos_target"][joint_name], device=self.env.device
                )

        _, _, _, _, extras = self.env.step(action_env_tensors)
        time_out = self.get_time_out()
        success = self.get_success()
        obs = self.get_observation()
        reward = self.get_reward()

        return obs, reward, success, time_out, extras

    def reset(self, env_ids: list[int] | None = None) -> tuple[Obs, Extra]:
        if env_ids is None:
            env_ids = list(range(self.num_envs))

        log.info(f"Resetting envs {env_ids}")

        tic = time.time()
        _, extras = self.env.reset(env_ids=env_ids)
        toc = time.time()
        log.trace(f"Reset isaaclab env time: {toc - tic:.2f}s")

        tic = time.time()
        self.task.checker.reset(self, env_ids=env_ids)
        toc = time.time()
        log.trace(f"Reset checker time: {toc - tic:.2f}s")

        ## Force rerender, see https://isaac-sim.github.io/IsaacLab/main/source/refs/issues.html#blank-initial-frames-from-the-camera
        tic = time.time()
        # XXX: previously 12 is not enough for pick_cube, if this is the case again, try 18
        for _ in range(12):
            # XXX: previously sim.render() is not enough for pick_cube, if this is the case again, try calling sim.step()
            # self.env.sim.step()
            self.env.sim.render()
        toc = time.time()
        log.trace(f"Reset render time: {toc - tic:.2f}s")

        ## Update camera buffer
        tic = time.time()
        for sensor in self.env.scene.sensors.values():
            sensor.update(dt=0)
        toc = time.time()
        log.trace(f"Reset sensor buffer time: {toc - tic:.2f}s")

        ## Update obs
        tic = time.time()
        obs = self.get_observation()
        toc = time.time()
        log.trace(f"Reset getting obs time: {toc - tic:.2f}s")

        return obs, extras

    def render(self) -> None:
        pass

    def close(self) -> None:
        super().close()
        self.env.close()
        self.simulation_app.close()

    ############################################################
    ## Utils
    ############################################################
    def refresh_render(self) -> None:
        for sensor in self.env.scene.sensors.values():
            sensor.update(dt=0)
        self.env.sim.render()

    def get_observation(self) -> Obs:
        obs = self.env._get_observations()
        # obs["states"] = self.get_states()  # TODO: This will increase 50% more step time, find a better way
        return obs

    def get_reward(self) -> Reward:
        from metasim.cfg.tasks.base_task_metacfg import BaseRLTaskMetaCfg

        if hasattr(self.task, "reward_fn"):
            return self.task.reward_fn(self.get_states())

        elif isinstance(self.task, BaseRLTaskMetaCfg):
            final_reward = torch.zeros(self.num_envs)
            for reward_func, reward_weight in zip(self.task.reward_functions, self.task.reward_weights):
                final_reward += reward_func(self.get_states()) * reward_weight
            return final_reward
        else:
            return None

    def get_success(self) -> Success:
        return self.task.checker.check(self)

    def get_time_out(self) -> TimeOut:
        _, time_out = self.env._get_dones()
        time_out = time_out.cpu()
        return time_out

    def get_termination(self) -> Termination:
        ## TODO: implement termination better
        # log.error("get_termination() not implemented, please override this method")
        return None

    ############################################################
    ## Set states
    ############################################################
    def _set_object_pose(
        self,
        object: BaseObjMetaCfg,
        position: torch.Tensor,  # (num_envs, 3)
        rotation: torch.Tensor,  # (num_envs, 4)
        env_ids: list[int] | None = None,
    ) -> None:
        """
        Set the pose of an object, set the velocity to zero
        """
        if env_ids is None:
            env_ids = list(range(self.num_envs))

        assert position.shape == (len(env_ids), 3)
        assert rotation.shape == (len(env_ids), 4)

        if isinstance(object, ArticulationObjMetaCfg):
            obj_inst = self.env.scene.articulations[object.name]
        elif isinstance(object, RigidObjMetaCfg):
            obj_inst = self.env.scene.rigid_objects[object.name]
        else:
            raise ValueError(f"Invalid object type: {type(object)}")

        pose = torch.concat(
            [
                position.to(self.env.device, dtype=torch.float32) + self.env.scene.env_origins[env_ids],
                rotation.to(self.env.device, dtype=torch.float32),
            ],
            dim=-1,
        )
        obj_inst.write_root_pose_to_sim(pose, env_ids=torch.tensor(env_ids, device=self.env.device))
        obj_inst.write_root_velocity_to_sim(
            torch.zeros((len(env_ids), 6), device=self.env.device, dtype=torch.float32),
            env_ids=torch.tensor(env_ids, device=self.env.device),
        )  # ! critical
        obj_inst.write_data_to_sim()

    def _set_object_joint_pos(
        self,
        object: BaseObjMetaCfg,
        joint_pos: torch.Tensor,  # (num_envs, num_joints)
        env_ids: list[int] | None = None,
    ) -> None:
        if env_ids is None:
            env_ids = list(range(self.num_envs))
        assert joint_pos.shape[0] == len(env_ids)
        pos = joint_pos.to(self.env.device)
        vel = torch.zeros_like(pos)
        obj_inst = self.env.scene.articulations[object.name]
        obj_inst.write_joint_state_to_sim(pos, vel, env_ids=torch.tensor(env_ids, device=self.env.device))
        obj_inst.write_data_to_sim()

    def set_states(self, states: list[EnvState], env_ids: list[int] | None = None) -> None:
        if env_ids is None:
            env_ids = list(range(self.num_envs))
        for obj in self.objects + [self.robot]:
            if obj.name not in states[0]:
                log.warning(f"Missing {obj.name} in states, setting its velocity to zero")
                pos, rot = get_pose(self.env, obj.name, env_ids=env_ids)
                self._set_object_pose(obj, pos, rot, env_ids=env_ids)
                continue

            if states[0][obj.name].get("pos", None) is None or states[0][obj.name].get("rot", None) is None:
                log.warning(f"No pose found for {obj.name}, setting its velocity to zero")
                pos, rot = get_pose(self.env, obj.name, env_ids=env_ids)
                self._set_object_pose(obj, pos, rot, env_ids=env_ids)
            else:
                pos = torch.stack([states[env_id][obj.name]["pos"] for env_id in env_ids]).to(self.env.device)
                rot = torch.stack([states[env_id][obj.name]["rot"] for env_id in env_ids]).to(self.env.device)
                self._set_object_pose(obj, pos, rot, env_ids=env_ids)

            if isinstance(obj, ArticulationObjMetaCfg):
                if states[0][obj.name].get("dof_pos", None) is None:
                    log.warning(f"No dof_pos found for {obj.name}")
                else:
                    dof_dict = [states[env_id][obj.name]["dof_pos"] for env_id in env_ids]
                    joint_names = self.get_object_joint_names(obj)
                    joint_pos = torch.zeros((len(env_ids), len(joint_names)), device=self.env.device)
                    for i, joint_name in enumerate(joint_names):
                        joint_pos[:, i] = torch.Tensor([x[joint_name] for x in dof_dict])
                    self._set_object_joint_pos(obj, joint_pos, env_ids=env_ids)
                    if obj == self.robot:
                        robot_inst = self.env.scene.articulations[obj.name]
                        robot_inst.set_joint_position_target(
                            joint_pos, env_ids=torch.tensor(env_ids, device=self.env.device)
                        )
                        robot_inst.write_data_to_sim()

    def set_pose(self, obj_name: str, pos: torch.Tensor, rot: torch.Tensor) -> None:
        # XXX: This is so hacky
        obj = next(
            (obj for obj in self.objects + [self.robot] + self.checker_debug_viewers if obj.name == obj_name), None
        )
        self._set_object_pose(obj, pos, rot)

    ############################################################
    ## Get states
    ############################################################
    def get_states(self, env_ids: list[int] | None = None) -> list[EnvState]:
        if env_ids is None:
            env_ids = list(range(self.num_envs))
        states = []
        for env_id in env_ids:
            env_state = {}
            for obj in self.objects + [self.robot]:
                if isinstance(obj, ArticulationObjMetaCfg):
                    obj_inst = self.env.scene.articulations[obj.name]
                else:
                    obj_inst = self.env.scene.rigid_objects[obj.name]
                obj_state = {}

                ## Basic states
                obj_state["pos"] = obj_inst.data.root_pos_w[env_id].cpu() - self.env.scene.env_origins[env_id].cpu()
                obj_state["rot"] = obj_inst.data.root_quat_w[env_id].cpu()
                obj_state["vel"] = obj_inst.data.root_vel_w[env_id].cpu()
                obj_state["ang_vel"] = obj_inst.data.root_ang_vel_w[env_id].cpu()

                ## Joint states
                if isinstance(obj, ArticulationObjMetaCfg):
                    obj_state["dof_pos"] = {
                        joint_name: obj_inst.data.joint_pos[env_id][i].item()
                        for i, joint_name in enumerate(obj_inst.joint_names)
                    }
                    obj_state["dof_vel"] = {
                        joint_name: obj_inst.data.joint_vel[env_id][i].item()
                        for i, joint_name in enumerate(obj_inst.joint_names)
                    }

                ## Actuator states
                ## XXX: Could non-robot objects have actuators?
                if isinstance(obj, BaseRobotMetaCfg):
                    obj_state["dof_pos_target"] = {
                        joint_name: obj_inst.data.joint_pos_target[env_id][i].item()
                        for i, joint_name in enumerate(obj_inst.joint_names)
                    }
                    obj_state["dof_vel_target"] = {
                        joint_name: obj_inst.data.joint_vel_target[env_id][i].item()
                        for i, joint_name in enumerate(obj_inst.joint_names)
                    }
                    obj_state["dof_torque"] = {
                        joint_name: (
                            obj_inst.data.joint_effort_target[env_id][i].item()
                            if joint_is_implicit_actuator(joint_name, obj_inst)
                            else obj_inst.data.applied_torque[env_id][i].item()
                        )
                        for i, joint_name in enumerate(obj_inst.joint_names)
                    }
                env_state[obj.name] = obj_state

                ## Body states
                ### XXX: will have bug when there are multiple objects with same structure, e.g. dual gripper
                coms = obj_inst.root_physx_view.get_coms()
                coms = coms.reshape((self.env.num_envs, obj_inst.num_bodies, 7))
                com_positions = coms[:, :, :3]  # (num_envs, num_bodies, 3)
                for i, body_name in enumerate(obj_inst.body_names):
                    body_state = {}
                    body_state["pos"] = (
                        obj_inst.data.body_pos_w[env_id, i].cpu() - self.env.scene.env_origins[env_id].cpu()
                    )
                    body_state["rot"] = obj_inst.data.body_quat_w[env_id, i].cpu()
                    body_state["vel"] = obj_inst.data.body_lin_vel_w[env_id, i].cpu()
                    body_state["ang_vel"] = obj_inst.data.body_ang_vel_w[env_id, i].cpu()
                    body_state["com"] = com_positions[env_id, i].cpu()
                    env_state[f"metasim_body_{body_name}"] = body_state

            states.append(env_state)
        return states

    def get_pos(
        self,
        obj_name: str,
        env_ids: list[int] | None = None,
        obj_subpath: str | None = None,
    ) -> torch.FloatTensor:
        if env_ids is None:
            env_ids = list(range(self.num_envs))
        pos, _ = get_pose(self.env, obj_name, obj_subpath, env_ids=env_ids)
        assert pos.shape == (len(env_ids), 3)
        return pos

    def get_rot(
        self,
        obj_name: str,
        env_ids: list[int] | None = None,
        obj_subpath: str | None = None,
    ) -> torch.FloatTensor:
        if env_ids is None:
            env_ids = list(range(self.num_envs))
        _, rot = get_pose(self.env, obj_name, obj_subpath, env_ids=env_ids)
        assert rot.shape == (len(env_ids), 4)
        return rot

    def get_dof_pos(self, obj_name: str, joint_name: str, env_ids: list[int] | None = None) -> torch.FloatTensor:
        if env_ids is None:
            env_ids = list(range(self.num_envs))
        dof_pos = torch.zeros(len(env_ids))
        for i, env_id in enumerate(env_ids):
            dof_pos[i] = self.env.scene.articulations[obj_name].data.joint_pos[env_id][
                self.env.scene.articulations[obj_name].joint_names.index(joint_name)
            ]
        return dof_pos

    ############################################################
    ## Misc
    ############################################################
    def is_running(self) -> bool:
        return self.simulation_app.is_running()

    def get_object_joint_names(self, object: BaseObjMetaCfg) -> list[str]:
        assert isinstance(object, ArticulationObjMetaCfg)
        return self.env.scene.articulations[object.name].joint_names

    def get_robot_joint_limits(self) -> tuple[Dof, Dof]:
        dof_min_tensor, dof_max_tensor = self.env.robot.root_physx_view.get_dof_limits()[0].split(1, dim=-1)
        dof_min = {
            joint_name: dof_min_tensor[i].item() for i, joint_name in enumerate(self.get_object_joint_names(self.robot))
        }
        dof_max = {
            joint_name: dof_max_tensor[i].item() for i, joint_name in enumerate(self.get_object_joint_names(self.robot))
        }
        return dof_min, dof_max

    @property
    def episode_length_buf(self) -> list[int]:
        return self.env.episode_length_buf.tolist()


IsaaclabEnv: Type[EnvWrapper[IsaaclabHandler]] = IdentityEnvWrapper(IsaaclabHandler)
