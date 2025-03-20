"""Configuration for the Libero pick butter task."""

from metasim.cfg.checkers import DetectedChecker, RelativeBboxDetector
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass

from ...base_task_metacfg import BaseTaskMetaCfg


@configclass
class LiberoPickButterMetaCfg(BaseTaskMetaCfg):
    """Configuration for the Libero pick butter task.

    This task is transferred from https://github.com/Lifelong-Robot-Learning/LIBERO/blob/master/libero/libero/bddl_files/libero_object/pick_up_the_butter_and_place_it_in_the_basket.bddl
    """

    source_benchmark = BenchmarkType.LIBERO
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 250

    objects = [
        RigidObjMetaCfg(
            name="butter",
            physics=PhysicStateType.RIGIDBODY,
            usd_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/butter/usd/butter.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/butter/urdf/butter.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/butter/mjcf/butter.xml",
        ),
        RigidObjMetaCfg(
            name="basket",
            physics=PhysicStateType.RIGIDBODY,
            usd_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/basket/usd/basket.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/basket/urdf/basket.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/basket/mjcf/basket.xml",
        ),
        RigidObjMetaCfg(
            name="tomato_sauce",
            physics=PhysicStateType.RIGIDBODY,
            usd_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/tomato_sauce/usd/tomato_sauce.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/tomato_sauce/urdf/tomato_sauce.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/tomato_sauce/mjcf/tomato_sauce.xml",
        ),
        RigidObjMetaCfg(
            name="orange_juice",
            physics=PhysicStateType.RIGIDBODY,
            usd_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/orange_juice/usd/orange_juice.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/orange_juice/urdf/orange_juice.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/orange_juice/mjcf/orange_juice.xml",
        ),
        RigidObjMetaCfg(
            name="chocolate_pudding",
            physics=PhysicStateType.RIGIDBODY,
            usd_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/chocolate_pudding/usd/chocolate_pudding.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/chocolate_pudding/urdf/chocolate_pudding.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/chocolate_pudding/mjcf/chocolate_pudding.xml",
        ),
        RigidObjMetaCfg(
            name="bbq_sauce",
            physics=PhysicStateType.RIGIDBODY,
            usd_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/bbq_sauce/usd/bbq_sauce.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/bbq_sauce/urdf/bbq_sauce.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/bbq_sauce/mjcf/bbq_sauce.xml",
        ),
        RigidObjMetaCfg(
            name="ketchup",
            physics=PhysicStateType.RIGIDBODY,
            usd_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/ketchup/usd/ketchup.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/ketchup/urdf/ketchup.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/ketchup/mjcf/ketchup.xml",
        ),
    ]

    traj_filepath = "roboverse_data/trajs/libero/pick_up_the_butter_and_place_it_in_the_basket/v2/franka_v2.pkl"

    checker = DetectedChecker(
        obj_name="butter",
        detector=RelativeBboxDetector(
            base_obj_name="basket",
            relative_pos=[0.0, 0.0, 0.07185],
            relative_quat=[1.0, 0.0, 0.0, 0.0],
            checker_lower=[-0.08, -0.08, -0.11],
            checker_upper=[0.08, 0.08, 0.05],
        ),
    )
