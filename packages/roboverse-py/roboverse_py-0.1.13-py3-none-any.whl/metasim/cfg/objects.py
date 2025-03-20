from __future__ import annotations

import math
from dataclasses import MISSING

from metasim.constants import PhysicStateType
from metasim.utils import configclass


@configclass
class BaseObjMetaCfg:
    name: str = MISSING
    fix_base_link: bool = False
    scale: float = 1.0


# File-based object
@configclass
class RigidObjMetaCfg(BaseObjMetaCfg):
    filepath: str | None = None
    urdf_path: str | None = None
    mjcf_path: str | None = None
    mesh_path: str | None = None
    physics: PhysicStateType = MISSING


@configclass
class NonConvexRigidObjMetaCfg(RigidObjMetaCfg):
    mesh_pose: list[float] = MISSING


@configclass
class ArticulationObjMetaCfg(BaseObjMetaCfg):
    filepath: str | None = None
    urdf_path: str | None = None
    mjcf_path: str | None = None


# Primitive object are all rigid objects
@configclass
class PrimitiveCubeMetaCfg(RigidObjMetaCfg):
    mass: float = 0.1
    color: list[float] = MISSING
    size: list[float] = MISSING
    physics: PhysicStateType = MISSING
    mjcf_path: str | None = None  # TODO: remove this field

    @property
    def half_size(self) -> list[float]:
        """
        For SAPIEN usage
        """
        return [size / 2 for size in self.size]

    @property
    def density(self) -> float:
        """
        For SAPIEN usage
        """
        return self.mass / (self.size[0] * self.size[1] * self.size[2])


@configclass
class PrimitiveSphereMetaCfg(RigidObjMetaCfg):
    mass: float = 0.1
    color: list[float] = MISSING
    radius: float = MISSING
    physics: PhysicStateType = MISSING

    @property
    def density(self) -> float:
        """
        For SAPIEN usage
        """
        return self.mass / (4 / 3 * math.pi * self.radius**3)
