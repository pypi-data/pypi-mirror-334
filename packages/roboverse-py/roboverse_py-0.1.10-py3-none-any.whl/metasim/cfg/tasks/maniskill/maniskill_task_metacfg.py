from metasim.cfg.tasks import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.utils import configclass


@configclass
class ManiskillTaskMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.MANISKILL
    task_type = TaskType.TABLETOP_MANIPULATION
    can_tabletop = True
