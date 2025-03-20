from __future__ import annotations

from dataclasses import MISSING
from typing import Literal

import torch
from loguru import logger as log

from metasim.cfg.objects import BaseObjMetaCfg
from metasim.utils.configclass import configclass
from metasim.utils.math import euler_xyz_from_quat, matrix_from_quat, quat_from_matrix
from metasim.utils.tensor_util import tensor_to_str

from .base_checker import BaseChecker
from .detectors import BaseDetector

try:
    from metasim.sim.base import BaseSimHandler
except:
    pass


@configclass
class DetectedChecker(BaseChecker):
    obj_name: str = MISSING
    obj_subpath: str | None = None
    detector: BaseDetector = MISSING
    ignore_if_first_check_success: bool = False

    def reset(self, handler: BaseSimHandler, env_ids: list[int] | None = None):
        self._first_check = torch.ones(handler.num_envs, dtype=torch.bool)  # True
        self._ignore = torch.zeros(handler.num_envs, dtype=torch.bool)  # False
        self.detector.reset(handler, env_ids=env_ids)

    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        success = self.detector.is_detected(handler, self.obj_name, self.obj_subpath)
        if self.ignore_if_first_check_success:
            self._ignore[self._first_check & success] = True
        self._first_check[self._first_check] = False

        success[self._ignore] = False
        return success

    def get_debug_viewers(self) -> list[BaseObjMetaCfg]:
        return self.detector.get_debug_viewers()


@configclass
class JointPosChecker(BaseChecker):
    obj_name: str = MISSING
    joint_name: str = MISSING
    mode: Literal["ge", "le"] = MISSING
    radian_threshold: float = MISSING

    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        dof_pos = handler.get_dof_pos(self.obj_name, self.joint_name)
        if self.mode == "ge":
            return dof_pos >= self.radian_threshold
        elif self.mode == "le":
            return dof_pos <= self.radian_threshold
        else:
            raise ValueError(f"Invalid mode: {self.mode}")

    def get_debug_viewers(self) -> list[BaseObjMetaCfg]:
        return []


@configclass
class JointPosShiftChecker(BaseChecker):
    """
    Check if the joint with `joint_name` of the object with `obj_name` was moved more than `threshold` units.
    - `threshold` is negative for moving towards the negative direction and positive for moving towards the positive direction.
    """

    obj_name: str = MISSING
    joint_name: str = MISSING
    threshold: float = MISSING

    def reset(self, handler: BaseSimHandler, env_ids: list[int] | None = None):
        if env_ids is None:
            env_ids = list(range(handler.num_envs))

        if not hasattr(self, "init_joint_pos"):
            self.init_joint_pos = torch.zeros(handler.num_envs, dtype=torch.float32)

        self.init_joint_pos[env_ids] = handler.get_dof_pos(self.obj_name, self.joint_name, env_ids=env_ids)

    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        cur_joint_pos = handler.get_dof_pos(self.obj_name, self.joint_name)
        joint_pos_diff = cur_joint_pos - self.init_joint_pos

        log.debug(f"Joint {self.joint_name} of object {self.obj_name} moved {tensor_to_str(joint_pos_diff)} units")

        if self.threshold > 0:
            return joint_pos_diff >= self.threshold
        else:
            return joint_pos_diff <= self.threshold


@configclass
class RotationShiftChecker(BaseChecker):
    """
    Check if the object with `obj_name` was rotated more than `radian_threshold` radians around the given `axis`.
    - `radian_threshold` is negative for clockwise rotations and positive for counter-clockwise rotations.
    - `radian_threshold` should be in the range of [-pi, pi].
    - `axis` should be one of "x", "y", "z". default is "z".
    """

    ## ref: https://github.com/mees/calvin_env/blob/c7377a6485be43f037f4a0b02e525c8c6e8d24b0/calvin_env/envs/tasks.py#L54
    obj_name: str = MISSING
    radian_threshold: float = MISSING
    axis: Literal["x", "y", "z"] = "z"

    def reset(self, handler: BaseSimHandler, env_ids: list[int] | None = None):
        if env_ids is None:
            env_ids = list(range(handler.num_envs))

        if not hasattr(self, "init_quat"):
            self.init_quat = torch.zeros(handler.num_envs, 4, dtype=torch.float32)

        self.init_quat[env_ids] = handler.get_rot(self.obj_name, env_ids=env_ids)

    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        cur_quat = handler.get_rot(self.obj_name)
        init_rot_mat = matrix_from_quat(self.init_quat)
        cur_rot_mat = matrix_from_quat(cur_quat)
        rot_diff = torch.matmul(cur_rot_mat, init_rot_mat.transpose(-1, -2))
        x, y, z = euler_xyz_from_quat(quat_from_matrix(rot_diff))
        v = {"x": x, "y": y, "z": z}[self.axis]

        ## Normalize the rotation angle to be within [-pi, pi]
        v[v > torch.pi] -= 2 * torch.pi
        v[v < -torch.pi] += 2 * torch.pi
        assert ((v >= -torch.pi) & (v <= torch.pi)).all()

        log.debug(f"Object {self.obj_name} rotated {tensor_to_str(v / torch.pi * 180)} degrees around {self.axis}-axis")

        if self.radian_threshold > 0:
            return v >= self.radian_threshold
        else:
            return v <= self.radian_threshold


@configclass
class PositionShiftChecker(BaseChecker):
    """
    Check if the object with `obj_name` was moved more than `distance` meters in given `axis`.
    - `distance` is negative for moving towards the negative direction and positive for moving towards the positive direction.
    - `max_distance` is the maximum distance the object can move.
    - `axis` should be one of "x", "y", "z".
    """

    obj_name: str = MISSING
    distance: float = MISSING
    bounding_distance: float = 1e2
    axis: Literal["x", "y", "z"] = MISSING

    def reset(self, handler: BaseSimHandler, env_ids: list[int] | None = None):
        if env_ids is None:
            env_ids = list(range(handler.num_envs))

        if not hasattr(self, "init_pos"):
            self.init_pos = torch.zeros(handler.num_envs, 3, dtype=torch.float32)

        tmp = handler.get_pos(self.obj_name, env_ids=env_ids)
        assert tmp.shape == (len(env_ids), 3)
        self.init_pos[env_ids] = tmp

    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        cur_pos = handler.get_pos(self.obj_name)
        if torch.isnan(cur_pos).any():
            log.debug(f"Object {self.obj_name} moved to nan position")
            return torch.ones(cur_pos.shape[0], dtype=torch.bool)
        dim = {"x": 0, "y": 1, "z": 2}[self.axis]
        dis_diff = cur_pos - self.init_pos
        dim_diff = dis_diff[:, dim]
        tot_dis = torch.norm(dis_diff, dim=-1)
        log.debug(f"Object {self.obj_name} moved {tensor_to_str(dim_diff)} meters in {self.axis} direction")
        if self.distance > 0:
            return (dim_diff >= self.distance) * (tot_dis <= self.bounding_distance)
        else:
            return dim_diff <= self.distance


@configclass
class SlideChecker(BaseChecker):
    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        from metasim.utils.h1_utils import torso_upright

        states = handler.get_states()
        terminated = []
        for state in states:
            if torso_upright(state, handler._robot.name) < 0.6:
                terminated.append(True)
            else:
                terminated.append(False)
        return torch.tensor(terminated)


@configclass
class WalkChecker(BaseChecker):
    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        from metasim.utils.h1_utils import z_height

        states = handler.get_states()
        terminated = []
        for state in states:
            if z_height(state, handler._robot.name) < 0.2:
                terminated.append(True)
            else:
                terminated.append(False)
        return torch.tensor(terminated)


@configclass
class StandChecker(WalkChecker):
    pass


@configclass
class RunChecker(WalkChecker):
    pass


@configclass
class CrawlChecker(BaseChecker):
    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        states = handler.get_states()
        terminated = [False] * len(states)
        return torch.tensor(terminated)


@configclass
class HurdleChecker(BaseChecker):
    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        states = handler.get_states()
        terminated = [False] * len(states)
        return torch.tensor(terminated)


@configclass
class MazeChecker(BaseChecker):
    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        from metasim.utils.h1_utils import z_height

        states = handler.get_states()
        terminated = []
        for state in states:
            if z_height(state, handler._robot.name) < 0.2:
                terminated.append(True)
            else:
                terminated.append(False)
        return torch.tensor(terminated)


@configclass
class PoleChecker(BaseChecker):
    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        from metasim.utils.h1_utils import z_height

        states = handler.get_states()
        terminated = []
        for state in states:
            if z_height(state, handler._robot.name) < 0.6:
                terminated.append(True)
            else:
                terminated.append(False)
        return torch.tensor(terminated)


@configclass
class SitChecker(BaseChecker):
    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        from metasim.utils.h1_utils import z_height

        states = handler.get_states()
        terminated = []
        for state in states:
            if z_height(state, handler._robot.name) < 0.5:
                terminated.append(True)
            else:
                terminated.append(False)
        return torch.tensor(terminated)


@configclass
class BalanceChecker(BaseChecker):
    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        from metasim.utils.h1_utils import z_height

        states = handler.get_states()
        terminated = []
        for state in states:
            if z_height(state, handler._robot.name) < 0.8:
                terminated.append(True)
            else:
                terminated.append(False)
        return torch.tensor(terminated)


@configclass
class StairChecker(BaseChecker):
    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        from metasim.utils.h1_utils import torso_upright

        states = handler.get_states()
        terminated = []
        for state in states:
            if torso_upright(state, handler._robot.name) < 0.1:
                terminated.append(True)
            else:
                terminated.append(False)
        return torch.tensor(terminated)


@configclass
class PushChecker(BaseChecker):
    def check(self, handler: BaseSimHandler) -> torch.BoolTensor:
        states = handler.get_states()
        terminated = []

        for state in states:
            # Get box position
            box_pos = state["object"]["pos"]

            # Get destination position
            dest_pos = state["destination"]["pos"]

            # Calculate distance between box and destination
            dgoal = torch.norm(box_pos - dest_pos)

            # Terminate when dgoal < 0.05 (success)
            if dgoal < 0.05:
                terminated.append(True)
            else:
                terminated.append(False)

        return torch.tensor(terminated)
