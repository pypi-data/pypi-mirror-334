from __future__ import annotations

import os
from typing import Literal

from loguru import logger as log
from tyro import MISSING

from metasim.utils.configclass import configclass
from metasim.utils.io_util import check_and_download
from metasim.utils.setup_util import get_robot, get_scene, get_task

from .cameras.camera import PinholeCameraMetaCfg
from .objects import BaseObjMetaCfg, PrimitiveCubeMetaCfg, PrimitiveSphereMetaCfg
from .randomization import RandomizationMetaCfg
from .render import RenderMetaCfg
from .robots.base_robot_metacfg import BaseRobotMetaCfg
from .scenes.base_scene_metacfg import SceneMetaCfg
from .tasks.base_task_metacfg import BaseTaskMetaCfg


def check_asset(obj: BaseObjMetaCfg, sim: Literal["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco"]):
    ## TODO: add a primitive base class?
    if isinstance(obj, PrimitiveCubeMetaCfg) or isinstance(obj, PrimitiveSphereMetaCfg):
        return

    if sim in ["isaaclab"]:
        check_and_download(obj.filepath)
    elif sim in ["isaacgym", "pybullet", "sapien"]:
        check_and_download(obj.urdf_path)
    elif sim in ["mujoco"]:
        check_and_download(obj.mjcf_path)


@configclass
class ScenarioMetaCfg:
    ## Config system
    task: BaseTaskMetaCfg = MISSING
    robot: BaseRobotMetaCfg = MISSING
    scene: SceneMetaCfg | None = None
    """None means no scene"""
    cameras: list[PinholeCameraMetaCfg] = []
    render: RenderMetaCfg = RenderMetaCfg()
    random: RandomizationMetaCfg = RandomizationMetaCfg()

    ## Handlers
    sim: Literal["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco"] = "isaaclab"
    renderer: Literal["isaaclab", "isaacgym", "pyrep", "pybullet", "sapien", "mujoco"] | None = None

    ## Others
    num_envs: int = 1
    try_add_table: bool = True
    object_states: bool = False
    split: Literal["train", "val", "test", "all"] = "all"
    headless: bool = False

    def __post_init__(self):
        ### Align configurations
        if (self.random.scene or self.scene is not None) and self.try_add_table:
            log.warning("try_add_table is set to False because scene randomization is enabled or a scene is specified")
            self.try_add_table = False

        ### Parse task and robot
        if isinstance(self.task, str):
            self.task = get_task(self.task)
        if isinstance(self.robot, str):
            self.robot = get_robot(self.robot)
        if isinstance(self.scene, str):
            self.scene = get_scene(self.scene)

        ### Check and download all the paths
        ## Object paths
        for obj in self.task.objects:
            check_asset(obj, self.sim)
        ## Robot paths
        check_asset(self.robot, self.sim)
        ## Scene paths
        if self.scene is not None:
            check_asset(self.scene, self.sim)
        ## Traj paths
        traj_filepath = self.task.traj_filepath
        if traj_filepath is None:
            return
        if (
            traj_filepath.find(".pkl") == -1
            and traj_filepath.find(".json") == -1
            and traj_filepath.find(".yaml") == -1
            and traj_filepath.find(".yml") == -1
        ):
            traj_filepath = os.path.join(traj_filepath, f"{self.robot.name}_v2.pkl.gz")
        check_and_download(traj_filepath)
