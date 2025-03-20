import unittest

from metasim.cfg.cameras import PinholeCameraMetaCfg
from metasim.cfg.scenario import ScenarioMetaCfg
from metasim.constants import SimType
from metasim.scripts.replay_demo import get_states
from metasim.utils.demo_util import get_traj
from metasim.utils.setup_util import get_sim_env_class


def do_all_tests(task, simulator, robot):
    camera = PinholeCameraMetaCfg(
        name="camera",
        data_types=["rgb", "depth"],
        width=256,
        height=256,
        pos=(1.5, -1.5, 1.5),  # near
        # pos=(12.0, -12.0, 20.0),  # far
        look_at=(0.0, 0.0, 0.0),
    )
    scenario = ScenarioMetaCfg(
        task=task,
        robot=robot,
        cameras=[camera],
        sim=simulator,
    )
    env_class = get_sim_env_class(SimType(scenario.sim))
    env = env_class(scenario, 1)

    init_states, all_actions, all_states = get_traj(scenario.task, scenario.robot, env.handler)

    for i in range(100):
        states = get_states(all_states, i, 1)
        env.handler.set_states(states)
        env.handler.refresh_render()

    env.handler.close()


# Test case to detect runtime errors
class SimulatorRuntimeErrors(unittest.TestCase):
    testing_task = "close_box"
    testing_robot = "franka"

    def test_pybullet(self):
        do_all_tests(self.testing_task, "pybullet", self.testing_robot)

    def test_mujoco(self):
        do_all_tests(self.testing_task, "mujoco", self.testing_robot)


class TaskRuntimeErrors(unittest.TestCase):
    def test_rlbench(self):
        do_all_tests("close_box", "pybullet", "franka")

    def test_basic(self):
        do_all_tests("pick_cube", "pybullet", "franka")


unittest.main()
