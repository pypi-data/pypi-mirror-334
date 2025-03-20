"""Sub-module containing the camera configuration."""

from __future__ import annotations

import math
from dataclasses import MISSING
from typing import Literal

from metasim.utils.configclass import configclass


@configclass
class PinholeCameraMetaCfg:
    """Pinhole camera configuration."""

    name: str = MISSING
    data_types: list[Literal["rgb", "depth"]] = MISSING
    width: int = MISSING
    height: int = MISSING
    pos: tuple[float, float, float] = MISSING
    look_at: tuple[float, float, float] = MISSING

    ## Pinhole Camera
    focal_length: float = 24  # same as Isaac Sim 2023.1 version, same as IsaacLab default
    focus_distance: float = 400.0  # same as Isaac Sim 2023.1 version, same as IsaacLab default
    horizontal_aperture: float = 20.955  # same as Isaac Sim 2023.1 version, same as IsaacLab default
    clipping_range: tuple[float, float] = (0.05, 1e5)  # same as Isaac Sim 2023.1 version

    @property
    def vertical_aperture(self) -> float:
        """Vertical aperture."""
        return self.horizontal_aperture * self.height / self.width

    @property
    def horizontal_fov(self) -> float:
        """Horizontal field of view, in degrees."""
        return 2 * math.atan(self.horizontal_aperture / (2 * self.focal_length)) / math.pi * 180

    @property
    def vertical_fov(self) -> float:
        """Vertical field of view, in degrees."""
        return 2 * math.atan(self.vertical_aperture / (2 * self.focal_length)) / math.pi * 180
