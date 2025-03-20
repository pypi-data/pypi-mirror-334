from metasim.cfg.objects import ArticulationObjMetaCfg, PrimitiveCubeMetaCfg
from metasim.cfg.tasks.base_task_metacfg import BaseTaskMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass


@configclass
class SceneA(BaseTaskMetaCfg):
    objects = [
        ArticulationObjMetaCfg(
            name="table",
            filepath="roboverse_data/assets/calvin/COMMON/table_a/usd/table.usd",
            urdf_path="roboverse_data/assets/calvin/COMMON/table_a/urdf/calvin_table_A.urdf",
            fix_base_link=True,
            scale=0.8,
        ),
        PrimitiveCubeMetaCfg(
            name="block_red",
            mass=0.1,  # origin is 1, smaller mass is easier to grasp
            size=(0.07, 0.05, 0.05),
            color=(1.0, 0.0, 0.0),
            physics=PhysicStateType.RIGIDBODY,
            scale=0.8,
        ),
        PrimitiveCubeMetaCfg(
            name="block_blue",
            mass=0.1,  # origin is 1, smaller mass is easier to grasp
            size=(0.1, 0.05, 0.05),
            color=(0.0, 0.0, 1.0),
            physics=PhysicStateType.RIGIDBODY,
            scale=0.8,
        ),
        PrimitiveCubeMetaCfg(
            name="block_pink",
            mass=0.1,  # origin is 1, smaller mass is easier to grasp
            size=(0.05, 0.05, 0.05),
            color=(1.0, 0.0, 1.0),
            physics=PhysicStateType.RIGIDBODY,
            scale=0.8,
        ),
    ]


SCENE_A = SceneA()
