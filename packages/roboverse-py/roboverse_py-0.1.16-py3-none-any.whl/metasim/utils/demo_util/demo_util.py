"""Sub-module containing utilities for loading and saving trajectories."""

from __future__ import annotations

import os

from loguru import logger as log

from metasim.cfg.robots.base_robot_metacfg import BaseRobotMetaCfg
from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.sim.base import BaseSimHandler

from .demo_util_v1 import get_traj_v1
from .demo_util_v2 import get_traj_v2


def get_traj(task: BaseTaskMetaCfg, robot: BaseRobotMetaCfg, handler: BaseSimHandler | None = None):
    """Get the trajectory data.

    Args:
        task: The task cfg instance.
        robot: The robot cfg instance.
        handler: The handler instance.

    Returns:
        The trajectory data.
    """
    if task.traj_filepath.find("v2") != -1:
        log.info("Reading trajectory using v2 data format")
        if os.path.exists(task.traj_filepath):
            return get_traj_v2(task, robot)
        else:
            raise FileNotFoundError(
                "The trajectory file does not exist, please check the path or convert the trajectory file to v2 format"
            )
    else:
        log.warning("Reading trajectory using v1 data format, which is deprecated")
        assert handler is not None, "Handler is required for v1 data format"
        return get_traj_v1(task, robot, handler)
