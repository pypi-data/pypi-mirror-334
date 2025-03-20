from metasim.cfg.tasks import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.utils import configclass


@configclass
class GAPartNetTaskMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.GAPARTNET
    task_type = TaskType.TABLETOP_MANIPULATION
    can_tabletop = True
