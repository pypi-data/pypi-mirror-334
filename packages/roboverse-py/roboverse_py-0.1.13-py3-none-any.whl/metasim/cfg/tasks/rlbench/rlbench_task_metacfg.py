from metasim.cfg.tasks import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.utils import configclass


@configclass
class RLBenchTaskMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.RLBENCH
    task_type = TaskType.TABLETOP_MANIPULATION
    can_tabletop = True
