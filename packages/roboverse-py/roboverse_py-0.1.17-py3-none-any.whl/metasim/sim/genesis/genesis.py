from __future__ import annotations

from metasim.cfg.robots.base_robot_metacfg import BaseRobotMetaCfg
from metasim.cfg.scenario import ScenarioMetaCfg
from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg

from ..base import BaseSimHandler, EnvWrapper, IdentityEnvWrapper

pass
################################################################################
## Common imports ends here, below are simulator specific imports
################################################################################


import genesis as gs
import numpy as np


class GenesisHandler(BaseSimHandler):
    def __init__(self, scenario: ScenarioMetaCfg, num_envs: int = 1, headless: bool = False):
        super().__init__(scenario, num_envs, headless)
        self._task: BaseTaskMetaCfg = scenario.task
        self._robot: BaseRobotMetaCfg = scenario.robot
        self._robot_init_pose = (0, 0, 0) if not self._robot.default_position else self._robot.default_position

        self._cameras = scenario.cameras
        self._env_ids = np.arange(num_envs)

    def launch(self) -> None:
        super().launch()

        gs.init(backend=gs.cpu)

        scene = gs.Scene(show_viewer=True)
        plane = scene.add_entity(gs.morphs.Plane())
        franka = scene.add_entity(
            gs.morphs.MJCF(file="xml/franka_emika_panda/panda.xml"),
        )

        scene.build()

        for i in range(1000):
            scene.step()


GenesisEnv: type[EnvWrapper[GenesisHandler]] = IdentityEnvWrapper(GenesisHandler)
