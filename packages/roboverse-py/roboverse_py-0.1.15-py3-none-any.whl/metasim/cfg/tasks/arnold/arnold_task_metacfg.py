from metasim.cfg.tasks import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.utils import configclass


@configclass
class ArnoldTaskMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.ARNOLD
    task_type = TaskType.TABLETOP_MANIPULATION
    can_tabletop = False
