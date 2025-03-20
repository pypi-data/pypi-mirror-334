from metasim.cfg.objects import ArticulationObjMetaCfg
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class OpenWashingMachineMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/open_washing_machine/v2"
    objects = [
        ArticulationObjMetaCfg(
            name="washer",
            usd_path="roboverse_data/assets/rlbench/open_washing_machine/washer/usd/washer.usd",
        ),
    ]
    # TODO: add checker
