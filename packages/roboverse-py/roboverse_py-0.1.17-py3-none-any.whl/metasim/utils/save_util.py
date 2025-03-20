"""Sub-module containing utilities for saving data."""

from __future__ import annotations

import json
import os
import pickle as pkl

import cv2
import numpy as np
import torch


def _shift_actions_to_previous_timestep(demo: list[dict[str, torch.Tensor]]):
    for i in range(len(demo) - 1):
        demo[i]["joint_qpos_target"] = demo[i + 1]["joint_qpos_target"]
    return demo


def save_demo(save_dir: str, demo: list[dict[str, torch.Tensor]]):
    """Save a demo to a directory.

    Args:
        save_dir: The directory to save the demo.
        demo: The demo to save.
    """
    ## TODO: This function needs to be updated to support rlds format
    demo = _shift_actions_to_previous_timestep(demo)
    os.makedirs(save_dir, exist_ok=True)
    for step, data_dict in enumerate(demo):
        rgb = data_dict["rgb"].numpy()  # [H, W, 3]
        cv2.imwrite(os.path.join(save_dir, f"rgb_{step:04d}.png"), rgb[..., ::-1])
        depth = data_dict["depth"].numpy()  # [H, W]
        depth_normalized = (depth - depth.min()) / (depth.max() - depth.min())
        cv2.imwrite(os.path.join(save_dir, f"depth_{step:04d}.png"), (depth_normalized * 65535).astype(np.uint16))

    jsondata = {
        ## Vision
        # TODO: support multiple cameras
        "depth_min": [d["depth"].min().item() for d in demo],
        "depth_max": [d["depth"].max().item() for d in demo],
        ## Camera
        "cam_pos": [d["cam_pos"].tolist() for d in demo],
        "cam_look_at": [d["cam_look_at"].tolist() for d in demo],
        "cam_intr": [d["cam_intr"].tolist() for d in demo],  # align with old version
        "cam_extr": [d["cam_extr"].tolist() for d in demo],  # align with old version
        ## Action
        # TODO: missing `ee_state` (`surr_ee_state`) in old version
        "joint_qpos_target": [d["joint_qpos_target"].tolist() for d in demo],
        "joint_qpos": [d["joint_qpos"].tolist() for d in demo],  # align with old version
        "robot_ee_state": [d["robot_ee_state"].tolist() for d in demo],  # align with old version
        "robot_root_state": [d["robot_root_state"].tolist() for d in demo],
        "robot_body_state": [d["robot_body_state"].tolist() for d in demo],
    }

    json.dump(jsondata, open(os.path.join(save_dir, "metadata.json"), "w"))
    pkl.dump(jsondata, open(os.path.join(save_dir, "metadata.pkl"), "wb"))
