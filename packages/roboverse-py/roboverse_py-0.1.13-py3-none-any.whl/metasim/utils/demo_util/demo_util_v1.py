from __future__ import annotations

import pickle as pkl

import numpy as np
import torch

from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.cfg.robots.base_robot_metacfg import BaseRobotMetaCfg
from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.sim.base import BaseSimHandler


def get_traj_v1(task: BaseTaskMetaCfg, robot: BaseRobotMetaCfg, handler: BaseSimHandler):
    assert type(handler).__name__ == "IsaaclabHandler", "Only IsaaclabHandler is supported for v1 trajectory reading"
    demo_original = pkl.load(open(task.traj_filepath, "rb"))["demos"][robot.name]
    init_states = get_init_states(demo_original, len(demo_original), task, handler, robot)
    all_actions = get_actions(demo_original, robot, handler)
    all_states = get_all_states(demo_original, task, handler, robot)
    return init_states, all_actions, all_states


def get_actions(demo_original, robot: BaseRobotMetaCfg, handler: BaseSimHandler):
    all_actions = []
    for demo_idx in range(len(demo_original)):
        actions = []
        for action_idx in range(demo_original[demo_idx]["robot_traj"]["q"].shape[0]):
            dof_pos_target = {}
            dof_array = demo_original[demo_idx]["robot_traj"]["q"][action_idx]
            for i, joint_name in enumerate(handler.get_object_joint_names(robot)):
                value = dof_array[i]
                if type(value) is np.ndarray:
                    value = value.item()
                elif type(value) is np.float32:
                    value = float(value)
                dof_pos_target[joint_name] = value
            action = {
                "dof_pos_target": dof_pos_target,
            }
            actions.append(action)
        all_actions.append(actions)
    return all_actions


def get_init_states(demo_original: list[dict], num_envs: int, task, handler, robot):
    dds = []
    for i in range(num_envs):
        dd = {}
        ## Objects
        for obj in task.objects:
            d = {}
            d["pos"] = demo_original[i]["env_setup"][f"init_{obj.name}_pos"].copy()
            d["rot"] = demo_original[i]["env_setup"][f"init_{obj.name}_quat"]
            dof = {}
            if isinstance(obj, ArticulationObjMetaCfg):
                for joint_name in handler.get_object_joint_names(obj):
                    value = demo_original[i]["env_setup"][f"init_{joint_name}_q"]
                    if type(value) is np.ndarray:
                        value = value.item()
                    elif type(value) is np.float32:
                        value = float(value)
                    dof[joint_name] = value
                d["dof_pos"] = dof
            dd[obj.name] = d

        ## Robot
        d = {}
        d["pos"] = demo_original[i]["env_setup"]["init_robot_pos"]
        d["rot"] = demo_original[i]["env_setup"]["init_robot_quat"]
        dof = {}
        dof_array = demo_original[i]["env_setup"]["init_q"]
        for i, joint_name in enumerate(handler.get_object_joint_names(robot)):
            value = dof_array[i]
            if type(value) is np.ndarray:
                value = value.item()
            elif type(value) is np.float32:
                value = float(value)
            dof[joint_name] = value
        d["dof_pos"] = dof
        dd[robot.name] = d

        for k, d in dd.items():
            for kk in ["pos", "rot"]:
                if type(d[kk]) is np.ndarray:
                    dd[k][kk] = torch.from_numpy(d[kk])

        dds.append(dd)
    return dds


def get_all_states(demo_original, task: BaseTaskMetaCfg, handler: BaseSimHandler, robot: BaseRobotMetaCfg):
    if demo_original[0].get("object_states", None) is None:
        return None

    all_states = []
    for demo_idx in range(len(demo_original)):
        states = []
        for i in range(len(demo_original[demo_idx]["object_states"])):
            state = {}

            ## Objects
            for obj in task.objects:
                obj_state = {}
                obj_state["pos"] = demo_original[demo_idx]["object_states"][i][f"{obj.name}_pos"].copy()
                obj_state["rot"] = demo_original[demo_idx]["object_states"][i][f"{obj.name}_quat"]

                if isinstance(obj, ArticulationObjMetaCfg):
                    dof = {}
                    for joint_name in handler.get_object_joint_names(obj):
                        value = demo_original[demo_idx]["object_states"][i][f"{joint_name}_q"]
                        if type(value) is np.ndarray:
                            value = value.item()
                        elif type(value) is np.float32 or type(value) is np.float64:
                            value = float(value)
                        dof[joint_name] = value
                    obj_state["dof_pos"] = dof
                state[obj.name] = obj_state

            ## Robot
            robot_state = {}
            robot_state["pos"] = demo_original[demo_idx]["env_setup"]["init_robot_pos"]
            robot_state["rot"] = demo_original[demo_idx]["env_setup"]["init_robot_quat"]
            dof = {}
            for j, joint_name in enumerate(handler.get_object_joint_names(robot)):
                value = demo_original[demo_idx]["robot_traj"]["q"][i][j]
                if type(value) is np.ndarray:
                    value = value.item()
                elif type(value) is np.float32 or type(value) is np.float64:
                    value = float(value)
                dof[joint_name] = value
            robot_state["dof_pos"] = dof
            state[robot.name] = robot_state

            for k, obj_state in state.items():
                for kk in ["pos", "rot"]:
                    if type(obj_state[kk]) is np.ndarray:
                        state[k][kk] = torch.from_numpy(obj_state[kk])
            states.append(state)

        all_states.append(states)
    return all_states
