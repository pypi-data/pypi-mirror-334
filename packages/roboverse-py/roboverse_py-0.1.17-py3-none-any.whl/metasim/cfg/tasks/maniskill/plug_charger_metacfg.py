## TODO:
## 1. The task implementation is not exactly same as the source benchmark
##    In this implementation, the hole on the base is slightly enlarged to reduce the difficulty due to the dynamics gap


from metasim.cfg.checkers.checkers import DetectedChecker
from metasim.cfg.checkers.detectors import RelativeBboxDetector
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .maniskill_task_metacfg import ManiskillTaskMetaCfg


@configclass
class PlugChargerMetaCfg(ManiskillTaskMetaCfg):
    episode_length = 250
    objects = [
        RigidObjMetaCfg(
            name="base",
            usd_path="roboverse_data/assets/maniskill/charger/base/base.usd",
            urdf_path="roboverse_data/assets/maniskill/charger/base.urdf",
            physics=PhysicStateType.GEOM,
            fix_base_link=True,
        ),
        RigidObjMetaCfg(
            name="charger",
            usd_path="roboverse_data/assets/maniskill/charger/charger/charger.usd",
            urdf_path="roboverse_data/assets/maniskill/charger/charger.urdf",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/plug_charger/trajectory-franka_v2.pkl"

    checker = DetectedChecker(
        obj_name="charger",
        detector=RelativeBboxDetector(
            base_obj_name="base",
            relative_quat=[1, 0, 0, 0],
            relative_pos=[0, 0, 0],
            checker_lower=[-0.02, -0.075, -0.075],
            checker_upper=[0.02, 0.075, 0.075],
            # debug_vis=True,
        ),
    )
