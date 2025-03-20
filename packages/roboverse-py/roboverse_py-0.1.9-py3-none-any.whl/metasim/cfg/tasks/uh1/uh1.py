from metasim.cfg.tasks import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.utils import configclass


@configclass
class UH1TaskMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.UH1
    task_type = TaskType.LOCOMOTION
    episode_length = 250
    objects = []


@configclass
class MabaoguoMetaCfg(UH1TaskMetaCfg):
    traj_filepath = "data_isaaclab/source_data/humanoid/maobaoguo_traj_v2.pkl"
