from metasim.cfg.objects import PrimitiveCubeMetaCfg
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass

from ..base_task_metacfg import BaseTaskMetaCfg


@configclass
class StackD0MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.ROBOSUITE
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 200
    traj_filepath = "data_isaaclab/source_data/robosuite/stack_d0/stack_d0_v2.pkl"
    objects = [
        PrimitiveCubeMetaCfg(
            name="cubeA", size=[0.02, 0.02, 0.02], mass=0.02, physics=PhysicStateType.RIGIDBODY, color=[1.0, 0.0, 0.0]
        ),
        PrimitiveCubeMetaCfg(
            name="cubeB",
            size=[0.025, 0.025, 0.025],
            mass=0.02,
            physics=PhysicStateType.RIGIDBODY,
            color=[0.0, 1.0, 0.0],
        ),
        PrimitiveCubeMetaCfg(
            name="table",
            # texture = 'data_isaaclab/robosuite/textures/ceramic.png',
            size=[0.8, 0.8, 0.05],
            physics=PhysicStateType.GEOM,
            color=[1.0, 1.0, 1.0],
        ),
    ]
