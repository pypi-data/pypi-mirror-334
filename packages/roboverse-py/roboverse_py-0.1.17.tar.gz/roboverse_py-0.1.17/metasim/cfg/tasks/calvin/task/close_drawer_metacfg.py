from metasim.cfg.checkers import JointPosShiftChecker
from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.utils import configclass


@configclass
class CloseDrawerMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.CALVIN
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    checker = JointPosShiftChecker(
        obj_name="table",
        joint_name="base__drawer",
        threshold=-0.12,
    )
