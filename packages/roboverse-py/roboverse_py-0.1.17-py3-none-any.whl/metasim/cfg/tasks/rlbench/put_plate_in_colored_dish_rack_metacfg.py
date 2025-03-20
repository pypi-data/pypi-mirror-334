from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PutPlateInColoredDishRackMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/put_plate_in_colored_dish_rack/v2"
    objects = [
        RigidObjMetaCfg(
            name="plate_visual",
            usd_path="roboverse_data/assets/rlbench/put_plate_in_colored_dish_rack/plate_visual/usd/plate_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="dish_rack",
            usd_path="roboverse_data/assets/rlbench/put_plate_in_colored_dish_rack/dish_rack/usd/dish_rack.usd",
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="plate_stand",
            usd_path="roboverse_data/assets/rlbench/put_plate_in_colored_dish_rack/plate_stand/usd/plate_stand.usd",
            physics=PhysicStateType.GEOM,
        ),
    ]
    # TODO: add checker
