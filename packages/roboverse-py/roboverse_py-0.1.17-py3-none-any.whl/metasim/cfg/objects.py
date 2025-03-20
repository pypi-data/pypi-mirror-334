"""Configuration classes for various types of objects used in the simulation.

Configurations include the object name, source file, geometries (scaling, radius, etc.),
and physics (mass, density, etc.).
"""

from __future__ import annotations

import math
from dataclasses import MISSING

from metasim.constants import PhysicStateType
from metasim.utils import configclass


@configclass
class BaseObjMetaCfg:
    """Base class for object metacfg."""

    name: str = MISSING
    """Object name"""
    fix_base_link: bool = False
    """Whether to fix the base link of the object, default is False"""
    scale: float = 1.0
    """Object scaling (in scalar) for the object, default is 1.0"""


# File-based object
@configclass
class RigidObjMetaCfg(BaseObjMetaCfg):
    """Rigid object metacfg.

    The file source should be specified, from a USD, URDF, MJCF, or mesh file,
    with the path specified by the members below.

    Attributes:
        usd_path: Path to the USD file
        urdf_path: Path to the URDF file
        mjcf_path: Path to the MJCF file
        mesh_path: Path to the Mesh file
        physics: Specify the physics APIs applied on the object
    """

    usd_path: str | None = None
    urdf_path: str | None = None
    mjcf_path: str | None = None
    mesh_path: str | None = None
    physics: PhysicStateType = MISSING


@configclass
class NonConvexRigidObjMetaCfg(RigidObjMetaCfg):
    """Non-convex rigid object class."""

    mesh_pose: list[float] = MISSING


@configclass
class ArticulationObjMetaCfg(BaseObjMetaCfg):
    """Articulation object metacfg."""

    usd_path: str | None = None
    urdf_path: str | None = None
    mjcf_path: str | None = None


# Primitive object are all rigid objects
@configclass
class PrimitiveCubeMetaCfg(RigidObjMetaCfg):
    """Primitive cube object metacfg.

    This class specifies configuration parameters of a primitive cube.

    Attributes:
        mass: Mass of the object, in kg, default is 0.1
        color: Color of the object in RGB
        size: Size of the object, extent in m
    """

    mass: float = 0.1
    color: list[float] = MISSING
    size: list[float] = MISSING
    physics: PhysicStateType = MISSING
    mjcf_path: str | None = None  # TODO: remove this field

    @property
    def half_size(self) -> list[float]:
        """Half of the extend, for SAPIEN usage."""
        return [size / 2 for size in self.size]

    @property
    def density(self) -> float:
        """Object density, for SAPIEN usage."""
        return self.mass / (self.size[0] * self.size[1] * self.size[2])


@configclass
class PrimitiveSphereMetaCfg(RigidObjMetaCfg):
    """Primitive sphere object metacfg."""

    mass: float = 0.1
    color: list[float] = MISSING
    radius: float = MISSING
    physics: PhysicStateType = MISSING

    @property
    def density(self) -> float:
        """For SAPIEN usage."""
        return self.mass / (4 / 3 * math.pi * self.radius**3)


@configclass
class PrimitiveCylinderMetaCfg(RigidObjMetaCfg):
    """Primitive cylinder object metacfg."""

    mass: float = 0.1
    color: list[float] = MISSING
    radius: float = MISSING
    height: float = MISSING
    physics: PhysicStateType = MISSING

    @property
    def density(self) -> float:
        """For SAPIEN usage."""
        return self.mass / (math.pi * self.radius**2 * self.height)
