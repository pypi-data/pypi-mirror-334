from metasim.cfg.objects import PrimitiveCubeMetaCfg, RigidObjMetaCfg
from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass


@configclass
class OpensdorRotTipRightHighlighter259MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/fd058916fb8843c09b4a2e05e3ee894e_tip_right/20240826-213625_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorRotTipRightHighlighter260MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/fd058916fb8843c09b4a2e05e3ee894e_tip_right/20240826-213156_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorRotTipRightHighlighter261MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/fd058916fb8843c09b4a2e05e3ee894e_tip_right/20240826-213247_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorRotTipRightHighlighter262MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/fd058916fb8843c09b4a2e05e3ee894e_tip_right/20240826-211702_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorRotTipRightHighlighter263MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/fd058916fb8843c09b4a2e05e3ee894e_tip_right/20240826-213535_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorRotTipRightHighlighter264MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/fd058916fb8843c09b4a2e05e3ee894e_tip_right/20240826-213114_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorRotTipRightHighlighter1092MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/25481a65cad54e2a956394ff2b2765cd_tip_right/20240826-223730_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorRotTipRightHighlighter1093MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/25481a65cad54e2a956394ff2b2765cd_tip_right/20240826-220758_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorRotTipRightHighlighter1094MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/25481a65cad54e2a956394ff2b2765cd_tip_right/20240826-222201_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorRotTipRightHighlighter1095MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/25481a65cad54e2a956394ff2b2765cd_tip_right/20240826-223258_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorRotTipRightHighlighter1096MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/25481a65cad54e2a956394ff2b2765cd_tip_right/20240826-215100_no_interaction/trajectory-unified_wo_traj_v2.pkl"


@configclass
class OpensdorRotTipRightHighlighter1097MetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
    ]
    traj_filepath = "data_isaaclab/source_data/open6dor/task_refine_rot_only/rot_ins/25481a65cad54e2a956394ff2b2765cd_tip_right/20240826-223903_no_interaction/trajectory-unified_wo_traj_v2.pkl"
