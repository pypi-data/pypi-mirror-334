"""Sub-module containing the render configuration."""

from __future__ import annotations

from typing import Literal

from metasim.utils.configclass import configclass


@configclass
class RenderMetaCfg:
    """Render configuration."""

    mode: Literal["rasterization", "raytracing", "pathtracing"] = "raytracing"
