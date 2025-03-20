from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PutUmbrellaInUmbrellaStandMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/put_umbrella_in_umbrella_stand/v2"
    objects = [
        RigidObjMetaCfg(
            name="umbrella_visual",
            usd_path="roboverse_data/assets/rlbench/put_umbrella_in_umbrella_stand/umbrella_visual/usd/umbrella_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="stand_visual",
            usd_path="roboverse_data/assets/rlbench/put_umbrella_in_umbrella_stand/stand_visual/usd/stand_visual.usd",
            physics=PhysicStateType.GEOM,
        ),
    ]
    # TODO: add checker
