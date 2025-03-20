import os

import torch
from loguru import logger as log

from metasim.cfg.lights import BaseLightMetaCfg, CylinderLightMetaCfg, DistantLightMetaCfg
from metasim.cfg.objects import (
    ArticulationObjMetaCfg,
    BaseObjMetaCfg,
    PrimitiveCubeMetaCfg,
    PrimitiveCylinderMetaCfg,
    PrimitiveSphereMetaCfg,
    RigidObjMetaCfg,
)
from metasim.cfg.robots import BaseRobotMetaCfg
from metasim.constants import PhysicStateType

try:
    from .empty_env import EmptyEnv
except:
    pass


def add_object(env: "EmptyEnv", obj: BaseObjMetaCfg) -> None:
    import omni.isaac.lab.sim as sim_utils
    from omni.isaac.lab.assets import (
        Articulation,
        ArticulationCfg,
        RigidObject,
        RigidObjectCfg,
    )

    assert isinstance(obj, BaseObjMetaCfg)
    prim_path = f"/World/envs/env_.*/{obj.name}"
    ## Rigid object
    if isinstance(obj, RigidObjMetaCfg):
        if obj.physics == PhysicStateType.XFORM:
            rigid_props = sim_utils.RigidBodyPropertiesCfg(disable_gravity=True, kinematic_enabled=True)
            collision_props = None
        elif obj.physics == PhysicStateType.GEOM:
            rigid_props = sim_utils.RigidBodyPropertiesCfg(disable_gravity=True, kinematic_enabled=True)
            collision_props = sim_utils.CollisionPropertiesCfg(collision_enabled=True)
        elif obj.physics == PhysicStateType.RIGIDBODY:
            rigid_props = sim_utils.RigidBodyPropertiesCfg()
            collision_props = sim_utils.CollisionPropertiesCfg(collision_enabled=True)
        else:
            raise ValueError(f"Unsupported physics state: {obj.physics}")

        ## Primitive object
        if isinstance(obj, PrimitiveCubeMetaCfg):
            env.scene.rigid_objects[obj.name] = RigidObject(
                RigidObjectCfg(
                    prim_path=prim_path,
                    spawn=sim_utils.MeshCuboidCfg(
                        size=tuple([x * obj.scale for x in obj.size]),
                        mass_props=sim_utils.MassPropertiesCfg(mass=obj.mass),
                        visual_material=sim_utils.PreviewSurfaceCfg(
                            diffuse_color=(obj.color[0], obj.color[1], obj.color[2])
                        ),
                        rigid_props=rigid_props,
                        collision_props=collision_props,
                    ),
                )
            )
            return
        if isinstance(obj, PrimitiveSphereMetaCfg):
            env.scene.rigid_objects[obj.name] = RigidObject(
                RigidObjectCfg(
                    prim_path=prim_path,
                    spawn=sim_utils.MeshSphereCfg(
                        radius=obj.radius,
                        mass_props=sim_utils.MassPropertiesCfg(mass=obj.mass),
                        visual_material=sim_utils.PreviewSurfaceCfg(
                            diffuse_color=(obj.color[0], obj.color[1], obj.color[2])
                        ),
                        rigid_props=rigid_props,
                        collision_props=collision_props,
                    ),
                )
            )
            return
        if isinstance(obj, PrimitiveCylinderMetaCfg):
            env.scene.rigid_objects[obj.name] = RigidObject(
                RigidObjectCfg(
                    prim_path=prim_path,
                    spawn=sim_utils.MeshCylinderCfg(
                        radius=obj.radius,
                        height=obj.height,
                        mass_props=sim_utils.MassPropertiesCfg(mass=obj.mass),
                        visual_material=sim_utils.PreviewSurfaceCfg(
                            diffuse_color=(obj.color[0], obj.color[1], obj.color[2])
                        ),
                        rigid_props=rigid_props,
                        collision_props=collision_props,
                    ),
                )
            )
            return
        ## File-based object
        # scale can be a constant or a tuple, or a list
        if isinstance(obj.scale, (tuple, list)):
            scale = tuple(obj.scale)
        else:
            scale = (obj.scale, obj.scale, obj.scale)

        usd_file_cfg = sim_utils.UsdFileCfg(
            usd_path=obj.usd_path,
            rigid_props=rigid_props,
            collision_props=collision_props,
            scale=scale,
        )
        if isinstance(obj, RigidObjMetaCfg):
            env.scene.rigid_objects[obj.name] = RigidObject(RigidObjectCfg(prim_path=prim_path, spawn=usd_file_cfg))
            return

    ## Articulation object
    if isinstance(obj, ArticulationObjMetaCfg):
        env.scene.articulations[obj.name] = Articulation(
            ArticulationCfg(
                prim_path=prim_path,
                spawn=sim_utils.UsdFileCfg(usd_path=obj.usd_path),
                actuators={},
            )
        )
        return
    raise ValueError(f"Unsupported object type: {type(obj)}")


def add_objects(env: "EmptyEnv", objects: list[BaseObjMetaCfg]) -> None:
    for obj in objects:
        add_object(env, obj)


def add_robot(env: "EmptyEnv", robot: BaseRobotMetaCfg) -> None:
    import omni.isaac.lab.sim as sim_utils
    from omni.isaac.lab.actuators import ImplicitActuatorCfg
    from omni.isaac.lab.assets import Articulation, ArticulationCfg

    cfg = ArticulationCfg(
        spawn=sim_utils.UsdFileCfg(
            usd_path=robot.usd_path,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(),
            articulation_props=sim_utils.ArticulationRootPropertiesCfg(),
        ),
        actuators={
            joint_name: ImplicitActuatorCfg(joint_names_expr=[joint_name], stiffness=None, damping=None)
            for joint_name in robot.actuators
        },
    )
    cfg.prim_path = f"/World/envs/env_.*/{robot.name}"
    cfg.spawn.usd_path = os.path.abspath(robot.usd_path)
    cfg.spawn.rigid_props.disable_gravity = not robot.enabled_gravity
    cfg.spawn.articulation_props.enabled_self_collisions = robot.enabled_self_collisions
    for joint_name, actuator in robot.actuators.items():
        cfg.actuators[joint_name].velocity_limit = actuator.velocity_limit

    robot_inst = Articulation(cfg)
    env.scene.articulations[robot.name] = robot_inst
    env.robot = robot_inst


def _add_light(env: "EmptyEnv", light: BaseLightMetaCfg, prim_path: str) -> None:
    import omni.isaac.lab.sim as sim_utils
    from omni.isaac.lab.sim.spawners import spawn_light

    if isinstance(light, DistantLightMetaCfg):
        spawn_light(
            prim_path,
            sim_utils.DistantLightCfg(
                intensity=light.intensity,
            ),
            orientation=light.quat,
        )
    elif isinstance(light, CylinderLightMetaCfg):
        spawn_light(
            prim_path,
            sim_utils.CylinderLightCfg(
                intensity=light.intensity,
                length=light.length,
                radius=light.radius,
            ),
            translation=light.pos,
            orientation=light.rot,
        )
    else:
        raise ValueError(f"Unsupported light type: {type(light)}")


def add_lights(env: "EmptyEnv", lights: list[BaseLightMetaCfg]) -> None:
    for i, light in enumerate(lights):
        _add_light(env, light, f"/World/envs/env_0/lights/light_{i}")


def get_pose(
    env: "EmptyEnv", obj_name: str, obj_subpath: str | None = None, env_ids: list[int] | None = None
) -> tuple[torch.FloatTensor, torch.FloatTensor]:
    from omni.isaac.core.prims import RigidPrimView

    if env_ids is None:
        env_ids = list(range(env.num_envs))

    if obj_name in env.scene.rigid_objects:
        obj_inst = env.scene.rigid_objects[obj_name]
    elif obj_name in env.scene.articulations:
        obj_inst = env.scene.articulations[obj_name]
    else:
        raise ValueError(f"Object {obj_name} not found")

    if obj_subpath is None:
        pos = obj_inst.data.root_pos_w.cpu()[env_ids] - env.scene.env_origins.cpu()[env_ids]
        rot = obj_inst.data.root_quat_w.cpu()[env_ids]
    else:
        view = RigidPrimView(
            obj_inst.cfg.prim_path + "/" + obj_subpath,
            name=f"{obj_name}_{obj_subpath}_view",
            reset_xform_properties=False,
        )
        pos, rot = view.get_world_poses(indices=env_ids)
        pos = pos - env.scene.env_origins[env_ids]
        pos = pos.cpu()
        rot = rot.cpu()

    assert pos.shape == (len(env_ids), 3)
    assert rot.shape == (len(env_ids), 4)
    return pos, rot


def joint_is_implicit_actuator(joint_name: str, obj_inst) -> bool:
    from omni.isaac.lab.actuators import ImplicitActuatorCfg
    from omni.isaac.lab.assets import Articulation

    assert isinstance(obj_inst, Articulation)
    actuators = [actuator for actuator in obj_inst.actuators.values() if joint_name in actuator.joint_names]
    if len(actuators) == 0:
        log.error(f"Joint {joint_name} could not be found in actuators of {obj_inst.cfg.prim_path}")
        return False
    if len(actuators) > 1:
        log.warning(f"Joint {joint_name} is found in multiple actuators of {obj_inst.cfg.prim_path}")
    actuator = actuators[0]
    return isinstance(actuator, ImplicitActuatorCfg)
