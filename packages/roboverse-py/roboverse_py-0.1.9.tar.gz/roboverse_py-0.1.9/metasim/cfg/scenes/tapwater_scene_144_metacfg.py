from __future__ import annotations

from metasim.utils.configclass import configclass

from .base_scene_metacfg import SceneMetaCfg


@configclass
class TapwaterScene144MetaCfg(SceneMetaCfg):
    """Config class for tapwater scene"""

    name: str = "tapwater_144"
    filepath: str = "roboverse_data/scenes/arnold/144/layout.usd"
    positions: list[tuple[float, float, float]] = [
        (-2.06621, 0.8603, -0.47689),
        (-0.87213, -0.42288, 0.00183),
    ]  # XXX: only positions are randomized for now
    default_position: tuple[float, float, float] = (-2.06621, 0.8603, -0.47689)
    quat: tuple[float, float, float, float] = (0.7071068, 0.7071068, 0.0, 0.0)
    scale: tuple[float, float, float] = (0.01, 0.01, 0.01)
