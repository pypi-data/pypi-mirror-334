"""This file contains the basic types for the MetaSim."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict

import torch

## Basic types
Dof = Dict[str, float]


## Trajectory types
class Action(TypedDict):
    """Action of the robot."""

    dof_pos_target: Dof


EnvState = Dict[
    str,
    TypedDict(
        "ObjState",
        {
            "pos": torch.Tensor,
            "rot": torch.Tensor,
            "vel": Optional[torch.Tensor],
            "ang_vel": Optional[torch.Tensor],
            "dof_pos": Dof,
            "dof_vel": Optional[Dof],
            "dof_pos_target": Optional[Dof],
            "dof_vel_target": Optional[Dof],
            "dof_torque": Optional[Dof],
            "com": Optional[torch.Tensor],
            "com_vel": Optional[torch.Tensor],
        },
    ),
]


## Gymnasium types
class Obs(TypedDict):
    """Observation of the environment."""

    rgb: torch.Tensor
    depth: torch.Tensor
    states: list[EnvState]


Reward = List[List[float]]  # TODO: you may modify this if necessary
Success = torch.BoolTensor
TimeOut = torch.BoolTensor
Extra = Dict[str, Any]  # XXX
Termination = torch.BoolTensor
