from metasim.cfg.checkers import DetectedChecker, RelativeBboxDetector
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass

from ...base_task_metacfg import BaseTaskMetaCfg


@configclass
class LiberoPickCreamCheeseMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.LIBERO
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 250

    objects = [
        RigidObjMetaCfg(
            name="cream_cheese",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/cream_cheese/usd/cream_cheese.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/cream_cheese/urdf/cream_cheese.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/cream_cheese/mjcf/cream_cheese.xml",
        ),
        RigidObjMetaCfg(
            name="basket",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/basket/usd/basket.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/basket/urdf/basket.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/basket/mjcf/basket.xml",
        ),
        RigidObjMetaCfg(
            name="alphabet_soup",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/alphabet_soup/usd/alphabet_soup.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/alphabet_soup/urdf/alphabet_soup.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/alphabet_soup/mjcf/alphabet_soup.xml",
        ),
        RigidObjMetaCfg(
            name="milk",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/milk/usd/milk.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/milk/urdf/milk.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/milk/mjcf/milk.xml",
        ),
        RigidObjMetaCfg(
            name="tomato_sauce",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/tomato_sauce/usd/tomato_sauce.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/tomato_sauce/urdf/tomato_sauce.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/tomato_sauce/mjcf/tomato_sauce.xml",
        ),
        RigidObjMetaCfg(
            name="butter",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/butter/usd/butter.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/butter/urdf/butter.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/butter/mjcf/butter.xml",
        ),
        RigidObjMetaCfg(
            name="orange_juice",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/orange_juice/usd/orange_juice.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/orange_juice/urdf/orange_juice.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/orange_juice/mjcf/orange_juice.xml",
        ),
    ]

    traj_filepath = "roboverse_data/trajs/libero/pick_up_the_cream_cheese_and_place_it_in_the_basket/v2/franka_v2.pkl"

    checker = DetectedChecker(
        obj_name="cream_cheese",
        obj_subpath=None,
        detector=RelativeBboxDetector(
            base_obj_name="basket",
            relative_pos=[0.0, 0.0, 0.07185],
            relative_quat=[1.0, 0.0, 0.0, 0.0],
            checker_lower=[-0.08, -0.08, -0.11],
            checker_upper=[0.08, 0.08, 0.05],
        ),
    )
