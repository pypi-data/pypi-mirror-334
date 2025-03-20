from __future__ import annotations

from typing import Literal

from metasim.utils.configclass import configclass


@configclass
class RenderMetaCfg:
    mode: Literal["rasterization", "raytracing", "pathtracing"] = "raytracing"
