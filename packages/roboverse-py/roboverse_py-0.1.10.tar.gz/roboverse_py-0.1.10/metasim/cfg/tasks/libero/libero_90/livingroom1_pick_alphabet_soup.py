from metasim.cfg.checkers import DetectedChecker, RelativeBboxDetector
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import BenchmarkType, TaskType
from metasim.utils import configclass

from ...base_task_metacfg import BaseTaskMetaCfg


@configclass
class Livingroom1PickAlphabetSoupMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.LIBERO
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 250

    objects = [
        RigidObjMetaCfg(
            name="alphabet_soup",
            filepath="data_isaaclab/assets/rlbench/close_box/box_base.usd",
            urdf_path="data_isaaclab/assets/rlbench_urdf/close_box/box_base_unique.urdf",
            mjcf_path="data_isaaclab/assets_mujoco/libero/stable_hope_objects/alphabet_soup/alphabet_soup.xml",
        ),
        RigidObjMetaCfg(
            name="basket",
            filepath="data_isaaclab/assets/rlbench/close_box/box_base.usd",
            urdf_path="data_isaaclab/assets/rlbench_urdf/close_box/box_base_unique.urdf",
            mjcf_path="data_isaaclab/assets_mujoco/libero/stable_scanned_objects/basket/basket.xml",
        ),
        RigidObjMetaCfg(
            name="cream_cheese",
            filepath="data_isaaclab/assets/rlbench/close_box/box_base.usd",
            urdf_path="data_isaaclab/assets/rlbench_urdf/close_box/box_base_unique.urdf",
            mjcf_path="data_isaaclab/assets_mujoco/libero/stable_hope_objects/cream_cheese/cream_cheese.xml",
        ),
        RigidObjMetaCfg(
            name="tomato_sauce",
            filepath="data_isaaclab/assets/rlbench/close_box/box_base.usd",
            urdf_path="data_isaaclab/assets/rlbench_urdf/close_box/box_base_unique.urdf",
            mjcf_path="data_isaaclab/assets_mujoco/libero/stable_hope_objects/tomato_sauce/tomato_sauce.xml",
        ),
        RigidObjMetaCfg(
            name="ketchup",
            filepath="data_isaaclab/assets/rlbench/close_box/box_base.usd",
            urdf_path="data_isaaclab/assets/rlbench_urdf/close_box/box_base_unique.urdf",
            mjcf_path="data_isaaclab/assets_mujoco/libero/stable_hope_objects/ketchup/ketchup.xml",
        ),
        RigidObjMetaCfg(
            name="livingroom_table",
            filepath="data_isaaclab/assets/rlbench/close_box/box_base.usd",
            urdf_path="data_isaaclab/assets/rlbench_urdf/close_box/box_base_unique.urdf",
            mjcf_path="data_isaaclab/assets_mujoco/libero/scenes/libero_living_room_tabletop_base_style.xml",
        ),
    ]

    traj_filepath = "data_isaaclab/source_data/libero_tasks/libero_objects/pick_up_the_alphabet_soup_and_place_it_in_the_basket/trajectory-unified_with_object_states_v2.pkl"

    checker = DetectedChecker(
        obj_name="alphabet_soup",
        obj_subpath=None,
        detector=RelativeBboxDetector(
            base_obj_name="basket",
            relative_pos=[0.0, 0.0, 0.07185],
            relative_quat=[1.0, 0.0, 0.0, 0.0],
            checker_lower=[-0.05, -0.05, -0.05],
            checker_upper=[0.05, 0.05, 0.05],
            debug_vis=True,
        ),
    )
