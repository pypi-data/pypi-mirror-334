from __future__ import annotations

import mujoco_viewer
import numpy as np
import torch
from dm_control import mjcf
from loguru import logger as log

from metasim.cfg.scenario import ScenarioMetaCfg
from metasim.constants import TaskType
from metasim.types import Extra, Obs, Reward, Success, TimeOut

from ..base import BaseSimHandler, EnvWrapper, IdentityEnvWrapper


class MujocoHandler(BaseSimHandler):
    def __init__(self, scenario: ScenarioMetaCfg, num_envs: int = 1, headless: bool = False):
        super().__init__(scenario, num_envs, headless)
        self.headless = headless

        if num_envs > 1:
            raise ValueError("MujocoHandler only supports single envs, please run with --num_envs 1.")

        self._robot = scenario.robot
        self._mujoco_robot_name = None
        self._robot_num_dof = None
        self._robot_path = self._robot.mjcf_path
        self._gravity_compensation = not self._robot.enabled_gravity

        self.viewer = None
        self.cameras = []
        for camera in scenario.cameras:
            self.cameras.append(camera)
        self._episode_length_buf = 0

        self.replay_traj = False
        self.use_task_decimation = False

        # FIXME: hard code decimation for now
        if self.use_task_decimation:
            self.decimation = self.scenario.decimation
        elif self.replay_traj:
            log.warning("Warning: hard coding decimation to 1 for object states")
            self.decimation = 1
        elif self.task is not None and self.task.task_type == TaskType.LOCOMOTION:
            self.decimation = self.scenario.decimation
        else:
            log.warning("Warning: hard coding decimation to 25 for replaying trajectories")
            self.decimation = 25

    def launch(self) -> None:
        super().launch()
        model = self._init_mujoco()
        self.physics = mjcf.Physics.from_mjcf_model(model)
        self.data = self.physics.data

        self.body_names = [self.physics.model.body(i).name for i in range(self.physics.model.nbody)]
        self.robot_body_names = [
            body_name for body_name in self.body_names if body_name.startswith(self._mujoco_robot_name)
        ]

    def _init_mujoco(self) -> mjcf.RootElement:
        object_paths = []
        for obj in self.objects:
            object_paths.append(obj.mjcf_path)

        mjcf_model = mjcf.RootElement()

        ## Optional: Add ground grid
        # mjcf_model.asset.add('texture', name="texplane", type="2d", builtin="checker", width=512, height=512, rgb1=[0.2, 0.3, 0.4], rgb2=[0.1, 0.2, 0.3])
        # mjcf_model.asset.add('material', name="matplane", reflectance="0.", texture="texplane", texrepeat=[1, 1], texuniform=True)

        for camera in self.cameras:
            direction = np.array([
                camera.look_at[0] - camera.pos[0],
                camera.look_at[1] - camera.pos[1],
                camera.look_at[2] - camera.pos[2],
            ])
            direction = direction / np.linalg.norm(direction)
            up = np.array([0, 0, 1])
            right = np.cross(direction, up)
            right = right / np.linalg.norm(right)
            up = np.cross(right, direction)

            camera_params = {
                "pos": f"{camera.pos[0]} {camera.pos[1]} {camera.pos[2]}",
                "mode": "fixed",
                "fovy": camera.vertical_fov,
                "xyaxes": f"{right[0]} {right[1]} {right[2]} {up[0]} {up[1]} {up[2]}",
                "resolution": f"{camera.width} {camera.height}",
            }
            mjcf_model.worldbody.add("camera", name=f"{camera.name}_custom", **camera_params)

        # Add ground grid, light, and skybox
        mjcf_model.asset.add(
            "texture",
            name="texplane",
            type="2d",
            builtin="checker",
            width=512,
            height=512,
            rgb1=[0, 0, 0],
            rgb2=[1.0, 1.0, 1.0],
        )
        mjcf_model.asset.add(
            "material", name="matplane", reflectance="0.2", texture="texplane", texrepeat=[1, 1], texuniform=True
        )
        ground = mjcf_model.worldbody.add(
            "geom",
            type="plane",
            pos="0 0 0",
            size="100 100 0.001",
            quat="1 0 0 0",
            condim="3",
            conaffinity="15",
            material="matplane",
        )
        self.object_body_names = []
        self.mj_objects = {}
        for i, (obj, obj_path) in enumerate(zip(self.objects, object_paths)):
            obj_mjcf = mjcf.from_path(obj_path)
            obj_attached = mjcf_model.attach(obj_mjcf)
            if not obj.fix_base_link:
                obj_attached.add("freejoint")
            self.object_body_names.append(obj_attached.full_identifier)
            self.mj_objects[obj.name] = obj_mjcf

        robot_xml = mjcf.from_path(self._robot_path)
        robot_attached = mjcf_model.attach(robot_xml)
        if self._robot.freejoint:
            robot_attached.add("freejoint")
        self.robot_attached = robot_attached
        self.mj_objects[self._robot.name] = robot_xml
        self._mujoco_robot_name = robot_xml.full_identifier
        return mjcf_model

    def _get_root_state(self, obj, obj_name):
        """Get root position, rotation, velocity for an object or robot."""
        if obj == self._robot:
            if self._robot.freejoint:
                root_joint = self.physics.data.joint(self._mujoco_robot_name)
                return {
                    "pos": torch.tensor(root_joint.qpos[:3], dtype=torch.float32),
                    "rot": torch.tensor(root_joint.qpos[3:7], dtype=torch.float32),
                    "vel": torch.tensor(root_joint.qvel[:3], dtype=torch.float32),
                    "ang_vel": torch.tensor(root_joint.qvel[3:6], dtype=torch.float32),
                }
            else:
                root_body_id = self.physics.model.body(self._mujoco_robot_name).id
                return {
                    "pos": torch.tensor(self.physics.data.xpos[root_body_id], dtype=torch.float32),
                    "rot": torch.tensor(self.physics.data.xquat[root_body_id], dtype=torch.float32),
                    "vel": torch.tensor(self.physics.data.cvel[root_body_id][:3], dtype=torch.float32),
                    "ang_vel": torch.tensor(self.physics.data.cvel[root_body_id][3:6], dtype=torch.float32),
                }
        else:
            model_name = self.mj_objects[obj_name].model + "/"
            try:
                obj_joint = self.physics.data.joint(model_name)
                return {
                    "pos": torch.tensor(obj_joint.qpos[:3], dtype=torch.float32),
                    "rot": torch.tensor(obj_joint.qpos[3:7], dtype=torch.float32),
                    "vel": torch.tensor(obj_joint.qvel[:3], dtype=torch.float32),
                    "ang_vel": torch.tensor(obj_joint.qvel[3:6], dtype=torch.float32),
                }
            except KeyError:
                obj_body_id = self.physics.model.body(model_name).id
                return {
                    "pos": torch.tensor(self.physics.data.xpos[obj_body_id], dtype=torch.float32),
                    "rot": torch.tensor(self.physics.data.xquat[obj_body_id], dtype=torch.float32),
                    "vel": torch.tensor(self.physics.data.cvel[obj_body_id][:3], dtype=torch.float32),
                    "ang_vel": torch.tensor(self.physics.data.cvel[obj_body_id][3:6], dtype=torch.float32),
                }

    def _get_joint_states(self, obj_name):
        """Get joint positions and velocities."""
        joint_states = {"dof_pos": {}, "dof_vel": {}}

        for joint_id in range(self.physics.model.njnt):
            joint_name = self.physics.model.joint(joint_id).name
            if joint_name.startswith(f"{obj_name}/") or (
                obj_name == self._robot.name and joint_name.startswith(self._mujoco_robot_name)
            ):
                clean_joint_name = joint_name.split("/")[-1]
                if clean_joint_name == "":
                    continue
                joint = self.physics.data.joint(joint_name)

                if len(joint.qpos.shape) == 0 or joint.qpos.shape == (1,):
                    joint_states["dof_pos"][clean_joint_name] = joint.qpos.item()
                    joint_states["dof_vel"][clean_joint_name] = joint.qvel.item()
                else:  # free joint
                    joint_states["dof_pos"][clean_joint_name] = torch.tensor(joint.qpos.copy(), dtype=torch.float32)
                    joint_states["dof_vel"][clean_joint_name] = torch.tensor(joint.qvel.copy(), dtype=torch.float32)

        return joint_states

    def _get_actuator_states(self, obj_name):
        """Get actuator states (targets and forces)."""
        actuator_states = {
            "dof_pos_target": {},
            "dof_vel_target": {},
            "dof_torque": {},
        }

        for actuator_id in range(self.physics.model.nu):
            actuator = self.physics.model.actuator(actuator_id)
            if actuator.name.startswith(self._mujoco_robot_name):
                clean_name = actuator.name[len(self._mujoco_robot_name) :]

                actuator_states["dof_pos_target"][clean_name] = float(
                    self.physics.data.ctrl[actuator_id].item()
                )  # Hardcoded to position control
                actuator_states["dof_vel_target"][clean_name] = None
                actuator_states["dof_torque"][clean_name] = float(self.physics.data.actuator_force[actuator_id].item())

        return actuator_states

    def get_states(self, env_ids: list[int] | None = None) -> list[dict]:
        state = {}

        for obj in self.objects + [self._robot]:
            state[obj.name] = self._get_root_state(obj, obj.name)
            state[obj.name].update(self._get_joint_states(obj.name))
            if obj == self._robot:
                state[obj.name].update(self._get_actuator_states(obj.name))

        for body_id in range(self.physics.model.nbody):
            body = self.physics.model.body(body_id)
            if body.name not in [self._mujoco_robot_name] + [obj.name for obj in self.objects]:
                state[f"metasim_body_{body.name}"] = {
                    "pos": torch.tensor(self.physics.data.xpos[body_id], dtype=torch.float32),
                    "rot": torch.tensor(self.physics.data.xquat[body_id], dtype=torch.float32),
                    "vel": torch.tensor(self.physics.data.cvel[body_id][:3], dtype=torch.float32),
                    "ang_vel": torch.tensor(self.physics.data.cvel[body_id][3:6], dtype=torch.float32),
                    "com": torch.tensor(self.physics.data.subtree_com[body_id], dtype=torch.float32),
                    "com_vel": torch.tensor(self.physics.data.subtree_linvel[body_id], dtype=torch.float32),
                }

        for site_id in range(self.physics.model.nsite):
            site = self.physics.model.site(site_id)

            linear_vel = None
            angular_vel = None
            for sensor_id in range(self.physics.model.nsensor):
                sensor = self.physics.model.sensor(sensor_id)
                if self.physics.model.sensor_objid[sensor_id] == site_id:
                    # mjtSensor enum: VELOCIMETER=2, GYRO=3
                    if sensor.type == 2:
                        linear_vel = torch.tensor(
                            self.physics.data.sensordata[sensor_id : sensor_id + 3], dtype=torch.float32
                        )
                    elif sensor.type == 3:
                        angular_vel = torch.tensor(
                            self.physics.data.sensordata[sensor_id : sensor_id + 3], dtype=torch.float32
                        )

            state[f"metasim_site_{site.name}"] = {
                "pos": torch.tensor(self.physics.data.site_xpos[site_id], dtype=torch.float32),
                "rot": torch.tensor(self.physics.data.site_xmat[site_id], dtype=torch.float32),
                "vel": linear_vel if linear_vel is not None else None,
                "ang_vel": angular_vel if angular_vel is not None else None,
            }

        return [state]

    def _set_root_state(self, obj_name, obj_state, zero_vel=False):
        """Set root position and rotation."""
        if "pos" not in obj_state and "rot" not in obj_state:
            return

        if obj_name == self._robot.name:
            if self._robot.freejoint:
                root_joint = self.physics.data.joint(self._mujoco_robot_name)
                root_joint.qpos[:3] = obj_state.get("pos", [0, 0, 0])
                root_joint.qpos[3:7] = obj_state.get("rot", [1, 0, 0, 0])
                if zero_vel:
                    root_joint.qvel[:6] = 0
            else:
                root_body = self.physics.named.model.body_pos[self._mujoco_robot_name]
                root_body_quat = self.physics.named.model.body_quat[self._mujoco_robot_name]
                root_body[:] = obj_state.get("pos", [0, 0, 0])
                root_body_quat[:] = obj_state.get("rot", [1, 0, 0, 0])
        else:
            model_name = self.mj_objects[obj_name].model + "/"
            try:
                obj_joint = self.physics.data.joint(model_name)
                obj_joint.qpos[:3] = obj_state["pos"]
                obj_joint.qpos[3:7] = obj_state["rot"]
                if zero_vel:
                    obj_joint.qvel[:6] = 0
            except KeyError:
                obj_body = self.physics.named.model.body_pos[model_name]
                obj_body_quat = self.physics.named.model.body_quat[model_name]
                obj_body[:] = obj_state["pos"]
                obj_body_quat[:] = obj_state["rot"]

    def _set_joint_state(self, obj_name, obj_state, zero_vel=False):
        """Set joint positions."""
        if "dof_pos" not in obj_state:
            return

        for joint_name, joint_pos in obj_state["dof_pos"].items():
            full_joint_name = (
                f"{self._mujoco_robot_name}{joint_name}" if obj_name == self._robot.name else f"{obj_name}/{joint_name}"
            )
            joint = self.physics.data.joint(full_joint_name)
            joint.qpos = joint_pos
            if zero_vel:
                joint.qvel = 0
            try:
                actuator = self.physics.model.actuator(full_joint_name)
                self.physics.data.ctrl[actuator.id] = joint_pos
            except KeyError:
                pass

    def set_states(self, states, env_ids=None, zero_vel=True):
        super().set_states(states, env_ids)
        if len(states) > 1:
            raise ValueError("MujocoHandler only supports single env state setting")

        for obj_name, obj_state in states[0].items():
            self._set_root_state(obj_name, obj_state, zero_vel)
            self._set_joint_state(obj_name, obj_state, zero_vel)

    def _disable_robotgravity(self):
        gravity_vec = np.array([0.0, 0.0, -9.81])

        self.physics.data.xfrc_applied[:] = 0
        for body_name in self.robot_body_names:
            body_id = self.physics.model.body(body_name).id
            force_vec = -gravity_vec * self.physics.model.body(body_name).mass
            self.physics.data.xfrc_applied[body_id, 0:3] = force_vec
            self.physics.data.xfrc_applied[body_id, 3:6] = 0

    def step(self, action: list[float]) -> tuple[Obs, Reward, Success, TimeOut, Extra]:
        self._episode_length_buf += 1

        super().step(action)
        joint_targets = action[0]["dof_pos_target"]

        if self.replay_traj:
            for joint_name, target_pos in joint_targets.items():
                joint = self.physics.data.joint(f"{self._mujoco_robot_name}{joint_name}")
                joint.qpos = target_pos
        else:
            for joint_name, target_pos in joint_targets.items():
                actuator = self.physics.data.actuator(f"{self._mujoco_robot_name}{joint_name}")
                actuator.ctrl = target_pos

        if self._gravity_compensation:
            self._disable_robotgravity()
        self.physics.step(self.decimation)

        if self.viewer is not None and self.viewer.is_alive and not self.headless:
            self.viewer.render()

        obs = self.get_observation() if self.headless else None
        success = self.checker.check(self)
        reward = self.get_reward()
        return (
            obs,
            reward,
            success,
            torch.tensor([self._episode_length_buf >= self.scenario.episode_length]),
            {},
        )

    def reset(self, env_ids: list[int] | None = None) -> tuple[Obs, Extra]:
        assert env_ids is None or env_ids == [0], "MujocoHandler only supports single env reset"
        self._episode_length_buf = 0
        self.simulate()
        obs = self.get_observation()
        self.checker.reset(self)
        return obs, {}

    def refresh_render(self) -> None:
        if self.viewer is not None:
            self.physics.forward()
            self.viewer.render()

    def simulate(self):
        if self.viewer is not None:
            self.viewer.close()
        for i in range(self.scenario.task.step_repeat):
            self.physics.forward()
            self.physics.step()
            if not self.headless:
                self.viewer = mujoco_viewer.MujocoViewer(self.physics.model.ptr, self.physics.data.ptr)
                self.viewer.render()

    ############################################################
    ## Utils
    ############################################################
    def render(self):
        if self.headless:
            # Return an image in headless mode
            # TODO: config the camera in both cfg and xml
            return self.physics.render(camera_id=1, width=640, height=480)
        else:
            if self.viewer is not None and self.viewer.is_alive:
                self.viewer.render()
                # Shouldn't return image for non-headless mode, this will block the desktop render loop
                # return self.physics.render(camera_id=1, width=640, height=480)

    def get_observation(self) -> Obs | None:
        obs = {}
        # Shouldn't return image for non-headless mode, this will block the desktop render loop
        if len(self.cameras) == 0 or not self.headless:
            return None
        camera = self.cameras[0]  # Using first camera as specified
        camera_id = "camera_custom"  # XXX: hard code camera id for now

        if "rgb" in camera.data_types:
            rgb_img = self.physics.render(
                width=camera.width,
                height=camera.height,
                camera_id=camera_id,
                depth=False,
            )
            obs["rgb"] = torch.from_numpy(rgb_img.copy()).unsqueeze(0)

        if "depth" in camera.data_types:
            depth_img = self.physics.render(
                width=camera.width,
                height=camera.height,
                camera_id=camera_id,
                depth=True,
            )
            obs["depth"] = torch.from_numpy(depth_img.copy()).unsqueeze(0)

        return obs

    def get_reward(self) -> Reward:
        from metasim.cfg.tasks.base_task_metacfg import BaseRLTaskMetaCfg

        if hasattr(self.task, "reward_fn"):
            return self.task.reward_fn(self.get_states())

        if isinstance(self.task, BaseRLTaskMetaCfg):
            final_reward = torch.zeros(self.num_envs)
            for reward_func, reward_weight in zip(self.task.reward_functions, self.task.reward_weights):
                final_reward += reward_func(self._robot.name)(self.get_states()) * reward_weight
            return final_reward
        else:
            return None

    def get_success(self) -> Success:
        return self.checker.check(self)

    def get_time_out(self) -> TimeOut:
        return torch.tensor([self._episode_length_buf >= self.scenario.episode_length], dtype=torch.bool)

    ############################################################
    ## Misc
    ############################################################
    def get_pos(self, obj_name: str, env_ids: list[int] | None = None) -> torch.FloatTensor:
        return torch.tensor(self.get_states()[0][obj_name]["pos"], dtype=torch.float32).unsqueeze(0)

    @property
    def num_envs(self) -> int:
        return 1

    @property
    def episode_length_buf(self) -> list[int]:
        return [self._episode_length_buf]


MujocoEnv: type[EnvWrapper[MujocoHandler]] = IdentityEnvWrapper(MujocoHandler)
