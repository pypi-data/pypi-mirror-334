from __future__ import annotations

import math

import numpy as np

import sapien.core as sapien
from metasim.cfg.objects import (
    ArticulationObjMetaCfg,
    NonConvexRigidObjMetaCfg,
    PrimitiveCubeMetaCfg,
    PrimitiveSphereMetaCfg,
    RigidObjMetaCfg,
)
from metasim.cfg.robots import BaseRobotMetaCfg
from metasim.utils.math import quat_from_euler_np
from sapien.utils import Viewer

from ..base import BaseSimHandler, EnvWrapper, GymEnvWrapper


class SapienHandler(BaseSimHandler):
    def __init__(self, scenario, num_envs=1, headless=False):
        super().__init__(scenario, num_envs, headless=headless)
        self.headless = False

    def _build_sapien(self):
        self.engine = sapien.Engine()  # Create a physical simulation engine
        self.renderer = sapien.SapienRenderer()  # Create a renderer

        self.time_step = 1 / 100.0

        scene_config = sapien.SceneConfig()
        # scene_config.default_dynamic_friction = self.physical_params.dynamic_friction
        # scene_config.default_static_friction = self.physical_params.static_friction
        # scene_config.contact_offset = self.physical_params.contact_offset
        # scene_config.default_restitution = self.physical_params.restitution
        # scene_config.enable_pcm = True
        # scene_config.solver_iterations = self.sim_params.num_position_iterations
        # scene_config.solver_velocity_iterations = self.sim_params.num_velocity_iterations
        scene_config.gravity = [0, 0, -9.81]
        # scene_config.bounce_threshold = self.sim_params.bounce_threshold

        self.engine.set_renderer(self.renderer)
        self.scene = self.engine.create_scene(scene_config)
        self.scene.set_timestep(self.time_step)
        self.scene.add_ground(altitude=0)

        self.loader: sapien.URDFLoader = self.scene.create_urdf_loader()

        # Add agents
        self.object_ids = {}
        self.object_joint_order = {}
        self.camera_ids = {}

        for camera in self.cameras:
            # Create a camera entity in the scene
            camera_id = self.scene.add_camera(
                name=camera.name,
                width=camera.width,
                height=camera.height,
                fovy=np.deg2rad(camera.vertical_fov),
                near=camera.clipping_range[0],
                far=camera.clipping_range[1],
            )
            pos = np.array(camera.pos)
            look_at = np.array(camera.look_at)
            direction_vector = look_at - pos
            yaw = math.atan2(direction_vector[1], direction_vector[0])
            pitch = math.atan2(direction_vector[2], math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2))
            roll = 0
            camera_id.set_pose(sapien.Pose(p=pos, q=quat_from_euler_np(roll, -pitch, yaw)))
            self.camera_ids[camera.name] = camera_id

            # near, far = 0.1, 100
            # width, height = 640, 480
            # camera_id = self.scene.add_camera(
            #     name="camera",
            #     width=width,
            #     height=height,
            #     fovy=np.deg2rad(35),
            #     near=near,
            #     far=far,
            # )
            # camera_id.set_pose(sapien.Pose(p=[2, 0, 0], q=[0, 0, -1, 0]))
            # self.camera_ids[camera.name] = camera_id

        for object in [*self.objects, self.robot]:
            if isinstance(object, (ArticulationObjMetaCfg, BaseRobotMetaCfg)):
                self.loader.fix_root_link = object.fix_base_link
                self.loader.scale = object.scale
                file_path = object.urdf_path
                curr_id = self.loader.load(file_path)
                curr_id.set_root_pose(sapien.Pose(p=[0, 0, 0], q=[1, 0, 0, 0]))

                self.object_ids[object.name] = curr_id

                active_joints = curr_id.get_active_joints()
                # num_joints = len(active_joints)
                cur_joint_names = []
                for id, joint in enumerate(active_joints):
                    joint_name = joint.get_name()
                    cur_joint_names.append(joint_name)
                self.object_joint_order[object.name] = cur_joint_names

                ### TODO
                # Change dof properties
                ###

                if isinstance(object, BaseRobotMetaCfg):
                    active_joints = curr_id.get_active_joints()
                    for id, joint in enumerate(active_joints):
                        stiffness = object.actuators[joint.get_name()].stiffness
                        damping = object.actuators[joint.get_name()].damping
                        joint.set_drive_property(stiffness, damping)
                else:
                    active_joints = curr_id.get_active_joints()
                    for id, joint in enumerate(active_joints):
                        joint.set_drive_property(0, 0)

                # if agent.dof.init:
                #     robot.set_qpos(agent.dof.init)

                # if agent.dof.target:
                #     robot.set_drive_target(agent.dof.target)

            elif isinstance(object, PrimitiveCubeMetaCfg):
                actor_builder = self.scene.create_actor_builder()
                # material = get_material(self.scene, agent.rigid_shape_property)
                actor_builder.add_box_collision(
                    half_size=[x * object.scale for x in object.half_size],
                    density=object.density,
                    # material=material,
                )
                actor_builder.add_box_visual(
                    half_size=[x * object.scale for x in object.half_size],
                    color=object.color if object.color else [1.0, 1.0, 0.0],
                )
                box = actor_builder.build(name="box")  # Add a box
                box.set_pose(sapien.Pose(p=[0, 0, 0], q=[1, 0, 0, 0]))
                # box.set_damping(agent.rigid_shape_property.linear_damping, agent.rigid_shape_property.angular_damping)
                # if agent.vel:
                #     box.set_velocity(agent.vel)
                # if agent.ang_vel:
                #     box.set_angular_velocity(agent.ang_vel)
                # box.set_damping(agent.rigid_shape_property.linear_damping, agent.rigid_shape_property.angular_damping)
                # if agent.fix_base_link:
                #     box.lock_motion()
                # agent.instance = box
                self.object_ids[object.name] = box
                self.object_joint_order[object.name] = []

            elif isinstance(object, PrimitiveSphereMetaCfg):
                actor_builder = self.scene.create_actor_builder()
                # material = get_material(self.scene, agent.rigid_shape_property)
                actor_builder.add_sphere_collision(radius=object.radius, density=object.density)
                actor_builder.add_sphere_visual(
                    radius=object.radius * object.scale, color=object.color if object.color else [1.0, 1.0, 0.0]
                )
                sphere = actor_builder.build(name="sphere")  # Add a sphere
                sphere.set_pose(sapien.Pose(p=[0, 0, 0], q=[1, 0, 0, 0]))
                # sphere.set_damping(
                #     agent.rigid_shape_property.linear_damping, agent.rigid_shape_property.angular_damping
                # )
                # if agent.vel:
                #     sphere.set_velocity(agent.vel)
                # if agent.ang_vel:
                #     sphere.set_angular_velocity(agent.ang_vel)
                # if agent.fix_base_link:
                #     sphere.lock_motion()
                # agent.instance = sphere
                self.object_ids[object.name] = sphere
                self.object_joint_order[object.name] = []

            elif isinstance(object, NonConvexRigidObjMetaCfg):
                builder = self.scene.create_actor_builder()
                scene_pose = sapien.Pose(p=np.array(object.mesh_pose[:3]), q=np.array(object.mesh_pose[3:]))
                builder.add_nonconvex_collision_from_file(object.filepath, scene_pose)
                builder.add_visual_from_file(object.filepath, scene_pose)
                curr_id = builder.build_static(name=object.name)

                self.object_ids[object.name] = curr_id
                self.object_joint_order[object.name] = []

            elif isinstance(object, RigidObjMetaCfg):
                self.loader.fix_root_link = object.fix_base_link
                self.loader.scale = object.scale
                file_path = object.urdf_path
                curr_id = self.loader.load(file_path)
                builder = self.loader.load_file_as_articulation_builder(file_path)
                curr_id.set_root_pose(sapien.Pose(p=[0, 0, 0], q=[1, 0, 0, 0]))

                self.object_ids[object.name] = curr_id
                self.object_joint_order[object.name] = []

            # elif agent.type == "capsule":
            #     actor_builder = self.scene.create_actor_builder()
            #     material = get_material(self.scene, agent.rigid_shape_property)
            #     actor_builder.add_capsule_collision(
            #         radius=agent.radius, half_length=agent.length, density=agent.density, material=material
            #     )
            #     actor_builder.add_capsule_visual(
            #         radius=agent.radius, half_length=agent.length, color=agent.color if agent.color else [1.0, 1.0, 1.0]
            #     )
            #     capsule = actor_builder.build(name="capsule")  # Add a capsule
            #     capsule.set_pose(sapien.Pose(p=[*agent.pos], q=np.asarray(agent.rot)))
            #     capsule.set_damping(
            #         agent.rigid_shape_property.linear_damping, agent.rigid_shape_property.angular_damping
            #     )
            #     if agent.vel:
            #         capsule.set_velocity(agent.vel)
            #     if agent.ang_vel:
            #         capsule.set_angular_velocity(agent.ang_vel)
            #     if agent.fix_base_link:
            #         capsule.lock_motion()
            #     agent.instance = capsule

        # Add lights
        self.scene.set_ambient_light([0.5, 0.5, 0.5])
        # self.scene.add_directional_light(
        #     self.sim_params.directional_light_pos, self.sim_params.directional_light_target
        # )

        # Create viewer and adjust camera position
        # if not self.viewer_params.headless:
        if not self.headless:
            self.viewer = Viewer(self.renderer)  # Create a viewer (window)
            self.viewer.set_scene(self.scene)  # Bind the viewer and the scene

        if not self.headless:
            camera_pos = np.array([1.5, -1.5, 1.5])
            camera_target = np.array([0.0, 0.0, 0.0])
            # if self.viewer_params.viewer_rot != None:
            #     camera_z = np.array([0.0, 0.0, 1.0])
            #     camera_rot = np.array(self.viewer_params.viewer_rot)
            #     camera_target = camera_pos + quat_apply(camera_rot, camera_z)
            # else:
            #     camera_target = np.array(self.viewer_params.target_pos)
            direction_vector = camera_target - camera_pos
            yaw = math.atan2(direction_vector[1], direction_vector[0])
            pitch = math.atan2(
                direction_vector[2], math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)
            )  # 计算 roll 角（绕 X 轴的旋转角度）
            roll = 0
            # The coordinate frame in Sapien is: x(forward), y(left), z(upward)
            # The principle axis of the camera is the x-axis
            self.viewer.set_camera_xyz(x=camera_pos[0], y=camera_pos[1], z=camera_pos[2])
            # The rotation of the free camera is represented as [roll(x), pitch(-y), yaw(-z)]
            self.viewer.set_camera_rpy(r=roll, p=pitch, y=-yaw)
            self.viewer.toggle_axes(show=False)
            self.viewer.toggle_camera_lines(show=False)

        # self.viewer.set_fovy(self.viewer_params.horizontal_fov)
        # self.viewer.window.set_camera_parameters(near=0.05, far=100, fovy=self.viewer_params.fovy / 2) # the /2 is to align with isaac-gym

        # List for debug points
        self.debug_points = []
        self.debug_lines = []

        self.scene.update_render()
        for camera_name, camera_id in self.camera_ids.items():
            camera_id.take_picture()

    def _apply_action(self, action, instance):
        qf = instance.compute_passive_force(gravity=True, coriolis_and_centrifugal=True, external=False)
        instance.set_qf(qf)
        instance.set_drive_target(action)

    def set_dof_targets(self, obj_name, target):
        instance = self.object_ids[obj_name]
        if isinstance(instance, sapien.Articulation):
            action = target[0]
            action_arr = np.array([action["dof_pos_target"][name] for name in self.object_joint_order[self.robot.name]])
            self._apply_action(action_arr, instance)

    def simulate(self):
        self.scene.step()
        self.scene.update_render()
        if not self.headless:
            self.viewer.render()
        for camera_name, camera_id in self.camera_ids.items():
            camera_id.take_picture()

    def launch(self):
        self._build_sapien()

    def close(self):
        if not self.headless:
            self.viewer.close()
        self.scene = None

    def is_running(self):
        if not self.headless:
            return not self.viewer.closed
        else:
            return self.scene is not None

    def get_states(self, env_ids=None):
        states = {}

        for obj_name, obj_id in self.object_ids.items():
            states[obj_name] = {}
            if isinstance(obj_id, sapien.Articulation):
                dof_pos = obj_id.get_qpos()
                dof_vel = obj_id.get_qvel()
                states[obj_name]["dof_pos"] = {
                    name: dof_pos[id] for id, name in enumerate(self.object_joint_order[obj_name])
                }
            pose = obj_id.get_pose()
            states[obj_name].update({
                "pose": {
                    "pos": np.array(pose.p),
                    "rot": np.array(pose.q),
                }
            })

        states["cameras"] = {}

        for camera_name, camera_id in self.camera_ids.items():
            color_img = camera_id.get_float_texture("Color")[..., :3]
            color_img = (color_img * 255).clip(0, 255).astype("uint8")
            depth_img = -camera_id.get_float_texture("Position")[..., 2]
            # states[camera_name] = {
            #     "rgb": color_img,
            #     "depth": depth_img,
            # }
            states["cameras"][camera_name] = {"rgb": color_img}

        return states

    def set_states(self, states, env_ids=None):
        for name, val in states[0].items():
            if name not in self.object_ids:
                continue
            # assert name in self.object_ids
            # Reset joint state
            obj_id = self.object_ids[name]

            if isinstance(self.object_dict[name], ArticulationObjMetaCfg):
                joint_names = self.object_joint_order[name]
                qpos_list = []
                for i, joint_name in enumerate(joint_names):
                    qpos_list.append(val["dof_pos"][joint_name])
                obj_id.set_qpos(np.array(qpos_list))

            # Reset base position and orientation
            obj_id.set_pose(sapien.Pose(p=val["pos"], q=val["rot"]))


SapienEnv: type[EnvWrapper[SapienHandler]] = GymEnvWrapper(SapienHandler)
