from metasim.cfg.objects import PrimitiveCubeMetaCfg, RigidObjMetaCfg
from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.constants import BenchmarkType, PhysicStateType, TaskType
from metasim.utils import configclass


@configclass
class OpensdorTestMetaCfg(BaseTaskMetaCfg):
    source_benchmark = BenchmarkType.OPEN6DOR
    task_type = TaskType.TABLETOP_MANIPULATION
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
            name="tissue box",
            urdf_path=(
                "data_isaaclab/assets/open6dor/objaverse_rescale/dc4c91abf45342b4bb8822f50fa162b2/material_2.urdf"
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
    traj_filepath = "tmp/data_template_v2.pkl"
