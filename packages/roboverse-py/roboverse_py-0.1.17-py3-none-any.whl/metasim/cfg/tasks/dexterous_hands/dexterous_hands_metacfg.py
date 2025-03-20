from metasim.cfg.tasks import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.utils import configclass


@configclass
class DexterousHandsTaskMetaCfg(BaseTaskMetaCfg):
    """Dexterous Hands Task Meta Configuration."""

    source_benchmark = BenchmarkType.DEXTEROUS_HANDS
    task_type = TaskType.DEXTEROUS_HANDS
    can_tabletop = False
