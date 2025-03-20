from metasim.cfg.checkers import DetectedChecker, RelativeBboxDetector
from metasim.cfg.objects import (
    RigidObjMetaCfg,
)
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass

from ...base_task_metacfg import BaseTaskMetaCfg


@configclass
class LiberoPickChocolatePuddingMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.LIBERO
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 250

    objects = [
        RigidObjMetaCfg(
            name="chocolate_pudding",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/chocolate_pudding/usd/chocolate_pudding.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/chocolate_pudding/urdf/chocolate_pudding.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/chocolate_pudding/mjcf/chocolate_pudding.xml",
        ),
        RigidObjMetaCfg(
            name="basket",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/basket/usd/basket.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/basket/urdf/basket.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/basket/mjcf/basket.xml",
        ),
        RigidObjMetaCfg(
            name="orange_juice",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/orange_juice/usd/orange_juice.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/orange_juice/urdf/orange_juice.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/orange_juice/mjcf/orange_juice.xml",
        ),
        RigidObjMetaCfg(
            name="bbq_sauce",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/bbq_sauce/usd/bbq_sauce.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/bbq_sauce/urdf/bbq_sauce.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/bbq_sauce/mjcf/bbq_sauce.xml",
        ),
        RigidObjMetaCfg(
            name="ketchup",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/ketchup/usd/ketchup.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/ketchup/urdf/ketchup.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/ketchup/mjcf/ketchup.xml",
        ),
        RigidObjMetaCfg(
            name="salad_dressing",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/salad_dressing/usd/salad_dressing.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/salad_dressing/urdf/salad_dressing.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/salad_dressing/mjcf/salad_dressing.xml",
        ),
        RigidObjMetaCfg(
            name="alphabet_soup",
            physics=PhysicStateType.RIGIDBODY,
            filepath="roboverse_data/assets/libero/COMMON/stable_hope_objects/alphabet_soup/usd/alphabet_soup.usd",
            urdf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/alphabet_soup/urdf/alphabet_soup.urdf",
            mjcf_path="roboverse_data/assets/libero/COMMON/stable_hope_objects/alphabet_soup/mjcf/alphabet_soup.xml",
        ),
    ]

    traj_filepath = (
        "roboverse_data/trajs/libero/pick_up_the_chocolate_pudding_and_place_it_in_the_basket/v2/franka_v2.pkl"
    )

    checker = DetectedChecker(
        obj_name="chocolate_pudding",
        obj_subpath=None,
        detector=RelativeBboxDetector(
            base_obj_name="basket",
            relative_pos=[0.0, 0.0, 0.07185],
            relative_quat=[1.0, 0.0, 0.0, 0.0],
            checker_lower=[-0.08, -0.08, -0.11],
            checker_upper=[0.08, 0.08, 0.05],
        ),
    )
