from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PutGroceriesInCupboardMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/put_groceries_in_cupboard/v2"
    objects = [
        RigidObjMetaCfg(
            name="cupboard",
            filepath="roboverse_data/assets/rlbench/put_groceries_in_cupboard/cupboard/usd/cupboard.usd",
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="chocolate_jello_visual",
            filepath="roboverse_data/assets/rlbench/put_groceries_in_cupboard/chocolate_jello_visual/usd/chocolate_jello_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="strawberry_jello_visual",
            filepath="roboverse_data/assets/rlbench/put_groceries_in_cupboard/strawberry_jello_visual/usd/strawberry_jello_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spam_visual",
            filepath="roboverse_data/assets/rlbench/put_groceries_in_cupboard/spam_visual/usd/spam_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="sugar_visual",
            filepath="roboverse_data/assets/rlbench/put_groceries_in_cupboard/sugar_visual/usd/sugar_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="crackers_visual",
            filepath="roboverse_data/assets/rlbench/put_groceries_in_cupboard/crackers_visual/usd/crackers_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mustard_visual",
            filepath="roboverse_data/assets/rlbench/put_groceries_in_cupboard/mustard_visual/usd/mustard_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="soup_visual",
            filepath="roboverse_data/assets/rlbench/put_groceries_in_cupboard/soup_visual/usd/soup_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tuna_visual",
            filepath="roboverse_data/assets/rlbench/put_groceries_in_cupboard/tuna_visual/usd/tuna_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="coffee_visual",
            filepath="roboverse_data/assets/rlbench/put_groceries_in_cupboard/coffee_visual/usd/coffee_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
