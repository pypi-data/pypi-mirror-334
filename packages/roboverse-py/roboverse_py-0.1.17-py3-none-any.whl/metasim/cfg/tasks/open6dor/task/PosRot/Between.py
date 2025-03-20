from metasim.cfg.objects import PrimitiveCubeMetaCfg, RigidObjMetaCfg
from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass


@configclass
class OpensdorPosRotBetweenUprightTissueBox1910MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6e9e9135bb5747f58d388e1e92477f02/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_tissue_box_between_the_keyboard_and_the_tissue_box_on_the_table.__upright/20240824-172651_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysCan1911MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="fork",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e98e7fb33743442383812b68608f7006/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/005_tomato_soup_can_google_16k/005_tomato_soup_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_can_between_the_knife_and_the_fork_on_the_table.__sideways/20240824-233511_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysCan1912MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d1d1c4b27f5c45a29910830e268f7ee2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_can_between_the_mug_and_the_tape_measure_on_the_table.__sideways/20240824-203626_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenScoopRightSpoon1913MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/b2d30398ba3741da9f9aef2319ee2b8b/material_2.urdf"
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
        RigidObjMetaCfg(
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0161b6232216457aa8f4f3393960ec85/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_spoon_between_the_book_and_the_remote_control_on_the_table.__scoop_right/20240824-171548_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownPlate1914MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/002_master_chef_can_google_16k/002_master_chef_can_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_plate_between_the_toilet_paper_roll_and_the_can_on_the_table.__upside_down/20240824-202649_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightLensForthCamera1915MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/8eda72f64e6e4443af4fdbeed07cad29/material_2.urdf"
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
        RigidObjMetaCfg(
            name="camera",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6a63fc4af48b453c91ca2b335a4d464d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_camera_between_the_tissue_box_and_the_hammer_on_the_table.__upright_lens_forth/20240824-170052_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenCapRightMarker1916MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/f53d75bd123b40bca14d12d54286f432/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="fork",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/030_fork_google_16k/030_fork_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="marker",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/040_large_marker_google_16k/040_large_marker_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_marker_between_the_apple_and_the_fork_on_the_table.__cap_right/20240824-175145_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenCapRightMarker1917MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e51e63e374ee4c25ae3fb4a9c74bd335/material_2.urdf"
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
            name="marker",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/040_large_marker_google_16k/040_large_marker_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_marker_between_the_paperweight_and_the_mouse_on_the_table.__cap_right/20240824-223425_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCalculator1918MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/dbb07d13a33546f09ac8ca98b1ddef20/material_2.urdf"
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
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0b1f7c17d70489888f5ae922169c0ce/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_calculator_between_the_wallet_and_the_mug_on_the_table.__upside_down/20240824-211929_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLyingFlatBook1919MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea91786392284f03809c37976da090bf/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_book_between_the_clipboard_and_the_headphone_on_the_table.__lying_flat/20240824-180332_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysBottle1920MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d1d1c4b27f5c45a29910830e268f7ee2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/021_bleach_cleanser_google_16k/021_bleach_cleanser_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_bottle_between_the_keyboard_and_the_tape_measure_on_the_table.__sideways/20240824-174139_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenRemoteControlForthRemoteControl1921MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/4b27628be0804c0285d0b13dda025a0d/material_2.urdf"
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
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea0cf48616e34708b73c82eb7c7366ca/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_remote_control_between_the_spatula_and_the_bottle_on_the_table.__remote_control_forth/20240824-165707_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLeftToy1922MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="knife",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/85db1d392a89459dbde5cdd951c4f6fb/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9adc77036b434348ae049776c50df624/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_toy_between_the_headphone_and_the_knife_on_the_table.__left/20240824-163921_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCalculator1923MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="calipers",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/95c967114b624291bc26bcd705aaa334/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/006_mustard_bottle_google_16k/006_mustard_bottle_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_calculator_between_the_calipers_and_the_bottle_on_the_table.__upside_down/20240824-172939_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownWineglass1924MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8eda72f64e6e4443af4fdbeed07cad29/material_2.urdf"
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
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc707f81a94e48078069c6a463f59fcf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_wineglass_between_the_cup_and_the_tissue_box_on_the_table.__upside_down/20240824-222820_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleLeftMug1925MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
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
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ece4453042144b4a82fb86a4eab1ba7f/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_cup_and_the_hammer_on_the_table.__handle_left/20240824-180007_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightScrewdriver1926MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/002_master_chef_can_google_16k/002_master_chef_can_google_16k.urdf",
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
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/044_flat_screwdriver_google_16k/044_flat_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_screwdriver_between_the_box_and_the_can_on_the_table.__handle_right/20240824-193010_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownWineglass1927MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e98e7fb33743442383812b68608f7006/material_2.urdf"
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
        RigidObjMetaCfg(
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc707f81a94e48078069c6a463f59fcf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_wineglass_between_the_fork_and_the_box_on_the_table.__upside_down/20240824-210019_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenPlugRightUsb1928MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="spatula",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/4b27628be0804c0285d0b13dda025a0d/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_USB_between_the_clipboard_and_the_spatula_on_the_table.__plug_right/20240824-165344_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightHammer1929MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="pot",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/af249e607bea40cfa2f275e5e23b8283/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hammer_between_the_screwdriver_and_the_pot_on_the_table.__handle_right/20240824-220029_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightSpatula1930MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5284b842434413a17133f7bf259669/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_spatula_between_the_box_and_the_toilet_paper_roll_on_the_table.__handle_right/20240824-195322_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightMicrophone1931MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="marker",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/040_large_marker_google_16k/040_large_marker_google_16k.urdf",
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/0a51815f3c0941ae8312fc6917173ed6/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_microphone_between_the_marker_and_the_bowl_on_the_table.__upright/20240824-230421_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenPlugRightUsb1932MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de79a920c48745ff95c0df7a7c300091/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/003_cracker_box_google_16k/003_cracker_box_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_USB_between_the_screwdriver_and_the_book_on_the_table.__plug_right/20240824-173853_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLyingFlatBook1933MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="wrench",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/042_adjustable_wrench_google_16k/042_adjustable_wrench_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_book_between_the_cup_and_the_wrench_on_the_table.__lying_flat/20240824-232159_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenCapRightBottomLeftBottle1934MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/c61227cac7224b86b43c53ac2a2b6ec7/material_2.urdf"
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
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/022_windex_bottle_google_16k/022_windex_bottle_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_bottle_between_the_book_and_the_tissue_box_on_the_table.__cap_right_bottom_left/20240824-184413_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLyingFlatBook1935MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de79a920c48745ff95c0df7a7c300091/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_book_between_the_scissors_and_the_keyboard_on_the_table.__lying_flat/20240824-215723_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownTextualBox1936MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-d_cups_google_16k/065-d_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="hot glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5ceec13e87774982afe825e7e74a0ce1/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_box_between_the_wrench_and_the_cup_on_the_table.__upside_down_textual/20240824-175320_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightHotGlueGun1937MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdb8227a88b2448d8c64fa82ffee3f58/material_2.urdf"
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
            name="hot glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5ceec13e87774982afe825e7e74a0ce1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hot_glue_gun_between_the_watch_and_the_pear_on_the_table.__upright/20240824-200641_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleLeftMug1938MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="binder",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a0026e7d1b244b9a9223daf4223c9372/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_organizer_and_the_binder_on_the_table.__handle_left/20240824-161532_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleLeftMug1939MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="SD card",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/02f7f045679d402da9b9f280030821d4/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_scissors_and_the_SD_card_on_the_table.__handle_left/20240824-191539_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCalculator1940MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/1574b13827734d54b6d9d86be8be71d1/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_calculator_between_the_cup_and_the_tape_measure_on_the_table.__upside_down/20240824-214104_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLeftToy1941MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/ycb_16k_backup/004_sugar_box_google_16k/004_sugar_box_google_16k.urdf"
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
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-b_toy_airplane_google_16k/072-b_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_toy_between_the_mouse_and_the_box_on_the_table.__left/20240824-220536_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightTissueBox1942MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/213d8df9c37a4d8cba794965676f7a75/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_tissue_box_between_the_flashlight_and_the_tissue_box_on_the_table.__upright/20240824-230332_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysTextualBox1943MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="hat",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc02f9c1fd01432fadd6e7d15851dc37/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_box_between_the_cup_and_the_hat_on_the_table.__sideways_textual/20240824-230523_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightWrench1944MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="eraser",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0916a69ba514ecc973b44528b9dcc43/material_2.urdf"
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
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/19c1913ba85042938f0a87d94397c946/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_wrench_between_the_eraser_and_the_shoe_on_the_table.__handle_right/20240824-192325_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenTapeMeasureUprightTapeMeasure1945MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c7ec86e7feb746489b30b4a01c2510af/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_tape_measure_between_the_bowl_and_the_remote_control_on_the_table.__tape_measure_upright/20240824-184258_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenClaspRightWallet1946MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="orange",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a4c9a503f63e440e8d6d924d4e5c36b1/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_wallet_between_the_mug_and_the_orange_on_the_table.__clasp_right/20240824-202822_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownPlate1947MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="apple",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/013_apple_google_16k/013_apple_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_plate_between_the_binder_and_the_apple_on_the_table.__upside_down/20240824-192802_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenTapeMeasureUprightTapeMeasure1948MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-c_cups_google_16k/065-c_cups_google_16k.urdf",
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/1574b13827734d54b6d9d86be8be71d1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_tape_measure_between_the_spoon_and_the_cup_on_the_table.__tape_measure_upright/20240824-175935_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCalculator1949MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ca4f9a92cc2f4ee98fe9332db41bf7f7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-b_toy_airplane_google_16k/072-b_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0b1f7c17d70489888f5ae922169c0ce/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_calculator_between_the_keyboard_and_the_mug_on_the_table.__upside_down/20240824-215838_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightPear1950MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-b_toy_airplane_google_16k/072-b_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pear",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f3dd3064db4f4e8880344425970cecad/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_pear_between_the_keyboard_and_the_toy_on_the_table.__upright/20240824-172951_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLighterForthLighter1951MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/afca0b1933b84b1dbebd1244f25e72fc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pen",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbeb7c776372466daffa619106e0b2e0/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="lighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d9675ab05c39447baf27e19ea07d484e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_lighter_between_the_book_and_the_wineglass_on_the_table.__lighter_forth/20240824-175619_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenBallpointRightPen1952MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea0cf48616e34708b73c82eb7c7366ca/material_2.urdf"
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
            name="pen",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f126e15c0f904fccbd76f9348baea12c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_pen_between_the_cup_and_the_toilet_paper_roll_on_the_table.__ballpoint_right/20240824-172418_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenScoopRightSpoon1953MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_spoon_between_the_mug_and_the_bowl_on_the_table.__scoop_right/20240824-220034_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLyingFlatHardDrive1954MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/002_master_chef_can_google_16k/002_master_chef_can_google_16k.urdf",
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
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8de4975c0f54c1a97203c6a674f6a39/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hard_drive_between_the_wineglass_and_the_can_on_the_table.__lying_flat/20240824-213447_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenTapeMeasureUprightTapeMeasure1955MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="glasses",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e4f348e98ceb45e3abc77da5b738f1b2/material_2.urdf"
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d1d1c4b27f5c45a29910830e268f7ee2/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_tape_measure_between_the_mug_and_the_glasses_on_the_table.__tape_measure_upright/20240824-221936_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightTextualSpeaker1956MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="clock",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdf932b04e6c4e0fbd6e274563b94536/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_speaker_between_the_remote_control_and_the_clock_on_the_table.__upright_textual/20240824-183945_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenRemoteControlForthRemoteControl1957MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/69511a7fad2f42ee8c4b0579bbc8fec6/material_2.urdf"
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
        RigidObjMetaCfg(
            name="spoon",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/031_spoon_google_16k/031_spoon_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_remote_control_between_the_calculator_and_the_envelope_box_on_the_table.__remote_control_forth/20240824-215655_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenCapForthCap1958MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="wallet",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ccfcc4ae6efa44a2ba34c4c479be7daf/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_cap_between_the_bowl_and_the_wallet_on_the_table.__cap_forth/20240824-165111_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightMug1959MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e5e87ddbf3f6470384bef58431351e2a/material_2.urdf"
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/ca4f9a92cc2f4ee98fe9332db41bf7f7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_mug_and_the_mug_on_the_table.__handle_right/20240824-160336_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCup1960MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="calipers",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/95c967114b624291bc26bcd705aaa334/material_2.urdf"
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-f_cups_google_16k/065-f_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_cup_between_the_bottle_and_the_calipers_on_the_table.__upside_down/20240824-193427_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleLeftMug1961MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e1a1527a0bd49ed8e473079392c31c8/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/025_mug_google_16k/025_mug_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_hammer_and_the_box_on_the_table.__handle_left/20240824-182355_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCup1962MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="knife",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/032_knife_google_16k/032_knife_google_16k.urdf",
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-c_cups_google_16k/065-c_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_cup_between_the_mug_and_the_knife_on_the_table.__upside_down/20240824-203949_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenPlugRightUsb1963MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
        RigidObjMetaCfg(
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b1098389cc3b460bb1f1ce558d4b0764/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_USB_between_the_spatula_and_the_tissue_box_on_the_table.__plug_right/20240824-172037_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysCan1964MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="eraser",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0916a69ba514ecc973b44528b9dcc43/material_2.urdf"
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/005_tomato_soup_can_google_16k/005_tomato_soup_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_can_between_the_spatula_and_the_eraser_on_the_table.__sideways/20240824-202019_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenPlugRightUsb1965MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8891134871e48ce8cb5053c4287272b/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_USB_between_the_hammer_and_the_headphone_on_the_table.__plug_right/20240824-223828_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLowerRimGlasses1966MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="binder",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/78e016eeb0bf45d5bea47547128383a8/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_glasses_between_the_mug_and_the_wineglass_on_the_table.__lower_rim/20240824-174818_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightMicrophone1967MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="SD card",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/02f7f045679d402da9b9f280030821d4/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_microphone_between_the_wrench_and_the_SD_card_on_the_table.__upright/20240824-160457_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLyingFlatBook1968MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9660e0c0326b4f7386014e27717231ae/material_2.urdf"
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
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de79a920c48745ff95c0df7a7c300091/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_book_between_the_scissors_and_the_box_on_the_table.__lying_flat/20240824-233557_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightApple1969MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/2bd98e8ea09f49bd85453a927011d31d/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_apple_between_the_mug_and_the_tissue_box_on_the_table.__upright/20240824-162418_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCalculator1970MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9bf1b31f641543c9a921042dac3b527f/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_calculator_between_the_binder_and_the_hammer_on_the_table.__upside_down/20240824-225720_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightTissueBox1971MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e32b159011544b8aa7cacd812636353e/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_tissue_box_between_the_lighter_and_the_hard_drive_on_the_table.__upright/20240824-213956_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightSpatula1972MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/025_mug_google_16k/025_mug_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_spatula_between_the_tissue_box_and_the_mug_on_the_table.__handle_right/20240824-183039_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenRemoteControlForthRemoteControl1973MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="lighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d9675ab05c39447baf27e19ea07d484e/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_remote_control_between_the_multimeter_and_the_lighter_on_the_table.__remote_control_forth/20240824-160349_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenRemoteControlForthRemoteControl1974MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbda0b25f41f40958ea984f460e4770b/material_2.urdf"
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/f1bbc61a42b94ee9a2976ca744f8962e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_remote_control_between_the_screwdriver_and_the_apple_on_the_table.__remote_control_forth/20240824-164522_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenTapeMeasureUprightTapeMeasure1975MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="binder",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a0026e7d1b244b9a9223daf4223c9372/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_tape_measure_between_the_toy_and_the_binder_on_the_table.__tape_measure_upright/20240824-214713_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenBladeRightKnife1976MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e98e7fb33743442383812b68608f7006/material_2.urdf"
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
            name="knife",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/032_knife_google_16k/032_knife_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_knife_between_the_fork_and_the_calipers_on_the_table.__blade_right/20240824-201734_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysTextualBox1977MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b31c69728a414e639eef2fccd1c3dd75/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_box_between_the_cup_and_the_clipboard_on_the_table.__sideways_textual/20240824-190441_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightApple1978MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0b1f7c17d70489888f5ae922169c0ce/material_2.urdf"
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
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbda0b25f41f40958ea984f460e4770b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_apple_between_the_tissue_box_and_the_calculator_on_the_table.__upright/20240824-190339_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightHammer1979MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/19c1913ba85042938f0a87d94397c946/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hammer_between_the_box_and_the_wrench_on_the_table.__handle_right/20240824-182407_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenPlugRightUsb1980MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d9675ab05c39447baf27e19ea07d484e/material_2.urdf"
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d1d1c4b27f5c45a29910830e268f7ee2/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_USB_between_the_lighter_and_the_headphone_on_the_table.__plug_right/20240824-233736_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleLeftMug1981MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8ed38a92668a425eb16da938622d9ace/material_2.urdf"
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/ca4f9a92cc2f4ee98fe9332db41bf7f7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_spatula_and_the_hammer_on_the_table.__handle_left/20240824-214729_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenWatchUprightWatch1982MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/021_bleach_cleanser_google_16k/021_bleach_cleanser_google_16k.urdf",
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
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdb8227a88b2448d8c64fa82ffee3f58/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_watch_between_the_bottle_and_the_plate_on_the_table.__watch_upright/20240824-225905_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenScoopRightSpoon1983MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8a6cb4f7b0004f53830e270dc6e1ff1d/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_spoon_between_the_knife_and_the_wrench_on_the_table.__scoop_right/20240824-204346_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownTextualBox1984MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/fac08019fef5474189f965bb495771eb/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/073-g_lego_duplo_google_16k/073-g_lego_duplo_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_box_between_the_microphone_and_the_toy_on_the_table.__upside_down_textual/20240824-180559_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightWrench1985MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="SD card",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/02f7f045679d402da9b9f280030821d4/material_2.urdf"
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
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5bf781c9fd8d4121b735503b13ba2eaf/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_wrench_between_the_SD_card_and_the_spatula_on_the_table.__handle_right/20240824-195203_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightMug1986MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ae7142127dd84ebbbe7762368ace452c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-j_cups_google_16k/065-j_cups_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_toilet_paper_roll_and_the_shoe_on_the_table.__handle_right/20240824-225752_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightMug1987MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9660e0c0326b4f7386014e27717231ae/material_2.urdf"
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/77d41aba53e4455f9f84fa04b175dff4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_keyboard_and_the_box_on_the_table.__handle_right/20240824-223833_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownTextualBox1988MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d5a5f0a954f94bcea3168329d1605fe9/material_2.urdf"
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
        RigidObjMetaCfg(
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e1a1527a0bd49ed8e473079392c31c8/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_box_between_the_shoe_and_the_binder_on_the_table.__upside_down_textual/20240824-195101_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleLeftMug1989MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/e5e87ddbf3f6470384bef58431351e2a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_hammer_and_the_pot_on_the_table.__handle_left/20240824-175003_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSpoutRightPot1990MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
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
            name="pot",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/cba3e4df7c354d22b7913d45a28a8159/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_pot_between_the_SD_card_and_the_mug_on_the_table.__spout_right/20240824-230439_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenMultimeterForthMultimeter1991MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
        RigidObjMetaCfg(
            name="multimeter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/79ac684e66b34554ba869bd2fc3c2653/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_multimeter_between_the_shoe_and_the_bottle_on_the_table.__multimeter_forth/20240824-174512_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenBladeRightKnife1992MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/f53d75bd123b40bca14d12d54286f432/material_2.urdf"
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
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9bf1b31f641543c9a921042dac3b527f/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_knife_between_the_apple_and_the_credit_card_on_the_table.__blade_right/20240824-190759_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightScrewdriver1993MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-f_cups_google_16k/065-f_cups_google_16k.urdf",
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
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/044_flat_screwdriver_google_16k/044_flat_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_screwdriver_between_the_cup_and_the_cup_on_the_table.__handle_right/20240824-162406_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCup1994MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f5080a3df6d847b693c5cca415886c61/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-f_cups_google_16k/065-f_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_cup_between_the_spatula_and_the_keyboard_on_the_table.__upside_down/20240824-223119_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownClipboard1995MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="calculator",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f0b1f7c17d70489888f5ae922169c0ce/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_clipboard_between_the_hammer_and_the_calculator_on_the_table.__upside_down/20240824-193257_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenClaspRightWallet1996MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="multimeter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/79ac684e66b34554ba869bd2fc3c2653/material_2.urdf"
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
            name="wallet",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f47fdcf9615d4e94a71e6731242a4c94/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_wallet_between_the_cup_and_the_multimeter_on_the_table.__clasp_right/20240824-205612_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCup1997MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="hammer",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/048_hammer_google_16k/048_hammer_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-i_cups_google_16k/065-i_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_cup_between_the_can_and_the_hammer_on_the_table.__upside_down/20240824-182648_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenBladeRightKnife1998MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="wineglass",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/afca0b1933b84b1dbebd1244f25e72fc/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_knife_between_the_spoon_and_the_wineglass_on_the_table.__blade_right/20240824-174903_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownBowl1999MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/4b27628be0804c0285d0b13dda025a0d/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="apple",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/013_apple_google_16k/013_apple_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="bowl",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/024_bowl_google_16k/024_bowl_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_bowl_between_the_spatula_and_the_apple_on_the_table.__upside_down/20240824-170022_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownTextualBox2000MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/77d41aba53e4455f9f84fa04b175dff4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/003_cracker_box_google_16k/003_cracker_box_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_box_between_the_cup_and_the_mug_on_the_table.__upside_down_textual/20240824-190150_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenBladeRightKnife2001MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8ed38a92668a425eb16da938622d9ace/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/032_knife_google_16k/032_knife_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_knife_between_the_bottle_and_the_hammer_on_the_table.__blade_right/20240824-202202_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenWatchUprightWatch2002MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-e_cups_google_16k/065-e_cups_google_16k.urdf",
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
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdb8227a88b2448d8c64fa82ffee3f58/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_watch_between_the_toy_and_the_cup_on_the_table.__watch_upright/20240824-232542_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenProngRightFork2003MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8a6cb4f7b0004f53830e270dc6e1ff1d/material_2.urdf"
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
            name="fork",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e98e7fb33743442383812b68608f7006/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_fork_between_the_cup_and_the_wrench_on_the_table.__prong_right/20240824-174224_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenEarpieceFarHeadphone2004MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="wallet",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ccfcc4ae6efa44a2ba34c4c479be7daf/material_2.urdf"
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
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/efb1727dee214d49b88c58792e4bdffc/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_headphone_between_the_mouse_and_the_wallet_on_the_table.__earpiece_far/20240824-203151_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenPhoneForthMobilePhone2005MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-d_cups_google_16k/065-d_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mobile phone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/45c813a9fac4458ead1f90280826c0a4/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mobile_phone_between_the_watch_and_the_cup_on_the_table.__phone_forth/20240824-165729_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLyingFlatBook2006MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ae7142127dd84ebbbe7762368ace452c/material_2.urdf"
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
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b2d30398ba3741da9f9aef2319ee2b8b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_book_between_the_remote_control_and_the_shoe_on_the_table.__lying_flat/20240824-223928_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysTextualBox2007MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f1bbc61a42b94ee9a2976ca744f8962e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="knife",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/032_knife_google_16k/032_knife_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_box_between_the_shoe_and_the_remote_control_on_the_table.__sideways_textual/20240824-230823_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightKeyboard2008MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d9675ab05c39447baf27e19ea07d484e/material_2.urdf"
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
            name="keyboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/44bb12d306864e2cb4256a61d4168942/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_keyboard_between_the_lighter_and_the_multimeter_on_the_table.__upright/20240824-180444_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenTipRightHighlighter2009MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="glue gun",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a1da12b81f034db894496c1ffc4be1f5/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_highlighter_between_the_mug_and_the_glue_gun_on_the_table.__tip_right/20240824-193329_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSpoutRightPot2010MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-e_cups_google_16k/065-e_cups_google_16k.urdf",
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
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ea91786392284f03809c37976da090bf/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_pot_between_the_cup_and_the_wrench_on_the_table.__spout_right/20240824-205916_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightTissueBox2011MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="binder",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a0026e7d1b244b9a9223daf4223c9372/material_2.urdf"
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6f8040c86eb84e7bba2cd928c0755029/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_tissue_box_between_the_organizer_and_the_binder_on_the_table.__upright/20240824-223706_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleLeftMug2012MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8de4975c0f54c1a97203c6a674f6a39/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_credit_card_and_the_hard_drive_on_the_table.__handle_left/20240824-172601_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightMug2013MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdb8227a88b2448d8c64fa82ffee3f58/material_2.urdf"
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-g_cups_google_16k/065-g_cups_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_watch_and_the_camera_on_the_table.__handle_right/20240824-232324_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCup2014MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/aa51af2f1270482193471455b504efc6/material_2.urdf"
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_cup_between_the_credit_card_and_the_shoe_on_the_table.__upside_down/20240824-202344_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenClaspRightWallet2015MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="pen",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f126e15c0f904fccbd76f9348baea12c/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_wallet_between_the_bottle_and_the_pen_on_the_table.__clasp_right/20240824-224805_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownTextualBox2016MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/efb1727dee214d49b88c58792e4bdffc/material_2.urdf"
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
            name="apple",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/013_apple_google_16k/013_apple_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/009_gelatin_box_google_16k/009_gelatin_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_box_between_the_headphone_and_the_pen_on_the_table.__upside_down_textual/20240824-193741_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenCapForthCap2017MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e51e63e374ee4c25ae3fb4a9c74bd335/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_cap_between_the_camera_and_the_mouse_on_the_table.__cap_forth/20240824-205326_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightScrewdriver2018MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="clipboard",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a37158f20ccf436483029e8295629738/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/043_phillips_screwdriver_google_16k/043_phillips_screwdriver_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_screwdriver_between_the_mug_and_the_clipboard_on_the_table.__handle_right/20240824-180044_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightMug2019MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/89dcd45ac1f04680b76b709357a3dba3/material_2.urdf"
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/3ea2fd4e065147048064f4c97a89fe6f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_lighter_and_the_remote_control_on_the_table.__handle_right/20240824-201112_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownTextualBox2020MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/f53d75bd123b40bca14d12d54286f432/material_2.urdf"
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
            name="box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e1a1527a0bd49ed8e473079392c31c8/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_box_between_the_apple_and_the_credit_card_on_the_table.__upside_down_textual/20240824-201606_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightKeyboard2021MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f53d75bd123b40bca14d12d54286f432/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_keyboard_between_the_cap_and_the_apple_on_the_table.__upright/20240824-220805_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenBladeRightKnife2022MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bdd36c94f3f74f22b02b8a069c8d97b7/material_2.urdf"
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
            name="knife",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0df75457524743ec81468c916fddb930/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_knife_between_the_hammer_and_the_bowl_on_the_table.__blade_right/20240824-215441_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenTipRightHighlighter2023MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/69511a7fad2f42ee8c4b0579bbc8fec6/material_2.urdf"
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
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d17b8f44d1544364b8ad9fe2554ddfdf/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_highlighter_between_the_calculator_and_the_fork_on_the_table.__tip_right/20240824-214702_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLyingFlatHardDrive2024MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="fork",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e98e7fb33743442383812b68608f7006/material_2.urdf"
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
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8de4975c0f54c1a97203c6a674f6a39/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hard_drive_between_the_headphone_and_the_fork_on_the_table.__lying_flat/20240824-214404_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenWatchUprightWatch2025MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5a4e1174dd4f5fa0a9a9076e476b91/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-g_cups_google_16k/065-g_cups_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_watch_between_the_box_and_the_plate_on_the_table.__watch_upright/20240824-205951_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenBulbRightHandleLeftFlashlight2026MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="power drill",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/035_power_drill_google_16k/035_power_drill_google_16k.urdf",
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
            name="flashlight",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/123a79642c2646d8b315576828fea84a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_flashlight_between_the_cup_and_the_power_drill_on_the_table.__bulb_right_handle_left/20240824-212500_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightJawLeftCalipers2027MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-e_cups_google_16k/065-e_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-a_toy_airplane_google_16k/072-a_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="calipers",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/95c967114b624291bc26bcd705aaa334/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_calipers_between_the_bowl_and_the_cup_on_the_table.__handle_right_jaw_left/20240824-162342_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSpoutRightPot2028MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="shoe",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d6951661c1e445d8a1d00b7d38d86030/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/008_pudding_box_google_16k/008_pudding_box_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="pot",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/af249e607bea40cfa2f275e5e23b8283/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_pot_between_the_spoon_and_the_shoe_on_the_table.__spout_right/20240824-161055_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenPlugRightUsb2029MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
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
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b1098389cc3b460bb1f1ce558d4b0764/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_USB_between_the_cup_and_the_bottle_on_the_table.__plug_right/20240824-201719_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownPlate2030MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="book",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/de79a920c48745ff95c0df7a7c300091/material_2.urdf"
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
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8d50c19e138b403e8b2ede9b47d8be3c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_plate_between_the_mug_and_the_book_on_the_table.__upside_down/20240824-202256_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownPlate2031MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="credit card",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5de830b2cccf4fe7a2e6b400abf26ca7/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-j_cups_google_16k/065-j_cups_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_plate_between_the_pear_and_the_credit_card_on_the_table.__upside_down/20240824-165551_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysTextualBox2032MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b8478cea51454555b90de0fe6ba7ba83/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_box_between_the_envelope_box_and_the_mug_on_the_table.__sideways_textual/20240824-175031_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenWatchUprightWatch2033MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="plate",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/029_plate_google_16k/029_plate_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/243b381dcdc34316a7e78a533572d273/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_watch_between_the_binder_and_the_plate_on_the_table.__watch_upright/20240824-190333_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightHammer2034MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d1d1c4b27f5c45a29910830e268f7ee2/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hammer_between_the_bottle_and_the_tape_measure_on_the_table.__handle_right/20240824-223356_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightHammer2035MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-i_cups_google_16k/065-i_cups_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hammer_between_the_spoon_and_the_cup_on_the_table.__handle_right/20240824-183431_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCalculator2036MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/77d41aba53e4455f9f84fa04b175dff4/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_calculator_between_the_bottle_and_the_toy_on_the_table.__upside_down/20240824-191206_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenEarpieceFarHeadphone2037MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/044_flat_screwdriver_google_16k/044_flat_screwdriver_google_16k.urdf",
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
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8891134871e48ce8cb5053c4287272b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_headphone_between_the_remote_control_and_the_screwdriver_on_the_table.__earpiece_far/20240824-220330_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightMug2038MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/77d41aba53e4455f9f84fa04b175dff4/material_2.urdf"
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
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/c25119c5ac6e4654be3b75d78e34a912/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_can_and_the_mug_on_the_table.__handle_right/20240824-163926_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenScoopRightLadle2039MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-c_cups_google_16k/065-c_cups_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_ladle_between_the_USB_and_the_cup_on_the_table.__scoop_right/20240824-162757_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightMouse2040MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0a51815f3c0941ae8312fc6917173ed6/material_2.urdf"
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
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f496168739384cdb86ef6d65e2068a3f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mouse_between_the_tissue_box_and_the_USB_on_the_table.__upright/20240824-191345_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleLeftMug2041MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
        RigidObjMetaCfg(
            name="highlighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/25481a65cad54e2a956394ff2b2765cd/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_glue_gun_and_the_cup_on_the_table.__handle_left/20240824-183958_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenClipSidewaysBinderClips2042MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/c61227cac7224b86b43c53ac2a2b6ec7/material_2.urdf"
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
        RigidObjMetaCfg(
            name="binder clips",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e55c38b24dc4c239448efa1c6b7f49f/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_binder_clips_between_the_book_and_the_scissors_on_the_table.__clip_sideways/20240824-191837_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleLeftMug2043MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="pen",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f126e15c0f904fccbd76f9348baea12c/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_cup_and_the_pen_on_the_table.__handle_left/20240824-230223_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLyingFlatHardDrive2044MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="fork",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/e98e7fb33743442383812b68608f7006/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hard_drive_between_the_mug_and_the_fork_on_the_table.__lying_flat/20240824-172424_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightLensForthCamera2045MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/8c0f8088a5d546c886d1b07e3f4eafae/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_camera_between_the_credit_card_and_the_bottle_on_the_table.__upright_lens_forth/20240824-163846_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenScoopRightSpoon2046MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="apple",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/013_apple_google_16k/013_apple_google_16k.urdf",
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
            name="spoon",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/218768789fdd42bd95eb933046698499/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_spoon_between_the_tissue_box_and_the_apple_on_the_table.__scoop_right/20240824-220844_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightTissueBox2047MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d9675ab05c39447baf27e19ea07d484e/material_2.urdf"
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
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f9d07bb386a04de8b0e1a9a28a936985/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_tissue_box_between_the_lighter_and_the_mouse_on_the_table.__upright/20240824-160125_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightEnvelopeBox2048MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="wallet",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/ccfcc4ae6efa44a2ba34c4c479be7daf/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_envelope_box_between_the_book_and_the_wallet_on_the_table.__upright/20240824-230255_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysBottle2049MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d6e38c73f8f2402aac890e8ebb115302/material_2.urdf"
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
        RigidObjMetaCfg(
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a7785ac7ce7f4ba79df661db33637ba9/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_bottle_between_the_wallet_and_the_watch_on_the_table.__sideways/20240824-161826_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenTipRightHighlighter2050MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="wrench",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/19c1913ba85042938f0a87d94397c946/material_2.urdf"
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
            name="highlighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fd058916fb8843c09b4a2e05e3ee894e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_highlighter_between_the_calculator_and_the_wrench_on_the_table.__tip_right/20240824-170925_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysShoe2051MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d17b8f44d1544364b8ad9fe2554ddfdf/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_shoe_between_the_mug_and_the_bottle_on_the_table.__sideways/20240824-182706_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightApple2052MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-b_cups_google_16k/065-b_cups_google_16k.urdf",
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
            name="apple",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fbda0b25f41f40958ea984f460e4770b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_apple_between_the_cup_and_the_spatula_on_the_table.__upright/20240824-193840_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightMouse2053MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="pen",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f126e15c0f904fccbd76f9348baea12c/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="marker",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/040_large_marker_google_16k/040_large_marker_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mouse_between_the_cup_and_the_pen_on_the_table.__upright/20240824-205503_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCup2054MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="box",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/003_cracker_box_google_16k/003_cracker_box_google_16k.urdf",
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-j_cups_google_16k/065-j_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_cup_between_the_credit_card_and_the_box_on_the_table.__upside_down/20240824-212827_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLighterForthLighter2055MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-a_toy_airplane_google_16k/072-a_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="lighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d9675ab05c39447baf27e19ea07d484e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_lighter_between_the_bottle_and_the_toy_on_the_table.__lighter_forth/20240824-233413_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLyingFlatHardDrive2056MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="spatula",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/033_spatula_google_16k/033_spatula_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hard_drive_between_the_knife_and_the_spatula_on_the_table.__lying_flat/20240824-181741_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleLeftMug2057MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_keyboard_and_the_bottle_on_the_table.__handle_left/20240824-181807_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysBottle2058MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-d_cups_google_16k/065-d_cups_google_16k.urdf",
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
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/794b730ae452424bb3a9ce3c6caaff7a/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_bottle_between_the_paperweight_and_the_cup_on_the_table.__sideways/20240824-193947_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysShoe2059MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="calipers",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/95c967114b624291bc26bcd705aaa334/material_2.urdf"
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
            name="multimeter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/79ac684e66b34554ba869bd2fc3c2653/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_shoe_between_the_calipers_and_the_toilet_paper_roll_on_the_table.__sideways/20240824-193919_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownPlate2060MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="bottle",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/021_bleach_cleanser_google_16k/021_bleach_cleanser_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_plate_between_the_bottle_and_the_bottle_on_the_table.__upside_down/20240824-191301_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightStapler2061MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdb8227a88b2448d8c64fa82ffee3f58/material_2.urdf"
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
            name="knife",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f93d05bc2db144f7a50374794ef5cf8d/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_stapler_between_the_watch_and_the_lighter_on_the_table.__upright/20240824-211730_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightHammer2062MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="highlighter",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/25481a65cad54e2a956394ff2b2765cd/material_2.urdf"
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
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d155e8051294915813e0c156e3cd6de/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hammer_between_the_knife_and_the_highlighter_on_the_table.__handle_right/20240824-192658_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightHammer2063MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="binder clips",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5e55c38b24dc4c239448efa1c6b7f49f/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hammer_between_the_mobile_phone_and_the_binder_clips_on_the_table.__handle_right/20240824-180946_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenHandleRightMug2064MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="apple",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/013_apple_google_16k/013_apple_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="mug",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/9321c45cb9cf459f9f803507d3a11fb3/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mug_between_the_wallet_and_the_apple_on_the_table.__handle_right/20240824-220336_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenSidewaysCan2065MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-b_toy_airplane_google_16k/072-b_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_can_between_the_can_and_the_toy_on_the_table.__sideways/20240824-202035_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightPear2066MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/dbb07d13a33546f09ac8ca98b1ddef20/material_2.urdf"
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
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/b1098389cc3b460bb1f1ce558d4b0764/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_pear_between_the_wallet_and_the_mug_on_the_table.__upright/20240824-182049_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownTextualBox2067MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/aa51af2f1270482193471455b504efc6/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_box_between_the_wrench_and_the_shoe_on_the_table.__upside_down_textual/20240824-185945_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightMouse2068MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="USB",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/0a51815f3c0941ae8312fc6917173ed6/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mouse_between_the_binder_and_the_mug_on_the_table.__upright/20240824-202350_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenScoopRightSpoon2069MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/6f8040c86eb84e7bba2cd928c0755029/material_2.urdf"
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
            name="toilet paper roll",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5284b842434413a17133f7bf259669/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_spoon_between_the_tissue_box_and_the_wrench_on_the_table.__scoop_right/20240824-161929_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenEarpieceFarHeadphone2070MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="headphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8891134871e48ce8cb5053c4287272b/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_headphone_between_the_cup_and_the_headphone_on_the_table.__earpiece_far/20240824-160539_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightApple2071MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="bowl",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/bf83213efac34b3cb2ad6ac5ddaf05d9/material_2.urdf"
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
            name="apple",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/013_apple_google_16k/013_apple_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_apple_between_the_mug_and_the_bowl_on_the_table.__upright/20240824-232457_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCalculator2072MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-g_cups_google_16k/065-g_cups_google_16k.urdf",
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/054be0c3f09143f38c4d8038eb2588c6/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_calculator_between_the_can_and_the_cup_on_the_table.__upside_down/20240824-195457_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLyingFlatHardDrive2073MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="orange",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/a4c9a503f63e440e8d6d924d4e5c36b1/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-h_cups_google_16k/065-h_cups_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hard_drive_between_the_wrench_and_the_orange_on_the_table.__lying_flat/20240824-184405_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCup2074MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/007_tuna_fish_can_google_16k/007_tuna_fish_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="can",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/005_tomato_soup_can_google_16k/005_tomato_soup_can_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-f_cups_google_16k/065-f_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_cup_between_the_tissue_box_and_the_can_on_the_table.__upside_down/20240824-165142_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightTissueBox2075MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="screwdriver",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/043_phillips_screwdriver_google_16k/043_phillips_screwdriver_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_tissue_box_between_the_mug_and_the_screwdriver_on_the_table.__upright/20240824-211844_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownCup2076MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/b1098389cc3b460bb1f1ce558d4b0764/material_2.urdf"
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
            name="microphone",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/5172dbe9281a45f48cee8c15bdfa1831/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="cup",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/065-j_cups_google_16k/065-j_cups_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_cup_between_the_USB_and_the_calculator_on_the_table.__upside_down/20240824-221614_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenRemoteControlForthRemoteControl2077MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="paperweight",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/21c10181c122474a8f72a4ad0331f185/material_2.urdf"
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
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f1bbc61a42b94ee9a2976ca744f8962e/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_remote_control_between_the_binder_and_the_paperweight_on_the_table.__remote_control_forth/20240824-223038_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownPlate2078MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="mouse",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f496168739384cdb86ef6d65e2068a3f/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_plate_between_the_cup_and_the_mouse_on_the_table.__upside_down/20240824-182832_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenCardForthTextualSdCard2079MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="wallet",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dbb07d13a33546f09ac8ca98b1ddef20/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="spatula",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/033_spatula_google_16k/033_spatula_google_16k.urdf",
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_SD_card_between_the_hammer_and_the_wallet_on_the_table.__card_forth_textual/20240824-171733_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenRightToy2080MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="knife",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/85db1d392a89459dbde5cdd951c4f6fb/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="toy",
            urdf_path="data_isaaclab/assets/open6dor/ycb_16k_backup/072-a_toy_airplane_google_16k/072-a_toy_airplane_google_16k.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_toy_between_the_binder_and_the_knife_on_the_table.__right/20240824-212817_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightHotGlueGun2081MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
    episode_length = 600
    objects = [
        PrimitiveCubeMetaCfg(
            name="table",
            mass=1,
            color=[255, 255, 255],
            size=[0.6, 0.8, 0.3],
        ),
        RigidObjMetaCfg(
            name="calipers",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/95c967114b624291bc26bcd705aaa334/material_2.urdf"
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
            name="hammer",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d155e8051294915813e0c156e3cd6de/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hot_glue_gun_between_the_calipers_and_the_mug_on_the_table.__upright/20240824-232737_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightStapler2082MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/d5a5f0a954f94bcea3168329d1605fe9/material_2.urdf"
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
            name="stapler",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d2c345be5c084b4e8c92b48f7be69315/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_stapler_between_the_shoe_and_the_spoon_on_the_table.__upright/20240824-215634_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenTapeMeasureUprightTapeMeasure2083MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f1bbc61a42b94ee9a2976ca744f8962e/material_2.urdf"
            ),
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
            name="tape measure",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/7138f5e13b2e4e17975c23ba5584164b/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_tape_measure_between_the_bottle_and_the_remote_control_on_the_table.__tape_measure_upright/20240824-222814_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenPlugRightUsb2084MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="remote control",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d72eebbf82be48f0a53e7e8b712e6a66/material_2.urdf"
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_USB_between_the_can_and_the_remote_control_on_the_table.__plug_right/20240824-201859_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUpsideDownPlate2085MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="bottle",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/d17b8f44d1544364b8ad9fe2554ddfdf/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_plate_between_the_mouse_and_the_bottle_on_the_table.__upside_down/20240824-201954_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenWatchUprightWatch2086MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
                "data_isaaclab/assets/open6dor/objaverse_rescale/bf83213efac34b3cb2ad6ac5ddaf05d9/material_2.urdf"
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
            name="watch",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/fdb8227a88b2448d8c64fa82ffee3f58/material_2.urdf"
            ),
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_watch_between_the_headphone_and_the_bowl_on_the_table.__watch_upright/20240824-202453_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenUprightMouse2087MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="hard drive",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/f8de4975c0f54c1a97203c6a674f6a39/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_mouse_between_the_shoe_and_the_hard_drive_on_the_table.__upright/20240824-190636_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorPosRotBetweenLyingFlatHardDrive2088MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="plate",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/6d5a4e1174dd4f5fa0a9a9076e476b91/material_2.urdf"
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
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_6dof/between/Place_the_hard_drive_between_the_clock_and_the_plate_on_the_table.__lying_flat/20240824-182619_no_interaction/trajectory-unified_wo_traj_v2.pkl"
