from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class SetTheTableMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 1200
    traj_filepath = "roboverse_data/trajs/rlbench/set_the_table/v2"
    objects = [
        RigidObjMetaCfg(
            name="holder",
            usd_path="roboverse_data/assets/rlbench/set_the_table/holder/usd/holder.usd",
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="fork_visual",
            usd_path="roboverse_data/assets/rlbench/set_the_table/fork_visual/usd/fork_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife_visual",
            usd_path="roboverse_data/assets/rlbench/set_the_table/knife_visual/usd/knife_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon_visual",
            usd_path="roboverse_data/assets/rlbench/set_the_table/spoon_visual/usd/spoon_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="plate_visual",
            usd_path="roboverse_data/assets/rlbench/set_the_table/plate_visual/usd/plate_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glass_visual",
            usd_path="roboverse_data/assets/rlbench/set_the_table/glass_visual/usd/glass_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
