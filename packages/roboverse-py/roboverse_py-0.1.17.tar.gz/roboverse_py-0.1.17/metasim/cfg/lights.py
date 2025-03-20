"""Configuration classes for lights used in the simulation."""

from __future__ import annotations

import math

import torch

from metasim.utils import configclass
from metasim.utils.math import quat_from_euler_xyz


@configclass
class BaseLightMetaCfg:
    """Base configuration for a light."""

    intensity: float = 500.0
    """Intensity of the light"""
    color: tuple[float, float, float] = (1.0, 1.0, 1.0)
    """Color of the light"""


@configclass
class DistantLightMetaCfg(BaseLightMetaCfg):
    """Configuration for a distant light. The default direction is (0, 0, -1), pointing towards Z- direction."""

    polar: float = 0.0
    """Polar angle of the light (in degrees). Default is 0, which means the light is pointing towards Z- direction."""
    azimuth: float = 0.0
    """Azimuth angle of the light (in degrees). Default is 0."""

    @property
    def quat(self) -> tuple[float, float, float, float]:
        """Quaternion of the light direction. (1, 0, 0, 0) means the light is pointing towards Z- direction."""
        roll = torch.tensor(self.polar / 180.0 * math.pi)
        pitch = torch.tensor(0.0)
        yaw = torch.tensor(self.azimuth / 180.0 * math.pi)
        return tuple(quat_from_euler_xyz(roll, pitch, yaw).squeeze(0).tolist())


@configclass
class CylinderLightMetaCfg(BaseLightMetaCfg):
    """Configuration for a cylinder light."""

    length: float = 1.0
    """Length of the cylinder (in m). Default is 1.0m."""
    radius: float = 0.5
    """Radius of the cylinder (in m). Default is 0.5m."""
    pos: tuple[float, float, float] = (0.0, 0.0, 0.0)
    """Position of the cylinder (in m). Default is (0.0, 0.0, 0.0)."""
    rot: tuple[float, float, float, float] = (1.0, 0.0, 0.0, 0.0)
    """Orientation of the cylinder. Default is (1.0, 0.0, 0.0, 0.0)."""
