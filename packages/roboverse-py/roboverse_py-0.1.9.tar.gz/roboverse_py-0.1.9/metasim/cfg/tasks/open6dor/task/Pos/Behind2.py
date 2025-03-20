from metasim.cfg.objects import PrimitiveCubeMetaCfg, RigidObjMetaCfg
from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass


@configclass
class OpensdorPosBehindKeyboard0MetaCfg(BaseTaskMetaCfg):
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
            name="apple",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/013_apple_google_16k/013_apple_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c7ec86e7feb746489b30b4a01c2510af/material_2.urdf"
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
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0161b6232216457aa8f4f3393960ec85/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_keyboard_behind_the_apple_on_the_table._/20240824-204303_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindScrewdriver1MetaCfg(BaseTaskMetaCfg):
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
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/043_phillips_screwdriver_google_16k/043_phillips_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_screwdriver_behind_the_bottle_on_the_table._/20240824-172750_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindWatch2MetaCfg(BaseTaskMetaCfg):
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
            name="ladle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ce27e3369587476c85a436905f1e5c00/material_2.urdf"
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
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdb8227a88b2448d8c64fa82ffee3f58/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_watch_behind_the_ladle_on_the_table._/20240824-232020_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindWineglass3MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d72eebbf82be48f0a53e7e8b712e6a66/material_2.urdf"
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
        RigidObjMetaCfg(
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/afca0b1933b84b1dbebd1244f25e72fc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_wineglass_behind_the_remote_control_on_the_table._/20240824-184713_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup4MetaCfg(BaseTaskMetaCfg):
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
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/afca0b1933b84b1dbebd1244f25e72fc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4f24b866dab248b684149ec6bb40101f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/048_hammer_google_16k/048_hammer_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-c_cups_google_16k/065-c_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_wineglass_on_the_table._/20240824-163624_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup5MetaCfg(BaseTaskMetaCfg):
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
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/073-g_lego_duplo_google_16k/073-g_lego_duplo_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-i_cups_google_16k/065-i_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_wineglass_on_the_table._/20240824-211126_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHammer6MetaCfg(BaseTaskMetaCfg):
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b31c69728a414e639eef2fccd1c3dd75/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4f24b866dab248b684149ec6bb40101f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_hammer_behind_the_clipboard_on_the_table._/20240824-214906_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindToy7MetaCfg(BaseTaskMetaCfg):
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
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ae7142127dd84ebbbe7762368ace452c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-a_toy_airplane_google_16k/072-a_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_toy_behind_the_spatula_on_the_table._/20240824-194024_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMouse8MetaCfg(BaseTaskMetaCfg):
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
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5172dbe9281a45f48cee8c15bdfa1831/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mouse_behind_the_microphone_on_the_table._/20240824-214402_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTapeMeasure9MetaCfg(BaseTaskMetaCfg):
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
            name="skillet",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/027_skillet_google_16k/027_skillet_google_16k.urdf",
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/7138f5e13b2e4e17975c23ba5584164b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tape_measure_behind_the_skillet_on_the_table._/20240824-165350_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindUsb10MetaCfg(BaseTaskMetaCfg):
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
            name="credit card",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5de830b2cccf4fe7a2e6b400abf26ca7/material_2.urdf"
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
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b1098389cc3b460bb1f1ce558d4b0764/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_USB_behind_the_credit_card_on_the_table._/20240824-230440_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHighlighter11MetaCfg(BaseTaskMetaCfg):
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
            name="highlighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fd058916fb8843c09b4a2e05e3ee894e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_highlighter_behind_the_mug_on_the_table._/20240824-195305_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindSpoon12MetaCfg(BaseTaskMetaCfg):
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
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbda0b25f41f40958ea984f460e4770b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/031_spoon_google_16k/031_spoon_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_spoon_behind_the_apple_on_the_table._/20240824-231144_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindScissors13MetaCfg(BaseTaskMetaCfg):
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
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b4bb8bd7791648fdb36c458fd9a877bf/material_2.urdf"
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
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2b1120c4b517409184413ed709c57a66/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_scissors_behind_the_cup_on_the_table._/20240824-222333_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMicrophone14MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-j_cups_google_16k/065-j_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5172dbe9281a45f48cee8c15bdfa1831/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_microphone_behind_the_cup_on_the_table._/20240824-195432_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMicrophone15MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-i_cups_google_16k/065-i_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
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
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5172dbe9281a45f48cee8c15bdfa1831/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_microphone_behind_the_cup_on_the_table._/20240824-171947_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMouse16MetaCfg(BaseTaskMetaCfg):
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
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bdd36c94f3f74f22b02b8a069c8d97b7/material_2.urdf"
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
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f496168739384cdb86ef6d65e2068a3f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mouse_behind_the_tape_measure_on_the_table._/20240824-193547_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug17MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/9660e0c0326b4f7386014e27717231ae/material_2.urdf"
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de23895b6e9b4cfd870e30d14c2150dd/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_box_on_the_table._/20240824-203559_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTissueBox18MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/78e016eeb0bf45d5bea47547128383a8/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-j_cups_google_16k/065-j_cups_google_16k.urdf",
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc4c91abf45342b4bb8822f50fa162b2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tissue_box_behind_the_binder_on_the_table._/20240824-172348_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindGlueGun19MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5284b842434413a17133f7bf259669/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_glue_gun_behind_the_toilet_paper_roll_on_the_table._/20240824-214825_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindPlate20MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/e5e87ddbf3f6470384bef58431351e2a/material_2.urdf"
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
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8d50c19e138b403e8b2ede9b47d8be3c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_plate_behind_the_calculator_on_the_table._/20240824-193407_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTissueBox21MetaCfg(BaseTaskMetaCfg):
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
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbda0b25f41f40958ea984f460e4770b/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tissue_box_behind_the_apple_on_the_table._/20240824-191927_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTissueBox22MetaCfg(BaseTaskMetaCfg):
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6e9e9135bb5747f58d388e1e92477f02/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tissue_box_behind_the_mobile_phone_on_the_table._/20240824-221018_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug23MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/025_mug_google_16k/025_mug_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_cup_on_the_table._/20240824-172558_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindToy24MetaCfg(BaseTaskMetaCfg):
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
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6add0a1fa81942acbb24504b130661c1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-a_toy_airplane_google_16k/072-a_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_toy_behind_the_can_on_the_table._/20240824-204811_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup25MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5284b842434413a17133f7bf259669/material_2.urdf"
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-c_cups_google_16k/065-c_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_toilet_paper_roll_on_the_table._/20240824-162009_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindShoe26MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/4f24b866dab248b684149ec6bb40101f/material_2.urdf"
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
            name="pear",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f9ac5185507b4d0dbc744941e9055b96/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_shoe_behind_the_hammer_on_the_table._/20240824-211306_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindShoe27MetaCfg(BaseTaskMetaCfg):
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
            name="mobile phone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/45c813a9fac4458ead1f90280826c0a4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="fork",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/030_fork_google_16k/030_fork_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d5a5f0a954f94bcea3168329d1605fe9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_shoe_behind_the_hammer_on_the_table._/20240824-205430_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBottle28MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/2bd98e8ea09f49bd85453a927011d31d/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_bottle_behind_the_tissue_box_on_the_table._/20240824-170122_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBottle29MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/2bd98e8ea09f49bd85453a927011d31d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/006_mustard_bottle_google_16k/006_mustard_bottle_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_bottle_behind_the_tissue_box_on_the_table._/20240824-205601_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBottle30MetaCfg(BaseTaskMetaCfg):
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
            name="lighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b640aa4990b64db9ab3d868c6f49820e/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_bottle_behind_the_tissue_box_on_the_table._/20240824-160443_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindRemoteControl31MetaCfg(BaseTaskMetaCfg):
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
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-b_toy_airplane_google_16k/072-b_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/003_cracker_box_google_16k/003_cracker_box_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_remote_control_behind_the_bottle_on_the_table._/20240824-214101_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindScissors32MetaCfg(BaseTaskMetaCfg):
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
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/006_mustard_bottle_google_16k/006_mustard_bottle_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_scissors_behind_the_hammer_on_the_table._/20240824-174733_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindPaperweight33MetaCfg(BaseTaskMetaCfg):
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-e_cups_google_16k/065-e_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-i_cups_google_16k/065-i_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="paperweight",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/21c10181c122474a8f72a4ad0331f185/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_paperweight_behind_the_mug_on_the_table._/20240824-161923_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug34MetaCfg(BaseTaskMetaCfg):
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
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de79a920c48745ff95c0df7a7c300091/material_2.urdf"
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/db9345f568e8499a9eac2577302b5f51/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_USB_on_the_table._/20240824-213027_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindGlueGun35MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/b8478cea51454555b90de0fe6ba7ba83/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_glue_gun_behind_the_mug_on_the_table._/20240824-180936_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTissueBox36MetaCfg(BaseTaskMetaCfg):
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
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbda0b25f41f40958ea984f460e4770b/material_2.urdf"
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
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8eda72f64e6e4443af4fdbeed07cad29/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tissue_box_behind_the_clock_on_the_table._/20240824-192421_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup37MetaCfg(BaseTaskMetaCfg):
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/922cd7d18c6748d49fe651ded8a04cf4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-d_cups_google_16k/065-d_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_tissue_box_on_the_table._/20240824-214754_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindKnife38MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/009_gelatin_box_google_16k/009_gelatin_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/048_hammer_google_16k/048_hammer_google_16k.urdf",
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
            name="knife",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/032_knife_google_16k/032_knife_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_knife_behind_the_box_on_the_table._/20240824-203605_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindFork39MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/031_spoon_google_16k/031_spoon_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="fork",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/030_fork_google_16k/030_fork_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_fork_behind_the_spoon_on_the_table._/20240824-193330_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindFork40MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/2613c5f24bb3407da2664c410c34d523/material_2.urdf"
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
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6add0a1fa81942acbb24504b130661c1/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_fork_behind_the_spoon_on_the_table._/20240824-201249_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMicrophone41MetaCfg(BaseTaskMetaCfg):
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
            name="camera",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f6f8675406b7437faaf96a1f82062028/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_microphone_behind_the_camera_on_the_table._/20240824-212353_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMicrophone42MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/e5e87ddbf3f6470384bef58431351e2a/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_microphone_behind_the_binder_on_the_table._/20240824-192237_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHammer43MetaCfg(BaseTaskMetaCfg):
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
            name="hot glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5ceec13e87774982afe825e7e74a0ce1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8ed38a92668a425eb16da938622d9ace/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_hammer_behind_the_hot_glue_gun_on_the_table._/20240824-213528_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindPlate44MetaCfg(BaseTaskMetaCfg):
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
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e1745c4aa7c046a2b5193d2d23be0192/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8d50c19e138b403e8b2ede9b47d8be3c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_plate_behind_the_shoe_on_the_table._/20240824-175155_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBinder45MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/003_cracker_box_google_16k/003_cracker_box_google_16k.urdf",
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
            name="binder",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/78e016eeb0bf45d5bea47547128383a8/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_binder_behind_the_highlighter_on_the_table._/20240824-222525_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMouse46MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/003_cracker_box_google_16k/003_cracker_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/002_master_chef_can_google_16k/002_master_chef_can_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mouse_behind_the_box_on_the_table._/20240824-200957_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindToy47MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e1a1527a0bd49ed8e473079392c31c8/material_2.urdf"
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
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/073-g_lego_duplo_google_16k/073-g_lego_duplo_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_toy_behind_the_box_on_the_table._/20240824-172734_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug48MetaCfg(BaseTaskMetaCfg):
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
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f81ca566b008446eb704cad4844603b6/material_2.urdf"
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
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e5e87ddbf3f6470384bef58431351e2a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_shoe_on_the_table._/20240824-205442_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindApple49MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/e5e87ddbf3f6470384bef58431351e2a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f53d75bd123b40bca14d12d54286f432/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_apple_behind_the_mug_on_the_table._/20240824-212908_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindWatch50MetaCfg(BaseTaskMetaCfg):
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
            name="envelope box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/40b28d1cbfbd4e9f9acf653b748324ee/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_watch_behind_the_envelope_box_on_the_table._/20240824-165409_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindWrench51MetaCfg(BaseTaskMetaCfg):
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
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5bf781c9fd8d4121b735503b13ba2eaf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_wrench_behind_the_mug_on_the_table._/20240824-210237_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindWrench52MetaCfg(BaseTaskMetaCfg):
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
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d9ffbc4bbe1044bb902e1dddac52b0de/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wrench",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/042_adjustable_wrench_google_16k/042_adjustable_wrench_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_wrench_behind_the_mug_on_the_table._/20240824-183457_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTapeMeasure53MetaCfg(BaseTaskMetaCfg):
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
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdb8227a88b2448d8c64fa82ffee3f58/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/1574b13827734d54b6d9d86be8be71d1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tape_measure_behind_the_organizer_on_the_table._/20240824-220050_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindSdCard54MetaCfg(BaseTaskMetaCfg):
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
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d5a5f0a954f94bcea3168329d1605fe9/material_2.urdf"
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
            name="SD card",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/02f7f045679d402da9b9f280030821d4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_SD_card_behind_the_wrench_on_the_table._/20240824-174023_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBox55MetaCfg(BaseTaskMetaCfg):
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
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8d50c19e138b403e8b2ede9b47d8be3c/material_2.urdf"
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
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/009_gelatin_box_google_16k/009_gelatin_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_box_behind_the_orange_on_the_table._/20240824-204501_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindScissors56MetaCfg(BaseTaskMetaCfg):
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
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc707f81a94e48078069c6a463f59fcf/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_scissors_behind_the_pen_on_the_table._/20240824-232309_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBowl57MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-d_cups_google_16k/065-d_cups_google_16k.urdf",
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
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bdd36c94f3f74f22b02b8a069c8d97b7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_bowl_behind_the_cup_on_the_table._/20240824-224617_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug58MetaCfg(BaseTaskMetaCfg):
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
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e51e63e374ee4c25ae3fb4a9c74bd335/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_mug_on_the_table._/20240824-180346_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug59MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/c25119c5ac6e4654be3b75d78e34a912/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6f8040c86eb84e7bba2cd928c0755029/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/1574b13827734d54b6d9d86be8be71d1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/3ea2fd4e065147048064f4c97a89fe6f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_mug_on_the_table._/20240824-201900_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindOrganizer60MetaCfg(BaseTaskMetaCfg):
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
            name="lighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b640aa4990b64db9ab3d868c6f49820e/material_2.urdf"
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
            name="mixer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/990d0cb9499540fda49b1ff36be9ba26/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_organizer_behind_the_lighter_on_the_table._/20240824-163443_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindSdCard61MetaCfg(BaseTaskMetaCfg):
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
            name="skillet",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/027_skillet_google_16k/027_skillet_google_16k.urdf",
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
            name="camera",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6a63fc4af48b453c91ca2b335a4d464d/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_SD_card_behind_the_skillet_on_the_table._/20240824-184555_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMouse62MetaCfg(BaseTaskMetaCfg):
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6f8040c86eb84e7bba2cd928c0755029/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mouse_behind_the_scissors_on_the_table._/20240824-203502_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindClipboard63MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5284b842434413a17133f7bf259669/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_clipboard_behind_the_toilet_paper_roll_on_the_table._/20240824-183304_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindRemoteControl64MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/f017c73a85484b6da3a66ec1cda70c71/material_2.urdf"
            ),
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_remote_control_behind_the_mouse_on_the_table._/20240824-212235_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindClipboard65MetaCfg(BaseTaskMetaCfg):
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a37158f20ccf436483029e8295629738/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/005_tomato_soup_can_google_16k/005_tomato_soup_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b31c69728a414e639eef2fccd1c3dd75/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_clipboard_behind_the_clipboard_on_the_table._/20240824-185159_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCan66MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="lighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d9675ab05c39447baf27e19ea07d484e/material_2.urdf"
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/010_potted_meat_can_google_16k/010_potted_meat_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_can_behind_the_can_on_the_table._/20240824-203150_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindToiletPaperRoll67MetaCfg(BaseTaskMetaCfg):
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
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5284b842434413a17133f7bf259669/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_toilet_paper_roll_behind_the_cup_on_the_table._/20240824-212311_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTissueBox68MetaCfg(BaseTaskMetaCfg):
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-d_cups_google_16k/065-d_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glasses",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e4f348e98ceb45e3abc77da5b738f1b2/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tissue_box_behind_the_knife_on_the_table._/20240824-172926_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBottle69MetaCfg(BaseTaskMetaCfg):
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
            name="wallet",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f47fdcf9615d4e94a71e6731242a4c94/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/021_bleach_cleanser_google_16k/021_bleach_cleanser_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_bottle_behind_the_mug_on_the_table._/20240824-214344_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCreditCard70MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/ccfcc4ae6efa44a2ba34c4c479be7daf/material_2.urdf"
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b31c69728a414e639eef2fccd1c3dd75/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_credit_card_behind_the_wallet_on_the_table._/20240824-224904_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindSpatula71MetaCfg(BaseTaskMetaCfg):
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
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea91786392284f03809c37976da090bf/material_2.urdf"
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
            name="spatula",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/033_spatula_google_16k/033_spatula_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_spatula_behind_the_spoon_on_the_table._/20240824-173152_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindPot72MetaCfg(BaseTaskMetaCfg):
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
            name="flashlight",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/123a79642c2646d8b315576828fea84a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pitcher base",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/019_pitcher_base_google_16k/019_pitcher_base_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pot",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/cba3e4df7c354d22b7913d45a28a8159/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_pot_behind_the_flashlight_on_the_table._/20240824-161318_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMouse73MetaCfg(BaseTaskMetaCfg):
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
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f9d07bb386a04de8b0e1a9a28a936985/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mouse_behind_the_hammer_on_the_table._/20240824-212242_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindScissors74MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/89dcd45ac1f04680b76b709357a3dba3/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_scissors_behind_the_remote_control_on_the_table._/20240824-203721_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBox75MetaCfg(BaseTaskMetaCfg):
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
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5172dbe9281a45f48cee8c15bdfa1831/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_box_behind_the_microphone_on_the_table._/20240824-222253_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCreditCard76MetaCfg(BaseTaskMetaCfg):
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
            name="credit card",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5de830b2cccf4fe7a2e6b400abf26ca7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_credit_card_behind_the_power_drill_on_the_table._/20240824-222016_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindClipboard77MetaCfg(BaseTaskMetaCfg):
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b31c69728a414e639eef2fccd1c3dd75/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_clipboard_behind_the_USB_on_the_table._/20240824-162829_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBox78MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/7bc2b14a48d1413e9375c32a53e3ee6f/material_2.urdf"
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
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/008_pudding_box_google_16k/008_pudding_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_box_behind_the_mug_on_the_table._/20240824-221532_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBox79MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/e5e87ddbf3f6470384bef58431351e2a/material_2.urdf"
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
        RigidObjMetaCfg(
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/003_cracker_box_google_16k/003_cracker_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_box_behind_the_mug_on_the_table._/20240824-213956_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBox80MetaCfg(BaseTaskMetaCfg):
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
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9660e0c0326b4f7386014e27717231ae/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_box_behind_the_mug_on_the_table._/20240824-213614_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindClipboard81MetaCfg(BaseTaskMetaCfg):
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
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea91786392284f03809c37976da090bf/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_clipboard_behind_the_keyboard_on_the_table._/20240824-190644_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindEnvelopeBox82MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/6add0a1fa81942acbb24504b130661c1/material_2.urdf"
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
            name="envelope box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/40b28d1cbfbd4e9f9acf653b748324ee/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_envelope_box_behind_the_bottle_on_the_table._/20240824-165729_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindApple83MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d6951661c1e445d8a1d00b7d38d86030/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc4c91abf45342b4bb8822f50fa162b2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f53d75bd123b40bca14d12d54286f432/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_apple_behind_the_shoe_on_the_table._/20240824-220609_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup84MetaCfg(BaseTaskMetaCfg):
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-f_cups_google_16k/065-f_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_clock_on_the_table._/20240824-200936_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMicrophone85MetaCfg(BaseTaskMetaCfg):
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
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fac08019fef5474189f965bb495771eb/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_microphone_behind_the_mug_on_the_table._/20240824-211848_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMicrophone86MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/e5e87ddbf3f6470384bef58431351e2a/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_microphone_behind_the_mug_on_the_table._/20240824-215946_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindKnife87MetaCfg(BaseTaskMetaCfg):
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
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b1098389cc3b460bb1f1ce558d4b0764/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/032_knife_google_16k/032_knife_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_knife_behind_the_bottle_on_the_table._/20240824-212346_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHammer88MetaCfg(BaseTaskMetaCfg):
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
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbda0b25f41f40958ea984f460e4770b/material_2.urdf"
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
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9bf1b31f641543c9a921042dac3b527f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_hammer_behind_the_book_on_the_table._/20240824-202030_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHotGlueGun89MetaCfg(BaseTaskMetaCfg):
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
            name="hot glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5ceec13e87774982afe825e7e74a0ce1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_hot_glue_gun_behind_the_keyboard_on_the_table._/20240824-170949_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindShoe90MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea0cf48616e34708b73c82eb7c7366ca/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_shoe_behind_the_toilet_paper_roll_on_the_table._/20240824-194856_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindWrench91MetaCfg(BaseTaskMetaCfg):
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
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/19c1913ba85042938f0a87d94397c946/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_wrench_behind_the_binder_on_the_table._/20240824-165829_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCan92MetaCfg(BaseTaskMetaCfg):
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
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2b1120c4b517409184413ed709c57a66/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/005_tomato_soup_can_google_16k/005_tomato_soup_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_can_behind_the_cup_on_the_table._/20240824-172354_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindFork93MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/9660e0c0326b4f7386014e27717231ae/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="fork",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/030_fork_google_16k/030_fork_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_fork_behind_the_box_on_the_table._/20240824-203956_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindWrench94MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/2613c5f24bb3407da2664c410c34d523/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-j_cups_google_16k/065-j_cups_google_16k.urdf",
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
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/19c1913ba85042938f0a87d94397c946/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_wrench_behind_the_spoon_on_the_table._/20240824-211438_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCan95MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/ycb_16k_backup/037_scissors_google_16k/037_scissors_google_16k.urdf"
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6e9e9135bb5747f58d388e1e92477f02/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/005_tomato_soup_can_google_16k/005_tomato_soup_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_can_behind_the_scissors_on_the_table._/20240824-185210_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindShoe96MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/969b0d9d99a8468898753fdcd219f883/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_shoe_behind_the_mouse_on_the_table._/20240824-183420_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBook97MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/ycb_16k_backup/004_sugar_box_google_16k/004_sugar_box_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c7ec86e7feb746489b30b4a01c2510af/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_book_behind_the_box_on_the_table._/20240824-224858_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBox98MetaCfg(BaseTaskMetaCfg):
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
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/aa51af2f1270482193471455b504efc6/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_box_behind_the_tissue_box_on_the_table._/20240824-174641_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHammer99MetaCfg(BaseTaskMetaCfg):
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
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9660e0c0326b4f7386014e27717231ae/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_hammer_behind_the_toy_on_the_table._/20240824-181222_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindPen100MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pen",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbeb7c776372466daffa619106e0b2e0/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_pen_behind_the_can_on_the_table._/20240824-172230_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTissueBox101MetaCfg(BaseTaskMetaCfg):
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
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5284b842434413a17133f7bf259669/material_2.urdf"
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/213d8df9c37a4d8cba794965676f7a75/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tissue_box_behind_the_plate_on_the_table._/20240824-164352_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindShoe102MetaCfg(BaseTaskMetaCfg):
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
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
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ece4453042144b4a82fb86a4eab1ba7f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_shoe_behind_the_wallet_on_the_table._/20240824-193119_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTissueBox103MetaCfg(BaseTaskMetaCfg):
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
            name="apple",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/013_apple_google_16k/013_apple_google_16k.urdf",
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2bd98e8ea09f49bd85453a927011d31d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tissue_box_behind_the_book_on_the_table._/20240824-211529_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindKnife104MetaCfg(BaseTaskMetaCfg):
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a37158f20ccf436483029e8295629738/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0df75457524743ec81468c916fddb930/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_knife_behind_the_clipboard_on_the_table._/20240824-214923_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindKnife105MetaCfg(BaseTaskMetaCfg):
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a37158f20ccf436483029e8295629738/material_2.urdf"
            ),
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
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d9ffbc4bbe1044bb902e1dddac52b0de/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0df75457524743ec81468c916fddb930/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_knife_behind_the_clipboard_on_the_table._/20240824-180858_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBottle106MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/af249e607bea40cfa2f275e5e23b8283/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/1574b13827734d54b6d9d86be8be71d1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/794b730ae452424bb3a9ce3c6caaff7a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_bottle_behind_the_pot_on_the_table._/20240824-175143_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindToy107MetaCfg(BaseTaskMetaCfg):
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
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/073-g_lego_duplo_google_16k/073-g_lego_duplo_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_toy_behind_the_bottle_on_the_table._/20240824-193458_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHammer108MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/f017c73a85484b6da3a66ec1cda70c71/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc4c91abf45342b4bb8822f50fa162b2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/021_bleach_cleanser_google_16k/021_bleach_cleanser_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4f24b866dab248b684149ec6bb40101f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_hammer_behind_the_mouse_on_the_table._/20240824-161830_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindFork109MetaCfg(BaseTaskMetaCfg):
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
            name="glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a1da12b81f034db894496c1ffc4be1f5/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_fork_behind_the_glue_gun_on_the_table._/20240824-201233_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup110MetaCfg(BaseTaskMetaCfg):
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
            name="skillet",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/027_skillet_google_16k/027_skillet_google_16k.urdf",
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-i_cups_google_16k/065-i_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_skillet_on_the_table._/20240824-210539_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindWrench111MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/bf83213efac34b3cb2ad6ac5ddaf05d9/material_2.urdf"
            ),
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
            name="ladle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ce27e3369587476c85a436905f1e5c00/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/19c1913ba85042938f0a87d94397c946/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_wrench_behind_the_bowl_on_the_table._/20240824-174119_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBinder112MetaCfg(BaseTaskMetaCfg):
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/1574b13827734d54b6d9d86be8be71d1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="binder",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/78e016eeb0bf45d5bea47547128383a8/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_binder_behind_the_knife_on_the_table._/20240824-192254_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMixer113MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d72eebbf82be48f0a53e7e8b712e6a66/material_2.urdf"
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
        RigidObjMetaCfg(
            name="mixer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/990d0cb9499540fda49b1ff36be9ba26/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mixer_behind_the_remote_control_on_the_table._/20240824-223328_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTapeMeasure114MetaCfg(BaseTaskMetaCfg):
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
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/19c1913ba85042938f0a87d94397c946/material_2.urdf"
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/7138f5e13b2e4e17975c23ba5584164b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tape_measure_behind_the_cup_on_the_table._/20240824-170132_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindWallet115MetaCfg(BaseTaskMetaCfg):
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
            name="mixer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/990d0cb9499540fda49b1ff36be9ba26/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-h_cups_google_16k/065-h_cups_google_16k.urdf",
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
            name="wallet",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f47fdcf9615d4e94a71e6731242a4c94/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_wallet_behind_the_mixer_on_the_table._/20240824-205516_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindEnvelopeBox116MetaCfg(BaseTaskMetaCfg):
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
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c61227cac7224b86b43c53ac2a2b6ec7/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_envelope_box_behind_the_cup_on_the_table._/20240824-200602_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindRemoteControl117MetaCfg(BaseTaskMetaCfg):
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
            name="clock",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdf932b04e6c4e0fbd6e274563b94536/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d9ffbc4bbe1044bb902e1dddac52b0de/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c7ec86e7feb746489b30b4a01c2510af/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_remote_control_behind_the_wrench_on_the_table._/20240824-210159_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindToiletPaperRoll118MetaCfg(BaseTaskMetaCfg):
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
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5284b842434413a17133f7bf259669/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_toilet_paper_roll_behind_the_calculator_on_the_table._/20240824-180959_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBottle119MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d72eebbf82be48f0a53e7e8b712e6a66/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/7ca7ebcfad964498b49af73be442acf9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/8c0f8088a5d546c886d1b07e3f4eafae/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_bottle_behind_the_remote_control_on_the_table._/20240824-184206_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindShoe120MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/2a371c84c5454f7facba7bb2f5312ad6/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_shoe_behind_the_book_on_the_table._/20240824-211640_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug121MetaCfg(BaseTaskMetaCfg):
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
            name="SD card",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/02f7f045679d402da9b9f280030821d4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/3ea2fd4e065147048064f4c97a89fe6f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_clock_on_the_table._/20240824-170329_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindOrganizer122MetaCfg(BaseTaskMetaCfg):
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
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ae7142127dd84ebbbe7762368ace452c/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_organizer_behind_the_pear_on_the_table._/20240824-211008_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHardDrive123MetaCfg(BaseTaskMetaCfg):
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de23895b6e9b4cfd870e30d14c2150dd/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_hard_drive_behind_the_clock_on_the_table._/20240824-163025_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTissueBox124MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/009_gelatin_box_google_16k/009_gelatin_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/213d8df9c37a4d8cba794965676f7a75/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tissue_box_behind_the_box_on_the_table._/20240824-184449_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTissueBox125MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/ycb_16k_backup/004_sugar_box_google_16k/004_sugar_box_google_16k.urdf"
            ),
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/002_master_chef_can_google_16k/002_master_chef_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8eda72f64e6e4443af4fdbeed07cad29/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tissue_box_behind_the_box_on_the_table._/20240824-205223_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindScissors126MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/9660e0c0326b4f7386014e27717231ae/material_2.urdf"
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
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/ycb_16k_backup/037_scissors_google_16k/037_scissors_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_scissors_behind_the_box_on_the_table._/20240824-171504_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBox127MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/f017c73a85484b6da3a66ec1cda70c71/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hammer",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/048_hammer_google_16k/048_hammer_google_16k.urdf",
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
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e1a1527a0bd49ed8e473079392c31c8/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_box_behind_the_mouse_on_the_table._/20240824-194235_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBox128MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/969b0d9d99a8468898753fdcd219f883/material_2.urdf"
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
            urdf_path=(
                "data_isaaclab/assets/open6dor/ycb_16k_backup/004_sugar_box_google_16k/004_sugar_box_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_box_behind_the_mouse_on_the_table._/20240824-225149_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindSpatula129MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/af249e607bea40cfa2f275e5e23b8283/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/032_knife_google_16k/032_knife_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_spatula_behind_the_pot_on_the_table._/20240824-200736_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindPot130MetaCfg(BaseTaskMetaCfg):
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/005_tomato_soup_can_google_16k/005_tomato_soup_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pot",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/cba3e4df7c354d22b7913d45a28a8159/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_pot_behind_the_toy_on_the_table._/20240824-224226_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug131MetaCfg(BaseTaskMetaCfg):
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b31c69728a414e639eef2fccd1c3dd75/material_2.urdf"
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
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/794b730ae452424bb3a9ce3c6caaff7a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/025_mug_google_16k/025_mug_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_clipboard_on_the_table._/20240824-230605_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHammer132MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/003_cracker_box_google_16k/003_cracker_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/213d8df9c37a4d8cba794965676f7a75/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_hammer_behind_the_box_on_the_table._/20240824-172042_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBottle133MetaCfg(BaseTaskMetaCfg):
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
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0a51815f3c0941ae8312fc6917173ed6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/794b730ae452424bb3a9ce3c6caaff7a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_bottle_behind_the_bowl_on_the_table._/20240824-162633_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindPowerDrill134MetaCfg(BaseTaskMetaCfg):
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
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc707f81a94e48078069c6a463f59fcf/material_2.urdf"
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
            name="power drill",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/035_power_drill_google_16k/035_power_drill_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_power_drill_behind_the_wineglass_on_the_table._/20240824-185936_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMarker135MetaCfg(BaseTaskMetaCfg):
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b31c69728a414e639eef2fccd1c3dd75/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="marker",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/040_large_marker_google_16k/040_large_marker_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_marker_behind_the_clipboard_on_the_table._/20240824-183315_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindPear136MetaCfg(BaseTaskMetaCfg):
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
            name="ladle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ce27e3369587476c85a436905f1e5c00/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_pear_behind_the_ladle_on_the_table._/20240824-200947_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBox137MetaCfg(BaseTaskMetaCfg):
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
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/009_gelatin_box_google_16k/009_gelatin_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_box_behind_the_organizer_on_the_table._/20240824-184550_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup138MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/8c0f8088a5d546c886d1b07e3f4eafae/material_2.urdf"
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/005_tomato_soup_can_google_16k/005_tomato_soup_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-i_cups_google_16k/065-i_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_bottle_on_the_table._/20240824-223454_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup139MetaCfg(BaseTaskMetaCfg):
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
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e1a1527a0bd49ed8e473079392c31c8/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-c_cups_google_16k/065-c_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_bottle_on_the_table._/20240824-180811_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindScissors140MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/044_flat_screwdriver_google_16k/044_flat_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="glasses",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e4f348e98ceb45e3abc77da5b738f1b2/material_2.urdf"
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
            name="scissors",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2b1120c4b517409184413ed709c57a66/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_scissors_behind_the_screwdriver_on_the_table._/20240824-215955_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBowl141MetaCfg(BaseTaskMetaCfg):
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
            name="ladle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ce27e3369587476c85a436905f1e5c00/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/003_cracker_box_google_16k/003_cracker_box_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_bowl_behind_the_ladle_on_the_table._/20240824-163803_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTissueBox142MetaCfg(BaseTaskMetaCfg):
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
            name="spatula",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4b27628be0804c0285d0b13dda025a0d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6e9e9135bb5747f58d388e1e92477f02/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tissue_box_behind_the_USB_on_the_table._/20240824-175704_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCalculator143MetaCfg(BaseTaskMetaCfg):
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
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e32b159011544b8aa7cacd812636353e/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_calculator_behind_the_pot_on_the_table._/20240824-180011_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindWrench144MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/213d8df9c37a4d8cba794965676f7a75/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc4c91abf45342b4bb8822f50fa162b2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wrench",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/042_adjustable_wrench_google_16k/042_adjustable_wrench_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_wrench_behind_the_tissue_box_on_the_table._/20240824-192749_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindKnife145MetaCfg(BaseTaskMetaCfg):
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
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e1745c4aa7c046a2b5193d2d23be0192/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_knife_behind_the_can_on_the_table._/20240824-233542_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup146MetaCfg(BaseTaskMetaCfg):
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
            name="multimeter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/79ac684e66b34554ba869bd2fc3c2653/material_2.urdf"
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_multimeter_on_the_table._/20240824-182704_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug147MetaCfg(BaseTaskMetaCfg):
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
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9adc77036b434348ae049776c50df624/material_2.urdf"
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
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/db9345f568e8499a9eac2577302b5f51/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_toy_on_the_table._/20240824-185930_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug148MetaCfg(BaseTaskMetaCfg):
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
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/008_pudding_box_google_16k/008_pudding_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/025_mug_google_16k/025_mug_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_toy_on_the_table._/20240824-161931_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindEraser149MetaCfg(BaseTaskMetaCfg):
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
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/afca0b1933b84b1dbebd1244f25e72fc/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_eraser_behind_the_wineglass_on_the_table._/20240824-193046_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindApple150MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/008_pudding_box_google_16k/008_pudding_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f53d75bd123b40bca14d12d54286f432/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_apple_behind_the_box_on_the_table._/20240824-233048_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindSpeaker151MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/19c1913ba85042938f0a87d94397c946/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-i_cups_google_16k/065-i_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="speaker",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4445f4442a884999960e7e6660459095/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_speaker_behind_the_wrench_on_the_table._/20240824-180853_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMouse152MetaCfg(BaseTaskMetaCfg):
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
            name="spatula",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/81b129ecf5724f63b5b044702a3140c2/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mouse_behind_the_binder_on_the_table._/20240824-170929_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBottle153MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/044_flat_screwdriver_google_16k/044_flat_screwdriver_google_16k.urdf",
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
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/021_bleach_cleanser_google_16k/021_bleach_cleanser_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_bottle_behind_the_screwdriver_on_the_table._/20240824-204148_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindSkillet154MetaCfg(BaseTaskMetaCfg):
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
            name="skillet",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/027_skillet_google_16k/027_skillet_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_skillet_behind_the_mug_on_the_table._/20240824-200532_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindFork155MetaCfg(BaseTaskMetaCfg):
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-i_cups_google_16k/065-i_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="fork",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/030_fork_google_16k/030_fork_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_fork_behind_the_can_on_the_table._/20240824-233227_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindFork156MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
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
            name="fork",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e98e7fb33743442383812b68608f7006/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_fork_behind_the_can_on_the_table._/20240824-201742_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindShoe157MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/f5080a3df6d847b693c5cca415886c61/material_2.urdf"
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
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bf83213efac34b3cb2ad6ac5ddaf05d9/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_shoe_behind_the_keyboard_on_the_table._/20240824-233248_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCalculator158MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/6add0a1fa81942acbb24504b130661c1/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_calculator_behind_the_bottle_on_the_table._/20240824-165835_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug159MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d72eebbf82be48f0a53e7e8b712e6a66/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/025_mug_google_16k/025_mug_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_remote_control_on_the_table._/20240824-200805_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindOrange160MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d28b249d997b46c1b42771d8ce869902/material_2.urdf"
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
        RigidObjMetaCfg(
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8d50c19e138b403e8b2ede9b47d8be3c/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_orange_behind_the_remote_control_on_the_table._/20240824-194218_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBottle161MetaCfg(BaseTaskMetaCfg):
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
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8c0f8088a5d546c886d1b07e3f4eafae/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_bottle_behind_the_shoe_on_the_table._/20240824-192726_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug162MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5a4e1174dd4f5fa0a9a9076e476b91/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/7bc2b14a48d1413e9375c32a53e3ee6f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_plate_on_the_table._/20240824-200921_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindSpatula163MetaCfg(BaseTaskMetaCfg):
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
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bdd36c94f3f74f22b02b8a069c8d97b7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/033_spatula_google_16k/033_spatula_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_spatula_behind_the_headphone_on_the_table._/20240824-190533_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindToiletPaperRoll164MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea0cf48616e34708b73c82eb7c7366ca/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_toilet_paper_roll_behind_the_bowl_on_the_table._/20240824-192431_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMouse165MetaCfg(BaseTaskMetaCfg):
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
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e51e63e374ee4c25ae3fb4a9c74bd335/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mouse_behind_the_highlighter_on_the_table._/20240824-210408_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindClipboard166MetaCfg(BaseTaskMetaCfg):
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b31c69728a414e639eef2fccd1c3dd75/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_clipboard_behind_the_pot_on_the_table._/20240824-192535_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHighlighter167MetaCfg(BaseTaskMetaCfg):
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c25119c5ac6e4654be3b75d78e34a912/material_2.urdf"
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
            name="highlighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fd058916fb8843c09b4a2e05e3ee894e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_highlighter_behind_the_USB_on_the_table._/20240824-191646_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCan168MetaCfg(BaseTaskMetaCfg):
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
            name="camera",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f6f8675406b7437faaf96a1f82062028/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/002_master_chef_can_google_16k/002_master_chef_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_can_behind_the_camera_on_the_table._/20240824-200629_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindPlate169MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/f496168739384cdb86ef6d65e2068a3f/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_plate_behind_the_mouse_on_the_table._/20240824-173726_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup170MetaCfg(BaseTaskMetaCfg):
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
            name="glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a1da12b81f034db894496c1ffc4be1f5/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-g_cups_google_16k/065-g_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_glue_gun_on_the_table._/20240824-215205_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindUsb171MetaCfg(BaseTaskMetaCfg):
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/002_master_chef_can_google_16k/002_master_chef_can_google_16k.urdf",
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
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/878049e8c3174fa68a56530e5aef7a5a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_USB_behind_the_spatula_on_the_table._/20240824-170201_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMouse172MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/e1745c4aa7c046a2b5193d2d23be0192/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mouse_behind_the_spoon_on_the_table._/20240824-190211_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindPlate173MetaCfg(BaseTaskMetaCfg):
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
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5a4e1174dd4f5fa0a9a9076e476b91/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_plate_behind_the_spatula_on_the_table._/20240824-195803_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindGlueGun174MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/031_spoon_google_16k/031_spoon_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/006_mustard_bottle_google_16k/006_mustard_bottle_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_glue_gun_behind_the_spoon_on_the_table._/20240824-193200_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindSpoon175MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/ece4453042144b4a82fb86a4eab1ba7f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/032_knife_google_16k/032_knife_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/033_spatula_google_16k/033_spatula_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_spoon_behind_the_shoe_on_the_table._/20240824-231515_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindClock176MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/ycb_16k_backup/004_sugar_box_google_16k/004_sugar_box_google_16k.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="power drill",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/035_power_drill_google_16k/035_power_drill_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="clock",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdf932b04e6c4e0fbd6e274563b94536/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_clock_behind_the_box_on_the_table._/20240824-203251_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindToiletPaperRoll177MetaCfg(BaseTaskMetaCfg):
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
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d6e38c73f8f2402aac890e8ebb115302/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_toilet_paper_roll_behind_the_mug_on_the_table._/20240824-205709_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindUsb178MetaCfg(BaseTaskMetaCfg):
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
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9bf1b31f641543c9a921042dac3b527f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b1098389cc3b460bb1f1ce558d4b0764/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_USB_behind_the_bottle_on_the_table._/20240824-194621_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindUsb179MetaCfg(BaseTaskMetaCfg):
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
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea91786392284f03809c37976da090bf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/009_gelatin_box_google_16k/009_gelatin_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0a51815f3c0941ae8312fc6917173ed6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_USB_behind_the_bottle_on_the_table._/20240824-215107_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindTapeMeasure180MetaCfg(BaseTaskMetaCfg):
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/7138f5e13b2e4e17975c23ba5584164b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_tape_measure_behind_the_USB_on_the_table._/20240824-192921_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindToiletPaperRoll181MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/042_adjustable_wrench_google_16k/042_adjustable_wrench_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea0cf48616e34708b73c82eb7c7366ca/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_toilet_paper_roll_behind_the_wrench_on_the_table._/20240824-193810_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindEraser182MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/969b0d9d99a8468898753fdcd219f883/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/005_tomato_soup_can_google_16k/005_tomato_soup_can_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_eraser_behind_the_mouse_on_the_table._/20240824-220632_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindBook183MetaCfg(BaseTaskMetaCfg):
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
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8d50c19e138b403e8b2ede9b47d8be3c/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_book_behind_the_wallet_on_the_table._/20240824-210939_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup184MetaCfg(BaseTaskMetaCfg):
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b31c69728a414e639eef2fccd1c3dd75/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/006_mustard_bottle_google_16k/006_mustard_bottle_google_16k.urdf",
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-i_cups_google_16k/065-i_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_clipboard_on_the_table._/20240824-195642_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCan185MetaCfg(BaseTaskMetaCfg):
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
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/19c1913ba85042938f0a87d94397c946/material_2.urdf"
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_can_behind_the_book_on_the_table._/20240824-162732_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup186MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/4f24b866dab248b684149ec6bb40101f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-d_cups_google_16k/065-d_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_hammer_on_the_table._/20240824-215115_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup187MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d499e1bc8a514e4bb5ca995ea6ba23b6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-a_cups_google_16k/065-a_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_hammer_on_the_table._/20240824-174018_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindPlate188MetaCfg(BaseTaskMetaCfg):
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
            name="envelope box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/40b28d1cbfbd4e9f9acf653b748324ee/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spoon",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/031_spoon_google_16k/031_spoon_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5a4e1174dd4f5fa0a9a9076e476b91/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_plate_behind_the_envelope_box_on_the_table._/20240824-171525_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug189MetaCfg(BaseTaskMetaCfg):
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e5e87ddbf3f6470384bef58431351e2a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_wrench_on_the_table._/20240824-192320_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindMug190MetaCfg(BaseTaskMetaCfg):
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/042_adjustable_wrench_google_16k/042_adjustable_wrench_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ca4f9a92cc2f4ee98fe9332db41bf7f7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_mug_behind_the_wrench_on_the_table._/20240824-161752_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup191MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/e1745c4aa7c046a2b5193d2d23be0192/material_2.urdf"
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-a_cups_google_16k/065-a_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_spoon_on_the_table._/20240824-221353_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindCup192MetaCfg(BaseTaskMetaCfg):
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-c_cups_google_16k/065-c_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_cup_behind_the_spoon_on_the_table._/20240824-193944_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHammer193MetaCfg(BaseTaskMetaCfg):
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
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/89dcd45ac1f04680b76b709357a3dba3/material_2.urdf"
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
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d499e1bc8a514e4bb5ca995ea6ba23b6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_hammer_behind_the_tape_measure_on_the_table._/20240824-224807_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindHammer194MetaCfg(BaseTaskMetaCfg):
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
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d499e1bc8a514e4bb5ca995ea6ba23b6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_hammer_behind_the_hammer_on_the_table._/20240824-221332_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindUsb195MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/c7ec86e7feb746489b30b4a01c2510af/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="marker",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/040_large_marker_google_16k/040_large_marker_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/878049e8c3174fa68a56530e5aef7a5a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_USB_behind_the_remote_control_on_the_table._/20240824-164236_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindShoe196MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e1a1527a0bd49ed8e473079392c31c8/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_shoe_behind_the_box_on_the_table._/20240824-232055_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosBehindApple197MetaCfg(BaseTaskMetaCfg):
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/e1745c4aa7c046a2b5193d2d23be0192/material_2.urdf"
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
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f53d75bd123b40bca14d12d54286f432/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_pos/behind/Place_the_apple_behind_the_spoon_on_the_table._/20240824-194651_no_interaction/trajectory-unified_wo_traj_v2.pkl"
