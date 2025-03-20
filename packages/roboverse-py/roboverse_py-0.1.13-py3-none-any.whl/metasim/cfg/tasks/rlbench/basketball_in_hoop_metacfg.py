from metasim.cfg.checkers import DetectedChecker, RelativeBboxDetector
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class BasketballInHoopMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/basketball_in_hoop/v2"
    objects = [
        RigidObjMetaCfg(
            name="basket_ball_hoop_visual",
            filepath="roboverse_data/assets/rlbench/basketball_in_hoop/basket_ball_hoop_visual/usd/basket_ball_hoop_visual_colored.usd",
            mesh_path="roboverse_data/assets/rlbench/basketball_in_hoop/basket_ball_hoop_visual/mesh/basket_ball_hoop_visual_colored.obj",
            physics=PhysicStateType.XFORM,
        ),
        RigidObjMetaCfg(
            name="ball",
            filepath="roboverse_data/assets/rlbench/basketball_in_hoop/ball/usd/ball_textured.usd",
            mesh_path="roboverse_data/assets/rlbench/basketball_in_hoop/ball/mesh/ball_textured.obj",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    checker = DetectedChecker(
        obj_name="ball",
        detector=RelativeBboxDetector(
            base_obj_name="basket_ball_hoop_visual",
            relative_quat=[-0.52125348147482, 0.66573167191783, 0.4157939106384, 0.33497995900038],
            relative_pos=[-0.060456029040702, -0.27864555866622, -0.17772846479924],
            checker_lower=[-0.025, -0.025, -0.05],
            checker_upper=[0.025, 0.025, 0.1],
            # debug_vis=True,
        ),
    )
