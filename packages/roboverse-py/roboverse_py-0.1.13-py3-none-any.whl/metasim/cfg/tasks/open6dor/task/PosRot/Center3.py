from metasim.cfg.objects import PrimitiveCubeMetaCfg, RigidObjMetaCfg
from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass


@configclass
class OpensdorPosRotCenterUpsideDownCup1798MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-a_cups_google_16k/065-a_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e32b159011544b8aa7cacd812636353e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/ycb_16k_backup/037_scissors_google_16k/037_scissors_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-e_cups_google_16k/065-e_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_cup_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-165453_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownCup1799MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a7785ac7ce7f4ba79df661db33637ba9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d5a5f0a954f94bcea3168329d1605fe9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de23895b6e9b4cfd870e30d14c2150dd/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-e_cups_google_16k/065-e_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_cup_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-215549_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownCup1800MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="pear",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f9ac5185507b4d0dbc744941e9055b96/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f93d05bc2db144f7a50374794ef5cf8d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9321c45cb9cf459f9f803507d3a11fb3/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_cup_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-202150_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownCup1801MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="binder clips",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e55c38b24dc4c239448efa1c6b7f49f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d6e38c73f8f2402aac890e8ebb115302/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e1a1527a0bd49ed8e473079392c31c8/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-d_cups_google_16k/065-d_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_cup_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-194619_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownCup1802MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/043_phillips_screwdriver_google_16k/043_phillips_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="speaker",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4445f4442a884999960e7e6660459095/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-f_cups_google_16k/065-f_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-e_cups_google_16k/065-e_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_cup_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-223519_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownCup1803MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d17b8f44d1544364b8ad9fe2554ddfdf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d28b249d997b46c1b42771d8ce869902/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d6951661c1e445d8a1d00b7d38d86030/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-i_cups_google_16k/065-i_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_cup_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-212155_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatBook1804MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="power drill",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/035_power_drill_google_16k/035_power_drill_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/efb1727dee214d49b88c58792e4bdffc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bf83213efac34b3cb2ad6ac5ddaf05d9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c61227cac7224b86b43c53ac2a2b6ec7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_book_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-231323_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatBook1805MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-a_cups_google_16k/065-a_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pen",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f126e15c0f904fccbd76f9348baea12c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c61227cac7224b86b43c53ac2a2b6ec7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_book_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-162847_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatBook1806MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc4c91abf45342b4bb8822f50fa162b2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e5e87ddbf3f6470384bef58431351e2a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/054be0c3f09143f38c4d8038eb2588c6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2a371c84c5454f7facba7bb2f5312ad6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_book_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-215511_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatBook1807MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="pitcher base",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/019_pitcher_base_google_16k/019_pitcher_base_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-j_cups_google_16k/065-j_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="camera",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6a63fc4af48b453c91ca2b335a4d464d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2a371c84c5454f7facba7bb2f5312ad6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_book_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-230007_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatBook1808MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f81ca566b008446eb704cad4844603b6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/073-g_lego_duplo_google_16k/073-g_lego_duplo_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pitcher base",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/019_pitcher_base_google_16k/019_pitcher_base_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2a371c84c5454f7facba7bb2f5312ad6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_book_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-164307_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatBook1809MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="fork",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/030_fork_google_16k/030_fork_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ece4453042144b4a82fb86a4eab1ba7f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbda0b25f41f40958ea984f460e4770b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c61227cac7224b86b43c53ac2a2b6ec7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_book_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-213113_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatBook1810MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/7138f5e13b2e4e17975c23ba5584164b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="flashlight",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/123a79642c2646d8b315576828fea84a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/69511a7fad2f42ee8c4b0579bbc8fec6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b2d30398ba3741da9f9aef2319ee2b8b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_book_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-162532_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatBook1811MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8891134871e48ce8cb5053c4287272b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a564a11174be455bbce4698f7da92fdf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b2d30398ba3741da9f9aef2319ee2b8b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_book_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-202139_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatBook1812MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-h_cups_google_16k/065-h_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="binder",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a0026e7d1b244b9a9223daf4223c9372/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mobile phone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/45c813a9fac4458ead1f90280826c0a4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de79a920c48745ff95c0df7a7c300091/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_book_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-161314_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatBook1813MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/010_potted_meat_can_google_16k/010_potted_meat_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8a6cb4f7b0004f53830e270dc6e1ff1d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f9d07bb386a04de8b0e1a9a28a936985/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b2d30398ba3741da9f9aef2319ee2b8b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_book_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-205014_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterBladesRightScissors1814MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d9ffbc4bbe1044bb902e1dddac52b0de/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mobile phone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/45c813a9fac4458ead1f90280826c0a4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/002_master_chef_can_google_16k/002_master_chef_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/ycb_16k_backup/037_scissors_google_16k/037_scissors_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_scissors_at_the_center_of_all_the_objects_on_the_table.__blades_right/20240824-195554_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterBladesRightScissors1815MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/7138f5e13b2e4e17975c23ba5584164b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="ladle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ce27e3369587476c85a436905f1e5c00/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9bf1b31f641543c9a921042dac3b527f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2b1120c4b517409184413ed709c57a66/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_scissors_at_the_center_of_all_the_objects_on_the_table.__blades_right/20240824-232010_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterBladesRightScissors1816MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e51e63e374ee4c25ae3fb4a9c74bd335/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="plate",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/029_plate_google_16k/029_plate_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/ycb_16k_backup/004_sugar_box_google_16k/004_sugar_box_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/ycb_16k_backup/037_scissors_google_16k/037_scissors_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_scissors_at_the_center_of_all_the_objects_on_the_table.__blades_right/20240824-225501_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterBladesRightScissors1817MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/aa51af2f1270482193471455b504efc6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2a371c84c5454f7facba7bb2f5312ad6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/ycb_16k_backup/037_scissors_google_16k/037_scissors_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_scissors_at_the_center_of_all_the_objects_on_the_table.__blades_right/20240824-163816_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterSidewaysTextualBox1818MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-f_cups_google_16k/065-f_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2c88306f3d724a839054f3c2913fb1d5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/35a76a67ea1c45edabbd5013de70d68d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/ycb_16k_backup/004_sugar_box_google_16k/004_sugar_box_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_box_at_the_center_of_all_the_objects_on_the_table.__sideways_textual/20240824-182304_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterSidewaysTextualBox1819MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/005_tomato_soup_can_google_16k/005_tomato_soup_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdb8227a88b2448d8c64fa82ffee3f58/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/efb1727dee214d49b88c58792e4bdffc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/009_gelatin_box_google_16k/009_gelatin_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_box_at_the_center_of_all_the_objects_on_the_table.__sideways_textual/20240824-192703_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterSidewaysTextualBox1820MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d1d1c4b27f5c45a29910830e268f7ee2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5172dbe9281a45f48cee8c15bdfa1831/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d499e1bc8a514e4bb5ca995ea6ba23b6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9660e0c0326b4f7386014e27717231ae/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_box_at_the_center_of_all_the_objects_on_the_table.__sideways_textual/20240824-214928_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterSidewaysTextualBox1821MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mobile phone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/45c813a9fac4458ead1f90280826c0a4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c609327dd3a74fb597584e1b4a14a615/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/85db1d392a89459dbde5cdd951c4f6fb/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/ycb_16k_backup/004_sugar_box_google_16k/004_sugar_box_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_box_at_the_center_of_all_the_objects_on_the_table.__sideways_textual/20240824-220652_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterSidewaysTextualBox1822MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d155e8051294915813e0c156e3cd6de/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/afca0b1933b84b1dbebd1244f25e72fc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/878049e8c3174fa68a56530e5aef7a5a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e1a1527a0bd49ed8e473079392c31c8/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_box_at_the_center_of_all_the_objects_on_the_table.__sideways_textual/20240824-184839_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterSidewaysTextualBox1823MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8ed38a92668a425eb16da938622d9ace/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/81b129ecf5724f63b5b044702a3140c2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b8478cea51454555b90de0fe6ba7ba83/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/008_pudding_box_google_16k/008_pudding_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_box_at_the_center_of_all_the_objects_on_the_table.__sideways_textual/20240824-211619_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownBowl1824MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/878049e8c3174fa68a56530e5aef7a5a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/aa51af2f1270482193471455b504efc6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-j_cups_google_16k/065-j_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_bowl_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-205007_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownBowl1825MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-a_toy_airplane_google_16k/072-a_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a564a11174be455bbce4698f7da92fdf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c25119c5ac6e4654be3b75d78e34a912/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_bowl_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-192522_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownBowl1826MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/022_windex_bottle_google_16k/022_windex_bottle_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="flashlight",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/123a79642c2646d8b315576828fea84a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="paperweight",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/21c10181c122474a8f72a4ad0331f185/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_bowl_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-174314_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownBowl1827MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="paperweight",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/21c10181c122474a8f72a4ad0331f185/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="fork",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/030_fork_google_16k/030_fork_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea91786392284f03809c37976da090bf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bdd36c94f3f74f22b02b8a069c8d97b7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_bowl_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-233838_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownBowl1828MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8d50c19e138b403e8b2ede9b47d8be3c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="skillet",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/027_skillet_google_16k/027_skillet_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-c_cups_google_16k/065-c_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_bowl_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-203251_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownBowl1829MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0161b6232216457aa8f4f3393960ec85/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/043_phillips_screwdriver_google_16k/043_phillips_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b1098389cc3b460bb1f1ce558d4b0764/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bf83213efac34b3cb2ad6ac5ddaf05d9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_bowl_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-215707_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownBowl1830MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-c_cups_google_16k/065-c_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="multimeter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/79ac684e66b34554ba869bd2fc3c2653/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="clock",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdf932b04e6c4e0fbd6e274563b94536/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bdd36c94f3f74f22b02b8a069c8d97b7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_bowl_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-191825_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownBowl1831MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/77d41aba53e4455f9f84fa04b175dff4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fac08019fef5474189f965bb495771eb/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2c88306f3d724a839054f3c2913fb1d5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bf83213efac34b3cb2ad6ac5ddaf05d9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_bowl_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-233148_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownBowl1832MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/794b730ae452424bb3a9ce3c6caaff7a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b4bb8bd7791648fdb36c458fd9a877bf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c25119c5ac6e4654be3b75d78e34a912/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_bowl_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-194311_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightStapler1833MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f1bbc61a42b94ee9a2976ca744f8962e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ae7142127dd84ebbbe7762368ace452c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="camera",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f6f8675406b7437faaf96a1f82062028/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="stapler",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d2c345be5c084b4e8c92b48f7be69315/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_stapler_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-200426_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightStapler1834MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/218768789fdd42bd95eb933046698499/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/69511a7fad2f42ee8c4b0579bbc8fec6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="plate",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/029_plate_google_16k/029_plate_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="stapler",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d2c345be5c084b4e8c92b48f7be69315/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_stapler_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-210816_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightStapler1835MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/002_master_chef_can_google_16k/002_master_chef_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/ycb_16k_backup/037_scissors_google_16k/037_scissors_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d499e1bc8a514e4bb5ca995ea6ba23b6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="stapler",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d2c345be5c084b4e8c92b48f7be69315/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_stapler_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-195534_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightStapler1836MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/048_hammer_google_16k/048_hammer_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b31c69728a414e639eef2fccd1c3dd75/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8891134871e48ce8cb5053c4287272b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="stapler",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d2c345be5c084b4e8c92b48f7be69315/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_stapler_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-230109_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightMouse1837MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de23895b6e9b4cfd870e30d14c2150dd/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/003_cracker_box_google_16k/003_cracker_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ae7142127dd84ebbbe7762368ace452c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f496168739384cdb86ef6d65e2068a3f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_mouse_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-173103_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightMouse1838MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="fork",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/030_fork_google_16k/030_fork_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/11307d06bb254318b95021d68c6fa12f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b4bb8bd7791648fdb36c458fd9a877bf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f017c73a85484b6da3a66ec1cda70c71/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_mouse_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-203442_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightMouse1839MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="power drill",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/035_power_drill_google_16k/035_power_drill_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2b1120c4b517409184413ed709c57a66/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0b1f7c17d70489888f5ae922169c0ce/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/969b0d9d99a8468898753fdcd219f883/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_mouse_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-213255_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightMouse1840MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-a_cups_google_16k/065-a_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e5e87ddbf3f6470384bef58431351e2a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glasses",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f632e59e1b4d4dd1b5889c3f24f5da78/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/969b0d9d99a8468898753fdcd219f883/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_mouse_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-212642_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightMouse1841MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="clock",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdf932b04e6c4e0fbd6e274563b94536/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9bf1b31f641543c9a921042dac3b527f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="paperweight",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/21c10181c122474a8f72a4ad0331f185/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e51e63e374ee4c25ae3fb4a9c74bd335/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_mouse_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-172110_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightMouse1842MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/022_windex_bottle_google_16k/022_windex_bottle_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="skillet",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/027_skillet_google_16k/027_skillet_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-a_toy_airplane_google_16k/072-a_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/969b0d9d99a8468898753fdcd219f883/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_mouse_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-222912_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightMouse1843MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/073-g_lego_duplo_google_16k/073-g_lego_duplo_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mobile phone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/45c813a9fac4458ead1f90280826c0a4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-h_cups_google_16k/065-h_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/969b0d9d99a8468898753fdcd219f883/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_mouse_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-184535_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightMouse1844MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b4bb8bd7791648fdb36c458fd9a877bf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b8478cea51454555b90de0fe6ba7ba83/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2c88306f3d724a839054f3c2913fb1d5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/969b0d9d99a8468898753fdcd219f883/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_mouse_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-174931_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightEnvelopeBox1845MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0b1f7c17d70489888f5ae922169c0ce/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/043_phillips_screwdriver_google_16k/043_phillips_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a1da12b81f034db894496c1ffc4be1f5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="envelope box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/40b28d1cbfbd4e9f9acf653b748324ee/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_envelope_box_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-195606_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterHandleRightSpatula1846MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="binder clips",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e55c38b24dc4c239448efa1c6b7f49f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d17b8f44d1544364b8ad9fe2554ddfdf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c25119c5ac6e4654be3b75d78e34a912/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/81b129ecf5724f63b5b044702a3140c2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spatula_at_the_center_of_all_the_objects_on_the_table.__handle_right/20240824-165310_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterHandleRightSpatula1847MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="highlighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fd058916fb8843c09b4a2e05e3ee894e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0b1f7c17d70489888f5ae922169c0ce/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4b27628be0804c0285d0b13dda025a0d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spatula_at_the_center_of_all_the_objects_on_the_table.__handle_right/20240824-213421_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterHandleRightSpatula1848MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0a51815f3c0941ae8312fc6917173ed6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/022_windex_bottle_google_16k/022_windex_bottle_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/010_potted_meat_can_google_16k/010_potted_meat_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/033_spatula_google_16k/033_spatula_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spatula_at_the_center_of_all_the_objects_on_the_table.__handle_right/20240824-172703_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterHandleRightSpatula1849MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f1bbc61a42b94ee9a2976ca744f8962e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a1da12b81f034db894496c1ffc4be1f5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a7785ac7ce7f4ba79df661db33637ba9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/033_spatula_google_16k/033_spatula_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spatula_at_the_center_of_all_the_objects_on_the_table.__handle_right/20240824-162703_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterHandleRightSpatula1850MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5bf781c9fd8d4121b735503b13ba2eaf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/44bb12d306864e2cb4256a61d4168942/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a37158f20ccf436483029e8295629738/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/033_spatula_google_16k/033_spatula_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spatula_at_the_center_of_all_the_objects_on_the_table.__handle_right/20240824-201349_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterHandleRightSpatula1851MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-g_cups_google_16k/065-g_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0df75457524743ec81468c916fddb930/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5bf781c9fd8d4121b735503b13ba2eaf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/81b129ecf5724f63b5b044702a3140c2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spatula_at_the_center_of_all_the_objects_on_the_table.__handle_right/20240824-181643_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLowerRimGlasses1852MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a564a11174be455bbce4698f7da92fdf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea91786392284f03809c37976da090bf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/048_hammer_google_16k/048_hammer_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glasses",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e4f348e98ceb45e3abc77da5b738f1b2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_glasses_at_the_center_of_all_the_objects_on_the_table.__lower_rim/20240824-220905_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLowerRimGlasses1853MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/7ca7ebcfad964498b49af73be442acf9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bdd36c94f3f74f22b02b8a069c8d97b7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e32b159011544b8aa7cacd812636353e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glasses",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e4f348e98ceb45e3abc77da5b738f1b2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_glasses_at_the_center_of_all_the_objects_on_the_table.__lower_rim/20240824-181317_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLowerRimGlasses1854MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/006_mustard_bottle_google_16k/006_mustard_bottle_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/77d41aba53e4455f9f84fa04b175dff4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e1a1527a0bd49ed8e473079392c31c8/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glasses",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e4f348e98ceb45e3abc77da5b738f1b2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_glasses_at_the_center_of_all_the_objects_on_the_table.__lower_rim/20240824-185806_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterSidewaysGlueGun1855MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="stapler",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d2c345be5c084b4e8c92b48f7be69315/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="highlighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fd058916fb8843c09b4a2e05e3ee894e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbda0b25f41f40958ea984f460e4770b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a1da12b81f034db894496c1ffc4be1f5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_glue_gun_at_the_center_of_all_the_objects_on_the_table.__sideways/20240824-202423_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterSidewaysGlueGun1856MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/35a76a67ea1c45edabbd5013de70d68d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calipers",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/95c967114b624291bc26bcd705aaa334/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/aa51af2f1270482193471455b504efc6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a1da12b81f034db894496c1ffc4be1f5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_glue_gun_at_the_center_of_all_the_objects_on_the_table.__sideways/20240824-182519_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterSidewaysGlueGun1857MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="orange",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a4c9a503f63e440e8d6d924d4e5c36b1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d28b249d997b46c1b42771d8ce869902/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="fork",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e98e7fb33743442383812b68608f7006/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a1da12b81f034db894496c1ffc4be1f5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_glue_gun_at_the_center_of_all_the_objects_on_the_table.__sideways/20240824-182741_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterSidewaysGlueGun1858MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a7785ac7ce7f4ba79df661db33637ba9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2c88306f3d724a839054f3c2913fb1d5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f017c73a85484b6da3a66ec1cda70c71/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a1da12b81f034db894496c1ffc4be1f5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_glue_gun_at_the_center_of_all_the_objects_on_the_table.__sideways/20240824-215000_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatHardDrive1859MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/033_spatula_google_16k/033_spatula_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f1bbc61a42b94ee9a2976ca744f8962e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="power drill",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/035_power_drill_google_16k/035_power_drill_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e32b159011544b8aa7cacd812636353e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_hard_drive_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-212953_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatHardDrive1860MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/11307d06bb254318b95021d68c6fa12f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc707f81a94e48078069c6a463f59fcf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="orange",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a4c9a503f63e440e8d6d924d4e5c36b1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8de4975c0f54c1a97203c6a674f6a39/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_hard_drive_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-162734_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatHardDrive1861MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="highlighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/25481a65cad54e2a956394ff2b2765cd/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="SD card",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/02f7f045679d402da9b9f280030821d4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="ladle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ce27e3369587476c85a436905f1e5c00/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8de4975c0f54c1a97203c6a674f6a39/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_hard_drive_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-195745_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatHardDrive1862MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="pitcher base",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/019_pitcher_base_google_16k/019_pitcher_base_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pear",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f9ac5185507b4d0dbc744941e9055b96/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/afca0b1933b84b1dbebd1244f25e72fc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8de4975c0f54c1a97203c6a674f6a39/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_hard_drive_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-161309_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRemoteControlForthRemoteControl1863MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc4c91abf45342b4bb8822f50fa162b2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-c_cups_google_16k/065-c_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="highlighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/25481a65cad54e2a956394ff2b2765cd/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/89dcd45ac1f04680b76b709357a3dba3/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_remote_control_at_the_center_of_all_the_objects_on_the_table.__remote_control_forth/20240824-203117_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRemoteControlForthRemoteControl1864MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c609327dd3a74fb597584e1b4a14a615/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/db9345f568e8499a9eac2577302b5f51/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fac08019fef5474189f965bb495771eb/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d28b249d997b46c1b42771d8ce869902/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_remote_control_at_the_center_of_all_the_objects_on_the_table.__remote_control_forth/20240824-225404_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRemoteControlForthRemoteControl1865MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="highlighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fd058916fb8843c09b4a2e05e3ee894e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f81ca566b008446eb704cad4844603b6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2bd98e8ea09f49bd85453a927011d31d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f1bbc61a42b94ee9a2976ca744f8962e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_remote_control_at_the_center_of_all_the_objects_on_the_table.__remote_control_forth/20240824-184944_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRemoteControlForthRemoteControl1866MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/44bb12d306864e2cb4256a61d4168942/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="plate",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/029_plate_google_16k/029_plate_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-f_cups_google_16k/065-f_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/89dcd45ac1f04680b76b709357a3dba3/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_remote_control_at_the_center_of_all_the_objects_on_the_table.__remote_control_forth/20240824-173514_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRemoteControlForthRemoteControl1867MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ae7142127dd84ebbbe7762368ace452c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/efb1727dee214d49b88c58792e4bdffc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d72eebbf82be48f0a53e7e8b712e6a66/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_remote_control_at_the_center_of_all_the_objects_on_the_table.__remote_control_forth/20240824-163245_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRemoteControlForthRemoteControl1868MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="organizer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4f52ebe6c8cf432986e47d8de83386ce/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="camera",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6a63fc4af48b453c91ca2b335a4d464d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/010_potted_meat_can_google_16k/010_potted_meat_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/89dcd45ac1f04680b76b709357a3dba3/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_remote_control_at_the_center_of_all_the_objects_on_the_table.__remote_control_forth/20240824-233253_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRemoteControlForthRemoteControl1869MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/922cd7d18c6748d49fe651ded8a04cf4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0b1f7c17d70489888f5ae922169c0ce/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/969b0d9d99a8468898753fdcd219f883/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f1bbc61a42b94ee9a2976ca744f8962e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_remote_control_at_the_center_of_all_the_objects_on_the_table.__remote_control_forth/20240824-183056_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatEraser1870MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/002_master_chef_can_google_16k/002_master_chef_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a564a11174be455bbce4698f7da92fdf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mixer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/990d0cb9499540fda49b1ff36be9ba26/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="eraser",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0916a69ba514ecc973b44528b9dcc43/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_eraser_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-170936_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatEraser1871MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="pen",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f126e15c0f904fccbd76f9348baea12c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pot",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/af249e607bea40cfa2f275e5e23b8283/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d17b8f44d1544364b8ad9fe2554ddfdf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="eraser",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0916a69ba514ecc973b44528b9dcc43/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_eraser_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-221925_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLyingFlatEraser1872MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6e9e9135bb5747f58d388e1e92477f02/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de79a920c48745ff95c0df7a7c300091/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="eraser",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0916a69ba514ecc973b44528b9dcc43/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_eraser_at_the_center_of_all_the_objects_on_the_table.__lying_flat/20240824-232412_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownWineglass1873MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2c88306f3d724a839054f3c2913fb1d5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f81ca566b008446eb704cad4844603b6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d1d1c4b27f5c45a29910830e268f7ee2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/afca0b1933b84b1dbebd1244f25e72fc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_wineglass_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-190613_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownWineglass1874MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8d50c19e138b403e8b2ede9b47d8be3c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4b27628be0804c0285d0b13dda025a0d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea0cf48616e34708b73c82eb7c7366ca/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/afca0b1933b84b1dbebd1244f25e72fc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_wineglass_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-224114_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUpsideDownWineglass1875MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-a_cups_google_16k/065-a_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8c0f8088a5d546c886d1b07e3f4eafae/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8a6cb4f7b0004f53830e270dc6e1ff1d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/afca0b1933b84b1dbebd1244f25e72fc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_wineglass_at_the_center_of_all_the_objects_on_the_table.__upside_down/20240824-233719_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightOrange1876MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d17b8f44d1544364b8ad9fe2554ddfdf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/922cd7d18c6748d49fe651ded8a04cf4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="binder",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a0026e7d1b244b9a9223daf4223c9372/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="orange",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a4c9a503f63e440e8d6d924d4e5c36b1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_orange_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-165557_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightOrange1877MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/025_mug_google_16k/025_mug_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc707f81a94e48078069c6a463f59fcf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b1098389cc3b460bb1f1ce558d4b0764/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="orange",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a4c9a503f63e440e8d6d924d4e5c36b1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_orange_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-174737_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightOrange1878MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="pot",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/cba3e4df7c354d22b7913d45a28a8159/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="credit card",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5de830b2cccf4fe7a2e6b400abf26ca7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/77d41aba53e4455f9f84fa04b175dff4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="orange",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a4c9a503f63e440e8d6d924d4e5c36b1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_orange_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-211902_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightLadle1879MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-c_cups_google_16k/065-c_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/aa51af2f1270482193471455b504efc6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5172dbe9281a45f48cee8c15bdfa1831/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="ladle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ce27e3369587476c85a436905f1e5c00/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_ladle_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-202332_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightLadle1880MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/878049e8c3174fa68a56530e5aef7a5a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8eda72f64e6e4443af4fdbeed07cad29/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8de4975c0f54c1a97203c6a674f6a39/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="ladle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ce27e3369587476c85a436905f1e5c00/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_ladle_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-211343_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightLadle1881MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2b1120c4b517409184413ed709c57a66/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pitcher base",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/019_pitcher_base_google_16k/019_pitcher_base_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f017c73a85484b6da3a66ec1cda70c71/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="ladle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ce27e3369587476c85a436905f1e5c00/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_ladle_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-223753_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightLadle1882MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="pear",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f9ac5185507b4d0dbc744941e9055b96/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="multimeter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/79ac684e66b34554ba869bd2fc3c2653/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a1da12b81f034db894496c1ffc4be1f5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="ladle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ce27e3369587476c85a436905f1e5c00/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_ladle_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-183444_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightSpoon1883MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="binder",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a0026e7d1b244b9a9223daf4223c9372/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c25119c5ac6e4654be3b75d78e34a912/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="power drill",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/035_power_drill_google_16k/035_power_drill_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/218768789fdd42bd95eb933046698499/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spoon_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-222906_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightSpoon1884MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8a6cb4f7b0004f53830e270dc6e1ff1d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b31c69728a414e639eef2fccd1c3dd75/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="skillet",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/027_skillet_google_16k/027_skillet_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2613c5f24bb3407da2664c410c34d523/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spoon_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-211413_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightSpoon1885MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bdd36c94f3f74f22b02b8a069c8d97b7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fac08019fef5474189f965bb495771eb/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ca4f9a92cc2f4ee98fe9332db41bf7f7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/218768789fdd42bd95eb933046698499/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spoon_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-203308_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightSpoon1886MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/35a76a67ea1c45edabbd5013de70d68d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2613c5f24bb3407da2664c410c34d523/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e51e63e374ee4c25ae3fb4a9c74bd335/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/218768789fdd42bd95eb933046698499/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spoon_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-220313_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightSpoon1887MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mobile phone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/45c813a9fac4458ead1f90280826c0a4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/afca0b1933b84b1dbebd1244f25e72fc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/044_flat_screwdriver_google_16k/044_flat_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/218768789fdd42bd95eb933046698499/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spoon_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-190323_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightSpoon1888MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/81b129ecf5724f63b5b044702a3140c2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="orange",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a4c9a503f63e440e8d6d924d4e5c36b1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2a371c84c5454f7facba7bb2f5312ad6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e1745c4aa7c046a2b5193d2d23be0192/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spoon_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-193307_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightSpoon1889MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e51e63e374ee4c25ae3fb4a9c74bd335/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-a_cups_google_16k/065-a_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-g_cups_google_16k/065-g_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/031_spoon_google_16k/031_spoon_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spoon_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-191516_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterScoopRightSpoon1890MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/db9345f568e8499a9eac2577302b5f51/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d499e1bc8a514e4bb5ca995ea6ba23b6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-f_cups_google_16k/065-f_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e1745c4aa7c046a2b5193d2d23be0192/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_spoon_at_the_center_of_all_the_objects_on_the_table.__scoop_right/20240824-190354_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightKeyboard1891MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ca4f9a92cc2f4ee98fe9332db41bf7f7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-a_toy_airplane_google_16k/072-a_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/044_flat_screwdriver_google_16k/044_flat_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/44bb12d306864e2cb4256a61d4168942/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_keyboard_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-173531_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightKeyboard1892MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea91786392284f03809c37976da090bf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/032_knife_google_16k/032_knife_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hat",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc02f9c1fd01432fadd6e7d15851dc37/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f5080a3df6d847b693c5cca415886c61/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_keyboard_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-205618_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightKeyboard1893MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de79a920c48745ff95c0df7a7c300091/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6add0a1fa81942acbb24504b130661c1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbda0b25f41f40958ea984f460e4770b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0161b6232216457aa8f4f3393960ec85/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_keyboard_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-184354_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightKeyboard1894MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="power drill",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/035_power_drill_google_16k/035_power_drill_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8891134871e48ce8cb5053c4287272b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2613c5f24bb3407da2664c410c34d523/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0161b6232216457aa8f4f3393960ec85/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_keyboard_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-232017_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterLeftToy1895MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0a51815f3c0941ae8312fc6917173ed6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d6e38c73f8f2402aac890e8ebb115302/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/218768789fdd42bd95eb933046698499/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-b_toy_airplane_google_16k/072-b_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_toy_at_the_center_of_all_the_objects_on_the_table.__left/20240824-220558_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightHotGlueGun1896MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0161b6232216457aa8f4f3393960ec85/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b8478cea51454555b90de0fe6ba7ba83/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wallet",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ccfcc4ae6efa44a2ba34c4c479be7daf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hot glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5ceec13e87774982afe825e7e74a0ce1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_hot_glue_gun_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-224159_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightHotGlueGun1897MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="pear",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f3dd3064db4f4e8880344425970cecad/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdb8227a88b2448d8c64fa82ffee3f58/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/006_mustard_bottle_google_16k/006_mustard_bottle_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hot glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5ceec13e87774982afe825e7e74a0ce1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_hot_glue_gun_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-170139_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightHotGlueGun1898MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea91786392284f03809c37976da090bf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hat",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc02f9c1fd01432fadd6e7d15851dc37/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d17b8f44d1544364b8ad9fe2554ddfdf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hot glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5ceec13e87774982afe825e7e74a0ce1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_hot_glue_gun_at_the_center_of_all_the_objects_on_the_table.__upright/20240824-214410_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRollSidewaysToiletPaperRoll1899MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-b_toy_airplane_google_16k/072-b_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pen",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f126e15c0f904fccbd76f9348baea12c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d155e8051294915813e0c156e3cd6de/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5284b842434413a17133f7bf259669/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_toilet_paper_roll_at_the_center_of_all_the_objects_on_the_table.__roll_sideways/20240824-171230_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRollSidewaysToiletPaperRoll1900MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/85db1d392a89459dbde5cdd951c4f6fb/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ece4453042144b4a82fb86a4eab1ba7f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/7ca7ebcfad964498b49af73be442acf9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_toilet_paper_roll_at_the_center_of_all_the_objects_on_the_table.__roll_sideways/20240824-162412_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRollSidewaysToiletPaperRoll1901MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0df75457524743ec81468c916fddb930/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cap",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/87e82aa304ce4571b69bdd5182549c72/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pear",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f9ac5185507b4d0dbc744941e9055b96/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5284b842434413a17133f7bf259669/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_toilet_paper_roll_at_the_center_of_all_the_objects_on_the_table.__roll_sideways/20240824-173520_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterHandleRightScrewdriver1902MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/3ea2fd4e065147048064f4c97a89fe6f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="speaker",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4445f4442a884999960e7e6660459095/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9321c45cb9cf459f9f803507d3a11fb3/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/044_flat_screwdriver_google_16k/044_flat_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_screwdriver_at_the_center_of_all_the_objects_on_the_table.__handle_right/20240824-183007_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterHandleRightScrewdriver1903MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="cap",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/87e82aa304ce4571b69bdd5182549c72/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="organizer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4f52ebe6c8cf432986e47d8de83386ce/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c25119c5ac6e4654be3b75d78e34a912/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/044_flat_screwdriver_google_16k/044_flat_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_screwdriver_at_the_center_of_all_the_objects_on_the_table.__handle_right/20240824-170033_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterHandleRightScrewdriver1904MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/243b381dcdc34316a7e78a533572d273/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0161b6232216457aa8f4f3393960ec85/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="orange",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a4c9a503f63e440e8d6d924d4e5c36b1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/043_phillips_screwdriver_google_16k/043_phillips_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_screwdriver_at_the_center_of_all_the_objects_on_the_table.__handle_right/20240824-191846_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightLensForthCamera1905MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="binder",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a0026e7d1b244b9a9223daf4223c9372/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pot",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/cba3e4df7c354d22b7913d45a28a8159/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5a4e1174dd4f5fa0a9a9076e476b91/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="camera",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f6f8675406b7437faaf96a1f82062028/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_camera_at_the_center_of_all_the_objects_on_the_table.__upright_lens_forth/20240824-230140_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightLensForthCamera1906MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="glasses",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e4f348e98ceb45e3abc77da5b738f1b2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/44bb12d306864e2cb4256a61d4168942/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/243b381dcdc34316a7e78a533572d273/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="camera",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f6f8675406b7437faaf96a1f82062028/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_camera_at_the_center_of_all_the_objects_on_the_table.__upright_lens_forth/20240824-215227_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterUprightLensForthCamera1907MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e32b159011544b8aa7cacd812636353e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-a_toy_airplane_google_16k/072-a_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="eraser",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0916a69ba514ecc973b44528b9dcc43/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="camera",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6a63fc4af48b453c91ca2b335a4d464d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_camera_at_the_center_of_all_the_objects_on_the_table.__upright_lens_forth/20240824-202113_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRightToy1908MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="wallet",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f47fdcf9615d4e94a71e6731242a4c94/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f9d07bb386a04de8b0e1a9a28a936985/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calipers",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/95c967114b624291bc26bcd705aaa334/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-a_toy_airplane_google_16k/072-a_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_toy_at_the_center_of_all_the_objects_on_the_table.__right/20240824-192609_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotCenterRightToy1909MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/022_windex_bottle_google_16k/022_windex_bottle_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2bd98e8ea09f49bd85453a927011d31d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-b_toy_airplane_google_16k/072-b_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/center/Place_the_toy_at_the_center_of_all_the_objects_on_the_table.__right/20240824-205206_no_interaction/trajectory-unified_wo_traj_v2.pkl"
