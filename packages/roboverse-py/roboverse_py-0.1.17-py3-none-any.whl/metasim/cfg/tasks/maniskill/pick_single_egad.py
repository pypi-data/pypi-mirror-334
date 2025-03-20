from metasim.cfg.checkers import PositionShiftChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .maniskill_task_metacfg import ManiskillTaskMetaCfg


@configclass
class _PickSingleEgadBaseMetaCfg(ManiskillTaskMetaCfg):
    episode_length = 250
    checker = PositionShiftChecker(
        obj_name="obj",
        distance=0.075,
        axis="z",
    )


@configclass
class PickSingleEgadA100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A10_0_v2.pkl"


@configclass
class PickSingleEgadA110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A11_0_v2.pkl"


@configclass
class PickSingleEgadA130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A13_0_v2.pkl"


@configclass
class PickSingleEgadA140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A14_0_v2.pkl"


@configclass
class PickSingleEgadA160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A16_0_v2.pkl"


@configclass
class PickSingleEgadA161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A16_1_v2.pkl"


@configclass
class PickSingleEgadA180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A18_0_v2.pkl"


@configclass
class PickSingleEgadA190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A19_0_v2.pkl"


@configclass
class PickSingleEgadA200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A20_0_v2.pkl"


@configclass
class PickSingleEgadA210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A21_0_v2.pkl"


@configclass
class PickSingleEgadA220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A22_0_v2.pkl"


@configclass
class PickSingleEgadA240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/A24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/A24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-A24_0_v2.pkl"


@configclass
class PickSingleEgadB100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B10_0_v2.pkl"


@configclass
class PickSingleEgadB101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B10_1_v2.pkl"


@configclass
class PickSingleEgadB102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B10_2_v2.pkl"


@configclass
class PickSingleEgadB103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B10_3_v2.pkl"


@configclass
class PickSingleEgadB111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B11_1_v2.pkl"


@configclass
class PickSingleEgadB112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B11_2_v2.pkl"


@configclass
class PickSingleEgadB113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B11_3_v2.pkl"


@configclass
class PickSingleEgadB121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B12_1_v2.pkl"


@configclass
class PickSingleEgadB130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B13_0_v2.pkl"


@configclass
class PickSingleEgadB131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B13_1_v2.pkl"


@configclass
class PickSingleEgadB132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B13_2_v2.pkl"


@configclass
class PickSingleEgadB133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B13_3_v2.pkl"


@configclass
class PickSingleEgadB140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B14_0_v2.pkl"


@configclass
class PickSingleEgadB141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B14_1_v2.pkl"


@configclass
class PickSingleEgadB142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B14_2_v2.pkl"


@configclass
class PickSingleEgadB143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B14_3_v2.pkl"


@configclass
class PickSingleEgadB150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B15_0_v2.pkl"


@configclass
class PickSingleEgadB151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B15_1_v2.pkl"


@configclass
class PickSingleEgadB152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B15_2_v2.pkl"


@configclass
class PickSingleEgadB153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B15_3_v2.pkl"


@configclass
class PickSingleEgadB161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B16_1_v2.pkl"


@configclass
class PickSingleEgadB162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B16_2_v2.pkl"


@configclass
class PickSingleEgadB163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B16_3_v2.pkl"


@configclass
class PickSingleEgadB170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B17_0_v2.pkl"


@configclass
class PickSingleEgadB171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B17_1_v2.pkl"


@configclass
class PickSingleEgadB172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B17_2_v2.pkl"


@configclass
class PickSingleEgadB173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B17_3_v2.pkl"


@configclass
class PickSingleEgadB180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B18_0_v2.pkl"


@configclass
class PickSingleEgadB190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B19_0_v2.pkl"


@configclass
class PickSingleEgadB192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B19_2_v2.pkl"


@configclass
class PickSingleEgadB193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B19_3_v2.pkl"


@configclass
class PickSingleEgadB200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B20_0_v2.pkl"


@configclass
class PickSingleEgadB201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B20_1_v2.pkl"


@configclass
class PickSingleEgadB202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B20_2_v2.pkl"


@configclass
class PickSingleEgadB210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B21_0_v2.pkl"


@configclass
class PickSingleEgadB211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B21_1_v2.pkl"


@configclass
class PickSingleEgadB212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B21_2_v2.pkl"


@configclass
class PickSingleEgadB213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B21_3_v2.pkl"


@configclass
class PickSingleEgadB220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B22_0_v2.pkl"


@configclass
class PickSingleEgadB221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B22_1_v2.pkl"


@configclass
class PickSingleEgadB222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B22_2_v2.pkl"


@configclass
class PickSingleEgadB223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B22_3_v2.pkl"


@configclass
class PickSingleEgadB231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B23_1_v2.pkl"


@configclass
class PickSingleEgadB232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B23_2_v2.pkl"


@configclass
class PickSingleEgadB233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B23_3_v2.pkl"


@configclass
class PickSingleEgadB240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B24_0_v2.pkl"


@configclass
class PickSingleEgadB241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B24_1_v2.pkl"


@configclass
class PickSingleEgadB242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B24_2_v2.pkl"


@configclass
class PickSingleEgadB243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B24_3_v2.pkl"


@configclass
class PickSingleEgadB250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B25_0_v2.pkl"


@configclass
class PickSingleEgadB251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B25_1_v2.pkl"


@configclass
class PickSingleEgadB252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B25_2_v2.pkl"


@configclass
class PickSingleEgadB253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/B25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/B25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-B25_3_v2.pkl"


@configclass
class PickSingleEgadC100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C10_0_v2.pkl"


@configclass
class PickSingleEgadC101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C10_1_v2.pkl"


@configclass
class PickSingleEgadC102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C10_2_v2.pkl"


@configclass
class PickSingleEgadC103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C10_3_v2.pkl"


@configclass
class PickSingleEgadC110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C11_0_v2.pkl"


@configclass
class PickSingleEgadC111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C11_1_v2.pkl"


@configclass
class PickSingleEgadC113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C11_3_v2.pkl"


@configclass
class PickSingleEgadC120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C12_0_v2.pkl"


@configclass
class PickSingleEgadC121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C12_1_v2.pkl"


@configclass
class PickSingleEgadC122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C12_2_v2.pkl"


@configclass
class PickSingleEgadC123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C12_3_v2.pkl"


@configclass
class PickSingleEgadC130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C13_0_v2.pkl"


@configclass
class PickSingleEgadC131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C13_1_v2.pkl"


@configclass
class PickSingleEgadC132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C13_2_v2.pkl"


@configclass
class PickSingleEgadC133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C13_3_v2.pkl"


@configclass
class PickSingleEgadC140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C14_0_v2.pkl"


@configclass
class PickSingleEgadC142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C14_2_v2.pkl"


@configclass
class PickSingleEgadC143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C14_3_v2.pkl"


@configclass
class PickSingleEgadC150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C15_0_v2.pkl"


@configclass
class PickSingleEgadC151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C15_1_v2.pkl"


@configclass
class PickSingleEgadC152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C15_2_v2.pkl"


@configclass
class PickSingleEgadC153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C15_3_v2.pkl"


@configclass
class PickSingleEgadC161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C16_1_v2.pkl"


@configclass
class PickSingleEgadC162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C16_2_v2.pkl"


@configclass
class PickSingleEgadC163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C16_3_v2.pkl"


@configclass
class PickSingleEgadC170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C17_0_v2.pkl"


@configclass
class PickSingleEgadC171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C17_1_v2.pkl"


@configclass
class PickSingleEgadC172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C17_2_v2.pkl"


@configclass
class PickSingleEgadC173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C17_3_v2.pkl"


@configclass
class PickSingleEgadC180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C18_0_v2.pkl"


@configclass
class PickSingleEgadC181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C18_1_v2.pkl"


@configclass
class PickSingleEgadC182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C18_2_v2.pkl"


@configclass
class PickSingleEgadC183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C18_3_v2.pkl"


@configclass
class PickSingleEgadC190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C19_0_v2.pkl"


@configclass
class PickSingleEgadC191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C19_1_v2.pkl"


@configclass
class PickSingleEgadC192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C19_2_v2.pkl"


@configclass
class PickSingleEgadC193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C19_3_v2.pkl"


@configclass
class PickSingleEgadC200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C20_0_v2.pkl"


@configclass
class PickSingleEgadC201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C20_1_v2.pkl"


@configclass
class PickSingleEgadC202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C20_2_v2.pkl"


@configclass
class PickSingleEgadC203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C20_3_v2.pkl"


@configclass
class PickSingleEgadC210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C21_0_v2.pkl"


@configclass
class PickSingleEgadC211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C21_1_v2.pkl"


@configclass
class PickSingleEgadC212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C21_2_v2.pkl"


@configclass
class PickSingleEgadC213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C21_3_v2.pkl"


@configclass
class PickSingleEgadC220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C22_0_v2.pkl"


@configclass
class PickSingleEgadC221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C22_1_v2.pkl"


@configclass
class PickSingleEgadC223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C22_3_v2.pkl"


@configclass
class PickSingleEgadC230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C23_0_v2.pkl"


@configclass
class PickSingleEgadC231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C23_1_v2.pkl"


@configclass
class PickSingleEgadC232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C23_2_v2.pkl"


@configclass
class PickSingleEgadC233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C23_3_v2.pkl"


@configclass
class PickSingleEgadC240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C24_0_v2.pkl"


@configclass
class PickSingleEgadC241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C24_1_v2.pkl"


@configclass
class PickSingleEgadC242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C24_2_v2.pkl"


@configclass
class PickSingleEgadC243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C24_3_v2.pkl"


@configclass
class PickSingleEgadC250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C25_0_v2.pkl"


@configclass
class PickSingleEgadC251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C25_1_v2.pkl"


@configclass
class PickSingleEgadC252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C25_2_v2.pkl"


@configclass
class PickSingleEgadC253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/C25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/C25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-C25_3_v2.pkl"


@configclass
class PickSingleEgadD100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D10_0_v2.pkl"


@configclass
class PickSingleEgadD101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D10_1_v2.pkl"


@configclass
class PickSingleEgadD102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D10_2_v2.pkl"


@configclass
class PickSingleEgadD103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D10_3_v2.pkl"


@configclass
class PickSingleEgadD110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D11_0_v2.pkl"


@configclass
class PickSingleEgadD111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D11_1_v2.pkl"


@configclass
class PickSingleEgadD112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D11_2_v2.pkl"


@configclass
class PickSingleEgadD113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D11_3_v2.pkl"


@configclass
class PickSingleEgadD121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D12_1_v2.pkl"


@configclass
class PickSingleEgadD122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D12_2_v2.pkl"


@configclass
class PickSingleEgadD130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D13_0_v2.pkl"


@configclass
class PickSingleEgadD131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D13_1_v2.pkl"


@configclass
class PickSingleEgadD132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D13_2_v2.pkl"


@configclass
class PickSingleEgadD133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D13_3_v2.pkl"


@configclass
class PickSingleEgadD141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D14_1_v2.pkl"


@configclass
class PickSingleEgadD142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D14_2_v2.pkl"


@configclass
class PickSingleEgadD150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D15_0_v2.pkl"


@configclass
class PickSingleEgadD151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D15_1_v2.pkl"


@configclass
class PickSingleEgadD152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D15_2_v2.pkl"


@configclass
class PickSingleEgadD153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D15_3_v2.pkl"


@configclass
class PickSingleEgadD160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D16_0_v2.pkl"


@configclass
class PickSingleEgadD161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D16_1_v2.pkl"


@configclass
class PickSingleEgadD162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D16_2_v2.pkl"


@configclass
class PickSingleEgadD163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D16_3_v2.pkl"


@configclass
class PickSingleEgadD170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D17_0_v2.pkl"


@configclass
class PickSingleEgadD171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D17_1_v2.pkl"


@configclass
class PickSingleEgadD172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D17_2_v2.pkl"


@configclass
class PickSingleEgadD180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D18_0_v2.pkl"


@configclass
class PickSingleEgadD181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D18_1_v2.pkl"


@configclass
class PickSingleEgadD182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D18_2_v2.pkl"


@configclass
class PickSingleEgadD183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D18_3_v2.pkl"


@configclass
class PickSingleEgadD190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D19_0_v2.pkl"


@configclass
class PickSingleEgadD191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D19_1_v2.pkl"


@configclass
class PickSingleEgadD193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D19_3_v2.pkl"


@configclass
class PickSingleEgadD200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D20_0_v2.pkl"


@configclass
class PickSingleEgadD201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D20_1_v2.pkl"


@configclass
class PickSingleEgadD202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D20_2_v2.pkl"


@configclass
class PickSingleEgadD203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D20_3_v2.pkl"


@configclass
class PickSingleEgadD210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D21_0_v2.pkl"


@configclass
class PickSingleEgadD211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D21_1_v2.pkl"


@configclass
class PickSingleEgadD212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D21_2_v2.pkl"


@configclass
class PickSingleEgadD213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D21_3_v2.pkl"


@configclass
class PickSingleEgadD220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D22_0_v2.pkl"


@configclass
class PickSingleEgadD221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D22_1_v2.pkl"


@configclass
class PickSingleEgadD222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D22_2_v2.pkl"


@configclass
class PickSingleEgadD223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D22_3_v2.pkl"


@configclass
class PickSingleEgadD230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D23_0_v2.pkl"


@configclass
class PickSingleEgadD231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D23_1_v2.pkl"


@configclass
class PickSingleEgadD232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D23_2_v2.pkl"


@configclass
class PickSingleEgadD233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D23_3_v2.pkl"


@configclass
class PickSingleEgadD240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D24_0_v2.pkl"


@configclass
class PickSingleEgadD241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D24_1_v2.pkl"


@configclass
class PickSingleEgadD242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D24_2_v2.pkl"


@configclass
class PickSingleEgadD243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D24_3_v2.pkl"


@configclass
class PickSingleEgadD250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D25_0_v2.pkl"


@configclass
class PickSingleEgadD251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D25_1_v2.pkl"


@configclass
class PickSingleEgadD252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D25_2_v2.pkl"


@configclass
class PickSingleEgadD253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/D25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/D25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-D25_3_v2.pkl"


@configclass
class PickSingleEgadE100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E10_0_v2.pkl"


@configclass
class PickSingleEgadE101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E10_1_v2.pkl"


@configclass
class PickSingleEgadE102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E10_2_v2.pkl"


@configclass
class PickSingleEgadE103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E10_3_v2.pkl"


@configclass
class PickSingleEgadE111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E11_1_v2.pkl"


@configclass
class PickSingleEgadE112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E11_2_v2.pkl"


@configclass
class PickSingleEgadE113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E11_3_v2.pkl"


@configclass
class PickSingleEgadE120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E12_0_v2.pkl"


@configclass
class PickSingleEgadE121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E12_1_v2.pkl"


@configclass
class PickSingleEgadE122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E12_2_v2.pkl"


@configclass
class PickSingleEgadE123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E12_3_v2.pkl"


@configclass
class PickSingleEgadE131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E13_1_v2.pkl"


@configclass
class PickSingleEgadE132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E13_2_v2.pkl"


@configclass
class PickSingleEgadE133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E13_3_v2.pkl"


@configclass
class PickSingleEgadE140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E14_0_v2.pkl"


@configclass
class PickSingleEgadE141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E14_1_v2.pkl"


@configclass
class PickSingleEgadE142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E14_2_v2.pkl"


@configclass
class PickSingleEgadE143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E14_3_v2.pkl"


@configclass
class PickSingleEgadE150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E15_0_v2.pkl"


@configclass
class PickSingleEgadE151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E15_1_v2.pkl"


@configclass
class PickSingleEgadE152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E15_2_v2.pkl"


@configclass
class PickSingleEgadE153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E15_3_v2.pkl"


@configclass
class PickSingleEgadE160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E16_0_v2.pkl"


@configclass
class PickSingleEgadE161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E16_1_v2.pkl"


@configclass
class PickSingleEgadE162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E16_2_v2.pkl"


@configclass
class PickSingleEgadE163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E16_3_v2.pkl"


@configclass
class PickSingleEgadE170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E17_0_v2.pkl"


@configclass
class PickSingleEgadE171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E17_1_v2.pkl"


@configclass
class PickSingleEgadE172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E17_2_v2.pkl"


@configclass
class PickSingleEgadE181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E18_1_v2.pkl"


@configclass
class PickSingleEgadE182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E18_2_v2.pkl"


@configclass
class PickSingleEgadE190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E19_0_v2.pkl"


@configclass
class PickSingleEgadE191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E19_1_v2.pkl"


@configclass
class PickSingleEgadE192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E19_2_v2.pkl"


@configclass
class PickSingleEgadE193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E19_3_v2.pkl"


@configclass
class PickSingleEgadE200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E20_0_v2.pkl"


@configclass
class PickSingleEgadE201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E20_1_v2.pkl"


@configclass
class PickSingleEgadE202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E20_2_v2.pkl"


@configclass
class PickSingleEgadE210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E21_0_v2.pkl"


@configclass
class PickSingleEgadE211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E21_1_v2.pkl"


@configclass
class PickSingleEgadE212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E21_2_v2.pkl"


@configclass
class PickSingleEgadE213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E21_3_v2.pkl"


@configclass
class PickSingleEgadE220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E22_0_v2.pkl"


@configclass
class PickSingleEgadE221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E22_1_v2.pkl"


@configclass
class PickSingleEgadE222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E22_2_v2.pkl"


@configclass
class PickSingleEgadE223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E22_3_v2.pkl"


@configclass
class PickSingleEgadE230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E23_0_v2.pkl"


@configclass
class PickSingleEgadE231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E23_1_v2.pkl"


@configclass
class PickSingleEgadE232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E23_2_v2.pkl"


@configclass
class PickSingleEgadE233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E23_3_v2.pkl"


@configclass
class PickSingleEgadE240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E24_0_v2.pkl"


@configclass
class PickSingleEgadE241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E24_1_v2.pkl"


@configclass
class PickSingleEgadE242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E24_2_v2.pkl"


@configclass
class PickSingleEgadE243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E24_3_v2.pkl"


@configclass
class PickSingleEgadE250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E25_0_v2.pkl"


@configclass
class PickSingleEgadE251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E25_1_v2.pkl"


@configclass
class PickSingleEgadE252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E25_2_v2.pkl"


@configclass
class PickSingleEgadE253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/E25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/E25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-E25_3_v2.pkl"


@configclass
class PickSingleEgadF100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F10_0_v2.pkl"


@configclass
class PickSingleEgadF101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F10_1_v2.pkl"


@configclass
class PickSingleEgadF103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F10_3_v2.pkl"


@configclass
class PickSingleEgadF110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F11_0_v2.pkl"


@configclass
class PickSingleEgadF111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F11_1_v2.pkl"


@configclass
class PickSingleEgadF112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F11_2_v2.pkl"


@configclass
class PickSingleEgadF113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F11_3_v2.pkl"


@configclass
class PickSingleEgadF121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F12_1_v2.pkl"


@configclass
class PickSingleEgadF122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F12_2_v2.pkl"


@configclass
class PickSingleEgadF130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F13_0_v2.pkl"


@configclass
class PickSingleEgadF131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F13_1_v2.pkl"


@configclass
class PickSingleEgadF132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F13_2_v2.pkl"


@configclass
class PickSingleEgadF133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F13_3_v2.pkl"


@configclass
class PickSingleEgadF140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F14_0_v2.pkl"


@configclass
class PickSingleEgadF142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F14_2_v2.pkl"


@configclass
class PickSingleEgadF143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F14_3_v2.pkl"


@configclass
class PickSingleEgadF150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F15_0_v2.pkl"


@configclass
class PickSingleEgadF151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F15_1_v2.pkl"


@configclass
class PickSingleEgadF152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F15_2_v2.pkl"


@configclass
class PickSingleEgadF153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F15_3_v2.pkl"


@configclass
class PickSingleEgadF160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F16_0_v2.pkl"


@configclass
class PickSingleEgadF161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F16_1_v2.pkl"


@configclass
class PickSingleEgadF162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F16_2_v2.pkl"


@configclass
class PickSingleEgadF163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F16_3_v2.pkl"


@configclass
class PickSingleEgadF170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F17_0_v2.pkl"


@configclass
class PickSingleEgadF171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F17_1_v2.pkl"


@configclass
class PickSingleEgadF172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F17_2_v2.pkl"


@configclass
class PickSingleEgadF173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F17_3_v2.pkl"


@configclass
class PickSingleEgadF180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F18_0_v2.pkl"


@configclass
class PickSingleEgadF181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F18_1_v2.pkl"


@configclass
class PickSingleEgadF182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F18_2_v2.pkl"


@configclass
class PickSingleEgadF183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F18_3_v2.pkl"


@configclass
class PickSingleEgadF190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F19_0_v2.pkl"


@configclass
class PickSingleEgadF191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F19_1_v2.pkl"


@configclass
class PickSingleEgadF192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F19_2_v2.pkl"


@configclass
class PickSingleEgadF193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F19_3_v2.pkl"


@configclass
class PickSingleEgadF200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F20_0_v2.pkl"


@configclass
class PickSingleEgadF202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F20_2_v2.pkl"


@configclass
class PickSingleEgadF203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F20_3_v2.pkl"


@configclass
class PickSingleEgadF210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F21_0_v2.pkl"


@configclass
class PickSingleEgadF211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F21_1_v2.pkl"


@configclass
class PickSingleEgadF212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F21_2_v2.pkl"


@configclass
class PickSingleEgadF213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F21_3_v2.pkl"


@configclass
class PickSingleEgadF220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F22_0_v2.pkl"


@configclass
class PickSingleEgadF221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F22_1_v2.pkl"


@configclass
class PickSingleEgadF222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F22_2_v2.pkl"


@configclass
class PickSingleEgadF223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F22_3_v2.pkl"


@configclass
class PickSingleEgadF230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F23_0_v2.pkl"


@configclass
class PickSingleEgadF231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F23_1_v2.pkl"


@configclass
class PickSingleEgadF232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F23_2_v2.pkl"


@configclass
class PickSingleEgadF233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F23_3_v2.pkl"


@configclass
class PickSingleEgadF240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F24_0_v2.pkl"


@configclass
class PickSingleEgadF241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F24_1_v2.pkl"


@configclass
class PickSingleEgadF242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F24_2_v2.pkl"


@configclass
class PickSingleEgadF243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F24_3_v2.pkl"


@configclass
class PickSingleEgadF250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F25_0_v2.pkl"


@configclass
class PickSingleEgadF251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F25_1_v2.pkl"


@configclass
class PickSingleEgadF252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F25_2_v2.pkl"


@configclass
class PickSingleEgadF253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/F25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/F25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-F25_3_v2.pkl"


@configclass
class PickSingleEgadG100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G10_0_v2.pkl"


@configclass
class PickSingleEgadG101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G10_1_v2.pkl"


@configclass
class PickSingleEgadG102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G10_2_v2.pkl"


@configclass
class PickSingleEgadG103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G10_3_v2.pkl"


@configclass
class PickSingleEgadG110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G11_0_v2.pkl"


@configclass
class PickSingleEgadG111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G11_1_v2.pkl"


@configclass
class PickSingleEgadG112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G11_2_v2.pkl"


@configclass
class PickSingleEgadG113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G11_3_v2.pkl"


@configclass
class PickSingleEgadG120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G12_0_v2.pkl"


@configclass
class PickSingleEgadG122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G12_2_v2.pkl"


@configclass
class PickSingleEgadG123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G12_3_v2.pkl"


@configclass
class PickSingleEgadG130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G13_0_v2.pkl"


@configclass
class PickSingleEgadG131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G13_1_v2.pkl"


@configclass
class PickSingleEgadG132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G13_2_v2.pkl"


@configclass
class PickSingleEgadG133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G13_3_v2.pkl"


@configclass
class PickSingleEgadG140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G14_0_v2.pkl"


@configclass
class PickSingleEgadG141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G14_1_v2.pkl"


@configclass
class PickSingleEgadG142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G14_2_v2.pkl"


@configclass
class PickSingleEgadG143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G14_3_v2.pkl"


@configclass
class PickSingleEgadG150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G15_0_v2.pkl"


@configclass
class PickSingleEgadG151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G15_1_v2.pkl"


@configclass
class PickSingleEgadG152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G15_2_v2.pkl"


@configclass
class PickSingleEgadG160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G16_0_v2.pkl"


@configclass
class PickSingleEgadG161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G16_1_v2.pkl"


@configclass
class PickSingleEgadG162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G16_2_v2.pkl"


@configclass
class PickSingleEgadG163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G16_3_v2.pkl"


@configclass
class PickSingleEgadG170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G17_0_v2.pkl"


@configclass
class PickSingleEgadG171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G17_1_v2.pkl"


@configclass
class PickSingleEgadG172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G17_2_v2.pkl"


@configclass
class PickSingleEgadG173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G17_3_v2.pkl"


@configclass
class PickSingleEgadG181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G18_1_v2.pkl"


@configclass
class PickSingleEgadG182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G18_2_v2.pkl"


@configclass
class PickSingleEgadG183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G18_3_v2.pkl"


@configclass
class PickSingleEgadG191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G19_1_v2.pkl"


@configclass
class PickSingleEgadG192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G19_2_v2.pkl"


@configclass
class PickSingleEgadG193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G19_3_v2.pkl"


@configclass
class PickSingleEgadG200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G20_0_v2.pkl"


@configclass
class PickSingleEgadG201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G20_1_v2.pkl"


@configclass
class PickSingleEgadG202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G20_2_v2.pkl"


@configclass
class PickSingleEgadG203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G20_3_v2.pkl"


@configclass
class PickSingleEgadG210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G21_0_v2.pkl"


@configclass
class PickSingleEgadG211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G21_1_v2.pkl"


@configclass
class PickSingleEgadG213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G21_3_v2.pkl"


@configclass
class PickSingleEgadG220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G22_0_v2.pkl"


@configclass
class PickSingleEgadG221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G22_1_v2.pkl"


@configclass
class PickSingleEgadG222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G22_2_v2.pkl"


@configclass
class PickSingleEgadG223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G22_3_v2.pkl"


@configclass
class PickSingleEgadG230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G23_0_v2.pkl"


@configclass
class PickSingleEgadG231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G23_1_v2.pkl"


@configclass
class PickSingleEgadG233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G23_3_v2.pkl"


@configclass
class PickSingleEgadG240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G24_0_v2.pkl"


@configclass
class PickSingleEgadG241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G24_1_v2.pkl"


@configclass
class PickSingleEgadG242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G24_2_v2.pkl"


@configclass
class PickSingleEgadG243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G24_3_v2.pkl"


@configclass
class PickSingleEgadG250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G25_0_v2.pkl"


@configclass
class PickSingleEgadG251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G25_1_v2.pkl"


@configclass
class PickSingleEgadG252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G25_2_v2.pkl"


@configclass
class PickSingleEgadG253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/G25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/G25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-G25_3_v2.pkl"


@configclass
class PickSingleEgadH100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H10_0_v2.pkl"


@configclass
class PickSingleEgadH101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H10_1_v2.pkl"


@configclass
class PickSingleEgadH102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H10_2_v2.pkl"


@configclass
class PickSingleEgadH103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H10_3_v2.pkl"


@configclass
class PickSingleEgadH110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H11_0_v2.pkl"


@configclass
class PickSingleEgadH111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H11_1_v2.pkl"


@configclass
class PickSingleEgadH112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H11_2_v2.pkl"


@configclass
class PickSingleEgadH113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H11_3_v2.pkl"


@configclass
class PickSingleEgadH120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H12_0_v2.pkl"


@configclass
class PickSingleEgadH121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H12_1_v2.pkl"


@configclass
class PickSingleEgadH122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H12_2_v2.pkl"


@configclass
class PickSingleEgadH123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H12_3_v2.pkl"


@configclass
class PickSingleEgadH130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H13_0_v2.pkl"


@configclass
class PickSingleEgadH131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H13_1_v2.pkl"


@configclass
class PickSingleEgadH132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H13_2_v2.pkl"


@configclass
class PickSingleEgadH140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H14_0_v2.pkl"


@configclass
class PickSingleEgadH141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H14_1_v2.pkl"


@configclass
class PickSingleEgadH142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H14_2_v2.pkl"


@configclass
class PickSingleEgadH143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H14_3_v2.pkl"


@configclass
class PickSingleEgadH150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H15_0_v2.pkl"


@configclass
class PickSingleEgadH151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H15_1_v2.pkl"


@configclass
class PickSingleEgadH152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H15_2_v2.pkl"


@configclass
class PickSingleEgadH153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H15_3_v2.pkl"


@configclass
class PickSingleEgadH160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H16_0_v2.pkl"


@configclass
class PickSingleEgadH161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H16_1_v2.pkl"


@configclass
class PickSingleEgadH162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H16_2_v2.pkl"


@configclass
class PickSingleEgadH163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H16_3_v2.pkl"


@configclass
class PickSingleEgadH170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H17_0_v2.pkl"


@configclass
class PickSingleEgadH171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H17_1_v2.pkl"


@configclass
class PickSingleEgadH172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H17_2_v2.pkl"


@configclass
class PickSingleEgadH173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H17_3_v2.pkl"


@configclass
class PickSingleEgadH181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H18_1_v2.pkl"


@configclass
class PickSingleEgadH182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H18_2_v2.pkl"


@configclass
class PickSingleEgadH183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H18_3_v2.pkl"


@configclass
class PickSingleEgadH190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H19_0_v2.pkl"


@configclass
class PickSingleEgadH191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H19_1_v2.pkl"


@configclass
class PickSingleEgadH192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H19_2_v2.pkl"


@configclass
class PickSingleEgadH193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H19_3_v2.pkl"


@configclass
class PickSingleEgadH200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H20_0_v2.pkl"


@configclass
class PickSingleEgadH201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H20_1_v2.pkl"


@configclass
class PickSingleEgadH202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H20_2_v2.pkl"


@configclass
class PickSingleEgadH203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H20_3_v2.pkl"


@configclass
class PickSingleEgadH210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H21_0_v2.pkl"


@configclass
class PickSingleEgadH211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H21_1_v2.pkl"


@configclass
class PickSingleEgadH212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H21_2_v2.pkl"


@configclass
class PickSingleEgadH220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H22_0_v2.pkl"


@configclass
class PickSingleEgadH221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H22_1_v2.pkl"


@configclass
class PickSingleEgadH222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H22_2_v2.pkl"


@configclass
class PickSingleEgadH223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H22_3_v2.pkl"


@configclass
class PickSingleEgadH230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H23_0_v2.pkl"


@configclass
class PickSingleEgadH231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H23_1_v2.pkl"


@configclass
class PickSingleEgadH240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H24_0_v2.pkl"


@configclass
class PickSingleEgadH241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H24_1_v2.pkl"


@configclass
class PickSingleEgadH242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H24_2_v2.pkl"


@configclass
class PickSingleEgadH243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H24_3_v2.pkl"


@configclass
class PickSingleEgadH250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H25_0_v2.pkl"


@configclass
class PickSingleEgadH251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H25_1_v2.pkl"


@configclass
class PickSingleEgadH252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H25_2_v2.pkl"


@configclass
class PickSingleEgadH253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/H25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/H25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-H25_3_v2.pkl"


@configclass
class PickSingleEgadI070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I07_0_v2.pkl"


@configclass
class PickSingleEgadI071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I07_1_v2.pkl"


@configclass
class PickSingleEgadI072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I07_2_v2.pkl"


@configclass
class PickSingleEgadI073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I07_3_v2.pkl"


@configclass
class PickSingleEgadI080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I08_0_v2.pkl"


@configclass
class PickSingleEgadI081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I08_1_v2.pkl"


@configclass
class PickSingleEgadI083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I08_3_v2.pkl"


@configclass
class PickSingleEgadI090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I09_0_v2.pkl"


@configclass
class PickSingleEgadI091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I09_1_v2.pkl"


@configclass
class PickSingleEgadI092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I09_2_v2.pkl"


@configclass
class PickSingleEgadI102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I10_2_v2.pkl"


@configclass
class PickSingleEgadI103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I10_3_v2.pkl"


@configclass
class PickSingleEgadI110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I11_0_v2.pkl"


@configclass
class PickSingleEgadI111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I11_1_v2.pkl"


@configclass
class PickSingleEgadI112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I11_2_v2.pkl"


@configclass
class PickSingleEgadI113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I11_3_v2.pkl"


@configclass
class PickSingleEgadI120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I12_0_v2.pkl"


@configclass
class PickSingleEgadI121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I12_1_v2.pkl"


@configclass
class PickSingleEgadI122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I12_2_v2.pkl"


@configclass
class PickSingleEgadI123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I12_3_v2.pkl"


@configclass
class PickSingleEgadI130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I13_0_v2.pkl"


@configclass
class PickSingleEgadI131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I13_1_v2.pkl"


@configclass
class PickSingleEgadI132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I13_2_v2.pkl"


@configclass
class PickSingleEgadI133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I13_3_v2.pkl"


@configclass
class PickSingleEgadI140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I14_0_v2.pkl"


@configclass
class PickSingleEgadI141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I14_1_v2.pkl"


@configclass
class PickSingleEgadI142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I14_2_v2.pkl"


@configclass
class PickSingleEgadI143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I14_3_v2.pkl"


@configclass
class PickSingleEgadI150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I15_0_v2.pkl"


@configclass
class PickSingleEgadI151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I15_1_v2.pkl"


@configclass
class PickSingleEgadI152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I15_2_v2.pkl"


@configclass
class PickSingleEgadI153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I15_3_v2.pkl"


@configclass
class PickSingleEgadI160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I16_0_v2.pkl"


@configclass
class PickSingleEgadI161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I16_1_v2.pkl"


@configclass
class PickSingleEgadI162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I16_2_v2.pkl"


@configclass
class PickSingleEgadI163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I16_3_v2.pkl"


@configclass
class PickSingleEgadI170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I17_0_v2.pkl"


@configclass
class PickSingleEgadI171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I17_1_v2.pkl"


@configclass
class PickSingleEgadI172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I17_2_v2.pkl"


@configclass
class PickSingleEgadI173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I17_3_v2.pkl"


@configclass
class PickSingleEgadI180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I18_0_v2.pkl"


@configclass
class PickSingleEgadI181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I18_1_v2.pkl"


@configclass
class PickSingleEgadI182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I18_2_v2.pkl"


@configclass
class PickSingleEgadI183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I18_3_v2.pkl"


@configclass
class PickSingleEgadI190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I19_0_v2.pkl"


@configclass
class PickSingleEgadI191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I19_1_v2.pkl"


@configclass
class PickSingleEgadI192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I19_2_v2.pkl"


@configclass
class PickSingleEgadI200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I20_0_v2.pkl"


@configclass
class PickSingleEgadI201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I20_1_v2.pkl"


@configclass
class PickSingleEgadI203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I20_3_v2.pkl"


@configclass
class PickSingleEgadI210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I21_0_v2.pkl"


@configclass
class PickSingleEgadI211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I21_1_v2.pkl"


@configclass
class PickSingleEgadI213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I21_3_v2.pkl"


@configclass
class PickSingleEgadI220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I22_0_v2.pkl"


@configclass
class PickSingleEgadI221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I22_1_v2.pkl"


@configclass
class PickSingleEgadI223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I22_3_v2.pkl"


@configclass
class PickSingleEgadI230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I23_0_v2.pkl"


@configclass
class PickSingleEgadI232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I23_2_v2.pkl"


@configclass
class PickSingleEgadI233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I23_3_v2.pkl"


@configclass
class PickSingleEgadI240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I24_0_v2.pkl"


@configclass
class PickSingleEgadI241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I24_1_v2.pkl"


@configclass
class PickSingleEgadI242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I24_2_v2.pkl"


@configclass
class PickSingleEgadI243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I24_3_v2.pkl"


@configclass
class PickSingleEgadI250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I25_0_v2.pkl"


@configclass
class PickSingleEgadI251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I25_1_v2.pkl"


@configclass
class PickSingleEgadI252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I25_2_v2.pkl"


@configclass
class PickSingleEgadI253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/I25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/I25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-I25_3_v2.pkl"


@configclass
class PickSingleEgadJ070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J07_0_v2.pkl"


@configclass
class PickSingleEgadJ071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J07_1_v2.pkl"


@configclass
class PickSingleEgadJ072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J07_2_v2.pkl"


@configclass
class PickSingleEgadJ073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J07_3_v2.pkl"


@configclass
class PickSingleEgadJ080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J08_0_v2.pkl"


@configclass
class PickSingleEgadJ082MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J08_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J08_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J08_2_v2.pkl"


@configclass
class PickSingleEgadJ083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J08_3_v2.pkl"


@configclass
class PickSingleEgadJ090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J09_0_v2.pkl"


@configclass
class PickSingleEgadJ091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J09_1_v2.pkl"


@configclass
class PickSingleEgadJ092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J09_2_v2.pkl"


@configclass
class PickSingleEgadJ100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J10_0_v2.pkl"


@configclass
class PickSingleEgadJ101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J10_1_v2.pkl"


@configclass
class PickSingleEgadJ102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J10_2_v2.pkl"


@configclass
class PickSingleEgadJ103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J10_3_v2.pkl"


@configclass
class PickSingleEgadJ110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J11_0_v2.pkl"


@configclass
class PickSingleEgadJ111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J11_1_v2.pkl"


@configclass
class PickSingleEgadJ112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J11_2_v2.pkl"


@configclass
class PickSingleEgadJ113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J11_3_v2.pkl"


@configclass
class PickSingleEgadJ120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J12_0_v2.pkl"


@configclass
class PickSingleEgadJ121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J12_1_v2.pkl"


@configclass
class PickSingleEgadJ122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J12_2_v2.pkl"


@configclass
class PickSingleEgadJ123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J12_3_v2.pkl"


@configclass
class PickSingleEgadJ130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J13_0_v2.pkl"


@configclass
class PickSingleEgadJ131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J13_1_v2.pkl"


@configclass
class PickSingleEgadJ132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J13_2_v2.pkl"


@configclass
class PickSingleEgadJ133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J13_3_v2.pkl"


@configclass
class PickSingleEgadJ140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J14_0_v2.pkl"


@configclass
class PickSingleEgadJ141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J14_1_v2.pkl"


@configclass
class PickSingleEgadJ142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J14_2_v2.pkl"


@configclass
class PickSingleEgadJ143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J14_3_v2.pkl"


@configclass
class PickSingleEgadJ150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J15_0_v2.pkl"


@configclass
class PickSingleEgadJ151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J15_1_v2.pkl"


@configclass
class PickSingleEgadJ152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J15_2_v2.pkl"


@configclass
class PickSingleEgadJ153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J15_3_v2.pkl"


@configclass
class PickSingleEgadJ160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J16_0_v2.pkl"


@configclass
class PickSingleEgadJ162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J16_2_v2.pkl"


@configclass
class PickSingleEgadJ163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J16_3_v2.pkl"


@configclass
class PickSingleEgadJ170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J17_0_v2.pkl"


@configclass
class PickSingleEgadJ171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J17_1_v2.pkl"


@configclass
class PickSingleEgadJ172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J17_2_v2.pkl"


@configclass
class PickSingleEgadJ173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J17_3_v2.pkl"


@configclass
class PickSingleEgadJ180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J18_0_v2.pkl"


@configclass
class PickSingleEgadJ181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J18_1_v2.pkl"


@configclass
class PickSingleEgadJ182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J18_2_v2.pkl"


@configclass
class PickSingleEgadJ183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J18_3_v2.pkl"


@configclass
class PickSingleEgadJ190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J19_0_v2.pkl"


@configclass
class PickSingleEgadJ191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J19_1_v2.pkl"


@configclass
class PickSingleEgadJ192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J19_2_v2.pkl"


@configclass
class PickSingleEgadJ193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J19_3_v2.pkl"


@configclass
class PickSingleEgadJ200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J20_0_v2.pkl"


@configclass
class PickSingleEgadJ201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J20_1_v2.pkl"


@configclass
class PickSingleEgadJ202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J20_2_v2.pkl"


@configclass
class PickSingleEgadJ203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J20_3_v2.pkl"


@configclass
class PickSingleEgadJ210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J21_0_v2.pkl"


@configclass
class PickSingleEgadJ211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J21_1_v2.pkl"


@configclass
class PickSingleEgadJ212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J21_2_v2.pkl"


@configclass
class PickSingleEgadJ213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J21_3_v2.pkl"


@configclass
class PickSingleEgadJ220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J22_0_v2.pkl"


@configclass
class PickSingleEgadJ221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J22_1_v2.pkl"


@configclass
class PickSingleEgadJ222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J22_2_v2.pkl"


@configclass
class PickSingleEgadJ223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J22_3_v2.pkl"


@configclass
class PickSingleEgadJ230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J23_0_v2.pkl"


@configclass
class PickSingleEgadJ231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J23_1_v2.pkl"


@configclass
class PickSingleEgadJ232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J23_2_v2.pkl"


@configclass
class PickSingleEgadJ233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J23_3_v2.pkl"


@configclass
class PickSingleEgadJ240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J24_0_v2.pkl"


@configclass
class PickSingleEgadJ241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J24_1_v2.pkl"


@configclass
class PickSingleEgadJ242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J24_2_v2.pkl"


@configclass
class PickSingleEgadJ243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J24_3_v2.pkl"


@configclass
class PickSingleEgadJ250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J25_0_v2.pkl"


@configclass
class PickSingleEgadJ251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J25_1_v2.pkl"


@configclass
class PickSingleEgadJ252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J25_2_v2.pkl"


@configclass
class PickSingleEgadJ253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/J25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/J25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-J25_3_v2.pkl"


@configclass
class PickSingleEgadK070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K07_0_v2.pkl"


@configclass
class PickSingleEgadK071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K07_1_v2.pkl"


@configclass
class PickSingleEgadK072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K07_2_v2.pkl"


@configclass
class PickSingleEgadK073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K07_3_v2.pkl"


@configclass
class PickSingleEgadK080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K08_0_v2.pkl"


@configclass
class PickSingleEgadK081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K08_1_v2.pkl"


@configclass
class PickSingleEgadK082MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K08_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K08_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K08_2_v2.pkl"


@configclass
class PickSingleEgadK083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K08_3_v2.pkl"


@configclass
class PickSingleEgadK090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K09_0_v2.pkl"


@configclass
class PickSingleEgadK092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K09_2_v2.pkl"


@configclass
class PickSingleEgadK093MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K09_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K09_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K09_3_v2.pkl"


@configclass
class PickSingleEgadK100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K10_0_v2.pkl"


@configclass
class PickSingleEgadK101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K10_1_v2.pkl"


@configclass
class PickSingleEgadK102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K10_2_v2.pkl"


@configclass
class PickSingleEgadK103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K10_3_v2.pkl"


@configclass
class PickSingleEgadK110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K11_0_v2.pkl"


@configclass
class PickSingleEgadK111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K11_1_v2.pkl"


@configclass
class PickSingleEgadK112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K11_2_v2.pkl"


@configclass
class PickSingleEgadK113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K11_3_v2.pkl"


@configclass
class PickSingleEgadK120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K12_0_v2.pkl"


@configclass
class PickSingleEgadK121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K12_1_v2.pkl"


@configclass
class PickSingleEgadK122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K12_2_v2.pkl"


@configclass
class PickSingleEgadK123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K12_3_v2.pkl"


@configclass
class PickSingleEgadK130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K13_0_v2.pkl"


@configclass
class PickSingleEgadK132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K13_2_v2.pkl"


@configclass
class PickSingleEgadK140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K14_0_v2.pkl"


@configclass
class PickSingleEgadK142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K14_2_v2.pkl"


@configclass
class PickSingleEgadK143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K14_3_v2.pkl"


@configclass
class PickSingleEgadK150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K15_0_v2.pkl"


@configclass
class PickSingleEgadK151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K15_1_v2.pkl"


@configclass
class PickSingleEgadK152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K15_2_v2.pkl"


@configclass
class PickSingleEgadK153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K15_3_v2.pkl"


@configclass
class PickSingleEgadK160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K16_0_v2.pkl"


@configclass
class PickSingleEgadK161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K16_1_v2.pkl"


@configclass
class PickSingleEgadK163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K16_3_v2.pkl"


@configclass
class PickSingleEgadK170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K17_0_v2.pkl"


@configclass
class PickSingleEgadK171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K17_1_v2.pkl"


@configclass
class PickSingleEgadK172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K17_2_v2.pkl"


@configclass
class PickSingleEgadK173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K17_3_v2.pkl"


@configclass
class PickSingleEgadK180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K18_0_v2.pkl"


@configclass
class PickSingleEgadK181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K18_1_v2.pkl"


@configclass
class PickSingleEgadK182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K18_2_v2.pkl"


@configclass
class PickSingleEgadK183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K18_3_v2.pkl"


@configclass
class PickSingleEgadK190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K19_0_v2.pkl"


@configclass
class PickSingleEgadK191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K19_1_v2.pkl"


@configclass
class PickSingleEgadK192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K19_2_v2.pkl"


@configclass
class PickSingleEgadK193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K19_3_v2.pkl"


@configclass
class PickSingleEgadK200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K20_0_v2.pkl"


@configclass
class PickSingleEgadK201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K20_1_v2.pkl"


@configclass
class PickSingleEgadK202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K20_2_v2.pkl"


@configclass
class PickSingleEgadK203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K20_3_v2.pkl"


@configclass
class PickSingleEgadK210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K21_0_v2.pkl"


@configclass
class PickSingleEgadK211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K21_1_v2.pkl"


@configclass
class PickSingleEgadK212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K21_2_v2.pkl"


@configclass
class PickSingleEgadK213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K21_3_v2.pkl"


@configclass
class PickSingleEgadK220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K22_0_v2.pkl"


@configclass
class PickSingleEgadK221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K22_1_v2.pkl"


@configclass
class PickSingleEgadK222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K22_2_v2.pkl"


@configclass
class PickSingleEgadK223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K22_3_v2.pkl"


@configclass
class PickSingleEgadK230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K23_0_v2.pkl"


@configclass
class PickSingleEgadK231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K23_1_v2.pkl"


@configclass
class PickSingleEgadK232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K23_2_v2.pkl"


@configclass
class PickSingleEgadK233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K23_3_v2.pkl"


@configclass
class PickSingleEgadK240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K24_0_v2.pkl"


@configclass
class PickSingleEgadK241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K24_1_v2.pkl"


@configclass
class PickSingleEgadK242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K24_2_v2.pkl"


@configclass
class PickSingleEgadK243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K24_3_v2.pkl"


@configclass
class PickSingleEgadK250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K25_0_v2.pkl"


@configclass
class PickSingleEgadK251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K25_1_v2.pkl"


@configclass
class PickSingleEgadK252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K25_2_v2.pkl"


@configclass
class PickSingleEgadK253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/K25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/K25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-K25_3_v2.pkl"


@configclass
class PickSingleEgadL070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L07_0_v2.pkl"


@configclass
class PickSingleEgadL071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L07_1_v2.pkl"


@configclass
class PickSingleEgadL072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L07_2_v2.pkl"


@configclass
class PickSingleEgadL073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L07_3_v2.pkl"


@configclass
class PickSingleEgadL080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L08_0_v2.pkl"


@configclass
class PickSingleEgadL081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L08_1_v2.pkl"


@configclass
class PickSingleEgadL082MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L08_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L08_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L08_2_v2.pkl"


@configclass
class PickSingleEgadL083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L08_3_v2.pkl"


@configclass
class PickSingleEgadL090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L09_0_v2.pkl"


@configclass
class PickSingleEgadL091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L09_1_v2.pkl"


@configclass
class PickSingleEgadL092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L09_2_v2.pkl"


@configclass
class PickSingleEgadL093MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L09_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L09_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L09_3_v2.pkl"


@configclass
class PickSingleEgadL100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L10_0_v2.pkl"


@configclass
class PickSingleEgadL101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L10_1_v2.pkl"


@configclass
class PickSingleEgadL102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L10_2_v2.pkl"


@configclass
class PickSingleEgadL110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L11_0_v2.pkl"


@configclass
class PickSingleEgadL111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L11_1_v2.pkl"


@configclass
class PickSingleEgadL112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L11_2_v2.pkl"


@configclass
class PickSingleEgadL113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L11_3_v2.pkl"


@configclass
class PickSingleEgadL120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L12_0_v2.pkl"


@configclass
class PickSingleEgadL121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L12_1_v2.pkl"


@configclass
class PickSingleEgadL122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L12_2_v2.pkl"


@configclass
class PickSingleEgadL123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L12_3_v2.pkl"


@configclass
class PickSingleEgadL130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L13_0_v2.pkl"


@configclass
class PickSingleEgadL131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L13_1_v2.pkl"


@configclass
class PickSingleEgadL132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L13_2_v2.pkl"


@configclass
class PickSingleEgadL133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L13_3_v2.pkl"


@configclass
class PickSingleEgadL141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L14_1_v2.pkl"


@configclass
class PickSingleEgadL142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L14_2_v2.pkl"


@configclass
class PickSingleEgadL143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L14_3_v2.pkl"


@configclass
class PickSingleEgadL150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L15_0_v2.pkl"


@configclass
class PickSingleEgadL151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L15_1_v2.pkl"


@configclass
class PickSingleEgadL153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L15_3_v2.pkl"


@configclass
class PickSingleEgadL160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L16_0_v2.pkl"


@configclass
class PickSingleEgadL161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L16_1_v2.pkl"


@configclass
class PickSingleEgadL162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L16_2_v2.pkl"


@configclass
class PickSingleEgadL163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L16_3_v2.pkl"


@configclass
class PickSingleEgadL171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L17_1_v2.pkl"


@configclass
class PickSingleEgadL172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L17_2_v2.pkl"


@configclass
class PickSingleEgadL173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L17_3_v2.pkl"


@configclass
class PickSingleEgadL180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L18_0_v2.pkl"


@configclass
class PickSingleEgadL181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L18_1_v2.pkl"


@configclass
class PickSingleEgadL182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L18_2_v2.pkl"


@configclass
class PickSingleEgadL183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L18_3_v2.pkl"


@configclass
class PickSingleEgadL191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L19_1_v2.pkl"


@configclass
class PickSingleEgadL192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L19_2_v2.pkl"


@configclass
class PickSingleEgadL193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L19_3_v2.pkl"


@configclass
class PickSingleEgadL200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L20_0_v2.pkl"


@configclass
class PickSingleEgadL201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L20_1_v2.pkl"


@configclass
class PickSingleEgadL202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L20_2_v2.pkl"


@configclass
class PickSingleEgadL203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L20_3_v2.pkl"


@configclass
class PickSingleEgadL210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L21_0_v2.pkl"


@configclass
class PickSingleEgadL211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L21_1_v2.pkl"


@configclass
class PickSingleEgadL212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L21_2_v2.pkl"


@configclass
class PickSingleEgadL213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L21_3_v2.pkl"


@configclass
class PickSingleEgadL220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L22_0_v2.pkl"


@configclass
class PickSingleEgadL221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L22_1_v2.pkl"


@configclass
class PickSingleEgadL222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L22_2_v2.pkl"


@configclass
class PickSingleEgadL223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L22_3_v2.pkl"


@configclass
class PickSingleEgadL230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L23_0_v2.pkl"


@configclass
class PickSingleEgadL231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L23_1_v2.pkl"


@configclass
class PickSingleEgadL232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L23_2_v2.pkl"


@configclass
class PickSingleEgadL233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L23_3_v2.pkl"


@configclass
class PickSingleEgadL240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L24_0_v2.pkl"


@configclass
class PickSingleEgadL241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L24_1_v2.pkl"


@configclass
class PickSingleEgadL243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L24_3_v2.pkl"


@configclass
class PickSingleEgadL250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L25_0_v2.pkl"


@configclass
class PickSingleEgadL251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L25_1_v2.pkl"


@configclass
class PickSingleEgadL252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L25_2_v2.pkl"


@configclass
class PickSingleEgadL253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/L25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/L25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-L25_3_v2.pkl"


@configclass
class PickSingleEgadM051MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M05_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M05_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M05_1_v2.pkl"


@configclass
class PickSingleEgadM052MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M05_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M05_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M05_2_v2.pkl"


@configclass
class PickSingleEgadM053MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M05_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M05_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M05_3_v2.pkl"


@configclass
class PickSingleEgadM061MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M06_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M06_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M06_1_v2.pkl"


@configclass
class PickSingleEgadM062MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M06_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M06_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M06_2_v2.pkl"


@configclass
class PickSingleEgadM063MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M06_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M06_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M06_3_v2.pkl"


@configclass
class PickSingleEgadM070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M07_0_v2.pkl"


@configclass
class PickSingleEgadM071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M07_1_v2.pkl"


@configclass
class PickSingleEgadM073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M07_3_v2.pkl"


@configclass
class PickSingleEgadM080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M08_0_v2.pkl"


@configclass
class PickSingleEgadM082MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M08_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M08_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M08_2_v2.pkl"


@configclass
class PickSingleEgadM083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M08_3_v2.pkl"


@configclass
class PickSingleEgadM090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M09_0_v2.pkl"


@configclass
class PickSingleEgadM091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M09_1_v2.pkl"


@configclass
class PickSingleEgadM092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M09_2_v2.pkl"


@configclass
class PickSingleEgadM093MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M09_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M09_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M09_3_v2.pkl"


@configclass
class PickSingleEgadM100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M10_0_v2.pkl"


@configclass
class PickSingleEgadM101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M10_1_v2.pkl"


@configclass
class PickSingleEgadM102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M10_2_v2.pkl"


@configclass
class PickSingleEgadM103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M10_3_v2.pkl"


@configclass
class PickSingleEgadM110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M11_0_v2.pkl"


@configclass
class PickSingleEgadM111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M11_1_v2.pkl"


@configclass
class PickSingleEgadM112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M11_2_v2.pkl"


@configclass
class PickSingleEgadM113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M11_3_v2.pkl"


@configclass
class PickSingleEgadM120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M12_0_v2.pkl"


@configclass
class PickSingleEgadM121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M12_1_v2.pkl"


@configclass
class PickSingleEgadM122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M12_2_v2.pkl"


@configclass
class PickSingleEgadM123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M12_3_v2.pkl"


@configclass
class PickSingleEgadM130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M13_0_v2.pkl"


@configclass
class PickSingleEgadM131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M13_1_v2.pkl"


@configclass
class PickSingleEgadM132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M13_2_v2.pkl"


@configclass
class PickSingleEgadM133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M13_3_v2.pkl"


@configclass
class PickSingleEgadM140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M14_0_v2.pkl"


@configclass
class PickSingleEgadM141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M14_1_v2.pkl"


@configclass
class PickSingleEgadM142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M14_2_v2.pkl"


@configclass
class PickSingleEgadM143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M14_3_v2.pkl"


@configclass
class PickSingleEgadM150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M15_0_v2.pkl"


@configclass
class PickSingleEgadM151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M15_1_v2.pkl"


@configclass
class PickSingleEgadM152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M15_2_v2.pkl"


@configclass
class PickSingleEgadM153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M15_3_v2.pkl"


@configclass
class PickSingleEgadM160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M16_0_v2.pkl"


@configclass
class PickSingleEgadM161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M16_1_v2.pkl"


@configclass
class PickSingleEgadM162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M16_2_v2.pkl"


@configclass
class PickSingleEgadM163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M16_3_v2.pkl"


@configclass
class PickSingleEgadM171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M17_1_v2.pkl"


@configclass
class PickSingleEgadM172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M17_2_v2.pkl"


@configclass
class PickSingleEgadM173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M17_3_v2.pkl"


@configclass
class PickSingleEgadM180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M18_0_v2.pkl"


@configclass
class PickSingleEgadM181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M18_1_v2.pkl"


@configclass
class PickSingleEgadM182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M18_2_v2.pkl"


@configclass
class PickSingleEgadM183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M18_3_v2.pkl"


@configclass
class PickSingleEgadM190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M19_0_v2.pkl"


@configclass
class PickSingleEgadM191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M19_1_v2.pkl"


@configclass
class PickSingleEgadM193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M19_3_v2.pkl"


@configclass
class PickSingleEgadM200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M20_0_v2.pkl"


@configclass
class PickSingleEgadM201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M20_1_v2.pkl"


@configclass
class PickSingleEgadM202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M20_2_v2.pkl"


@configclass
class PickSingleEgadM203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M20_3_v2.pkl"


@configclass
class PickSingleEgadM210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M21_0_v2.pkl"


@configclass
class PickSingleEgadM211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M21_1_v2.pkl"


@configclass
class PickSingleEgadM213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M21_3_v2.pkl"


@configclass
class PickSingleEgadM221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M22_1_v2.pkl"


@configclass
class PickSingleEgadM222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M22_2_v2.pkl"


@configclass
class PickSingleEgadM223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M22_3_v2.pkl"


@configclass
class PickSingleEgadM230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M23_0_v2.pkl"


@configclass
class PickSingleEgadM231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M23_1_v2.pkl"


@configclass
class PickSingleEgadM232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M23_2_v2.pkl"


@configclass
class PickSingleEgadM233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M23_3_v2.pkl"


@configclass
class PickSingleEgadM240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M24_0_v2.pkl"


@configclass
class PickSingleEgadM241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M24_1_v2.pkl"


@configclass
class PickSingleEgadM242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M24_2_v2.pkl"


@configclass
class PickSingleEgadM243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M24_3_v2.pkl"


@configclass
class PickSingleEgadM250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M25_0_v2.pkl"


@configclass
class PickSingleEgadM251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M25_1_v2.pkl"


@configclass
class PickSingleEgadM252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M25_2_v2.pkl"


@configclass
class PickSingleEgadM253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/M25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/M25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-M25_3_v2.pkl"


@configclass
class PickSingleEgadN050MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N05_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N05_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N05_0_v2.pkl"


@configclass
class PickSingleEgadN051MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N05_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N05_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N05_1_v2.pkl"


@configclass
class PickSingleEgadN052MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N05_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N05_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N05_2_v2.pkl"


@configclass
class PickSingleEgadN060MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N06_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N06_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N06_0_v2.pkl"


@configclass
class PickSingleEgadN061MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N06_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N06_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N06_1_v2.pkl"


@configclass
class PickSingleEgadN062MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N06_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N06_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N06_2_v2.pkl"


@configclass
class PickSingleEgadN063MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N06_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N06_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N06_3_v2.pkl"


@configclass
class PickSingleEgadN070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N07_0_v2.pkl"


@configclass
class PickSingleEgadN071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N07_1_v2.pkl"


@configclass
class PickSingleEgadN072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N07_2_v2.pkl"


@configclass
class PickSingleEgadN073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N07_3_v2.pkl"


@configclass
class PickSingleEgadN080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N08_0_v2.pkl"


@configclass
class PickSingleEgadN081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N08_1_v2.pkl"


@configclass
class PickSingleEgadN083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N08_3_v2.pkl"


@configclass
class PickSingleEgadN090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N09_0_v2.pkl"


@configclass
class PickSingleEgadN091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N09_1_v2.pkl"


@configclass
class PickSingleEgadN092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N09_2_v2.pkl"


@configclass
class PickSingleEgadN093MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N09_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N09_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N09_3_v2.pkl"


@configclass
class PickSingleEgadN100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N10_0_v2.pkl"


@configclass
class PickSingleEgadN101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N10_1_v2.pkl"


@configclass
class PickSingleEgadN103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N10_3_v2.pkl"


@configclass
class PickSingleEgadN110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N11_0_v2.pkl"


@configclass
class PickSingleEgadN111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N11_1_v2.pkl"


@configclass
class PickSingleEgadN112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N11_2_v2.pkl"


@configclass
class PickSingleEgadN113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N11_3_v2.pkl"


@configclass
class PickSingleEgadN120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N12_0_v2.pkl"


@configclass
class PickSingleEgadN121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N12_1_v2.pkl"


@configclass
class PickSingleEgadN123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N12_3_v2.pkl"


@configclass
class PickSingleEgadN130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N13_0_v2.pkl"


@configclass
class PickSingleEgadN131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N13_1_v2.pkl"


@configclass
class PickSingleEgadN133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N13_3_v2.pkl"


@configclass
class PickSingleEgadN143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N14_3_v2.pkl"


@configclass
class PickSingleEgadN150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N15_0_v2.pkl"


@configclass
class PickSingleEgadN151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N15_1_v2.pkl"


@configclass
class PickSingleEgadN152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N15_2_v2.pkl"


@configclass
class PickSingleEgadN153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N15_3_v2.pkl"


@configclass
class PickSingleEgadN160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N16_0_v2.pkl"


@configclass
class PickSingleEgadN161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N16_1_v2.pkl"


@configclass
class PickSingleEgadN162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N16_2_v2.pkl"


@configclass
class PickSingleEgadN163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N16_3_v2.pkl"


@configclass
class PickSingleEgadN170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N17_0_v2.pkl"


@configclass
class PickSingleEgadN171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N17_1_v2.pkl"


@configclass
class PickSingleEgadN172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N17_2_v2.pkl"


@configclass
class PickSingleEgadN173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N17_3_v2.pkl"


@configclass
class PickSingleEgadN180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N18_0_v2.pkl"


@configclass
class PickSingleEgadN181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N18_1_v2.pkl"


@configclass
class PickSingleEgadN182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N18_2_v2.pkl"


@configclass
class PickSingleEgadN183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N18_3_v2.pkl"


@configclass
class PickSingleEgadN190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N19_0_v2.pkl"


@configclass
class PickSingleEgadN191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N19_1_v2.pkl"


@configclass
class PickSingleEgadN192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N19_2_v2.pkl"


@configclass
class PickSingleEgadN193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N19_3_v2.pkl"


@configclass
class PickSingleEgadN200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N20_0_v2.pkl"


@configclass
class PickSingleEgadN201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N20_1_v2.pkl"


@configclass
class PickSingleEgadN202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N20_2_v2.pkl"


@configclass
class PickSingleEgadN203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N20_3_v2.pkl"


@configclass
class PickSingleEgadN210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N21_0_v2.pkl"


@configclass
class PickSingleEgadN211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N21_1_v2.pkl"


@configclass
class PickSingleEgadN212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N21_2_v2.pkl"


@configclass
class PickSingleEgadN213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N21_3_v2.pkl"


@configclass
class PickSingleEgadN220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N22_0_v2.pkl"


@configclass
class PickSingleEgadN222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N22_2_v2.pkl"


@configclass
class PickSingleEgadN223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N22_3_v2.pkl"


@configclass
class PickSingleEgadN230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N23_0_v2.pkl"


@configclass
class PickSingleEgadN231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N23_1_v2.pkl"


@configclass
class PickSingleEgadN233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N23_3_v2.pkl"


@configclass
class PickSingleEgadN240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N24_0_v2.pkl"


@configclass
class PickSingleEgadN241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N24_1_v2.pkl"


@configclass
class PickSingleEgadN242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N24_2_v2.pkl"


@configclass
class PickSingleEgadN243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N24_3_v2.pkl"


@configclass
class PickSingleEgadN250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N25_0_v2.pkl"


@configclass
class PickSingleEgadN251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N25_1_v2.pkl"


@configclass
class PickSingleEgadN252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N25_2_v2.pkl"


@configclass
class PickSingleEgadN253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/N25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/N25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-N25_3_v2.pkl"


@configclass
class PickSingleEgadO050MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O05_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O05_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O05_0_v2.pkl"


@configclass
class PickSingleEgadO051MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O05_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O05_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O05_1_v2.pkl"


@configclass
class PickSingleEgadO053MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O05_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O05_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O05_3_v2.pkl"


@configclass
class PickSingleEgadO060MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O06_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O06_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O06_0_v2.pkl"


@configclass
class PickSingleEgadO061MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O06_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O06_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O06_1_v2.pkl"


@configclass
class PickSingleEgadO062MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O06_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O06_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O06_2_v2.pkl"


@configclass
class PickSingleEgadO063MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O06_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O06_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O06_3_v2.pkl"


@configclass
class PickSingleEgadO070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O07_0_v2.pkl"


@configclass
class PickSingleEgadO072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O07_2_v2.pkl"


@configclass
class PickSingleEgadO073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O07_3_v2.pkl"


@configclass
class PickSingleEgadO080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O08_0_v2.pkl"


@configclass
class PickSingleEgadO081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O08_1_v2.pkl"


@configclass
class PickSingleEgadO082MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O08_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O08_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O08_2_v2.pkl"


@configclass
class PickSingleEgadO083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O08_3_v2.pkl"


@configclass
class PickSingleEgadO090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O09_0_v2.pkl"


@configclass
class PickSingleEgadO091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O09_1_v2.pkl"


@configclass
class PickSingleEgadO092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O09_2_v2.pkl"


@configclass
class PickSingleEgadO093MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O09_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O09_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O09_3_v2.pkl"


@configclass
class PickSingleEgadO100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O10_0_v2.pkl"


@configclass
class PickSingleEgadO101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O10_1_v2.pkl"


@configclass
class PickSingleEgadO102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O10_2_v2.pkl"


@configclass
class PickSingleEgadO103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O10_3_v2.pkl"


@configclass
class PickSingleEgadO110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O11_0_v2.pkl"


@configclass
class PickSingleEgadO112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O11_2_v2.pkl"


@configclass
class PickSingleEgadO113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O11_3_v2.pkl"


@configclass
class PickSingleEgadO120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O12_0_v2.pkl"


@configclass
class PickSingleEgadO121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O12_1_v2.pkl"


@configclass
class PickSingleEgadO122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O12_2_v2.pkl"


@configclass
class PickSingleEgadO123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O12_3_v2.pkl"


@configclass
class PickSingleEgadO130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O13_0_v2.pkl"


@configclass
class PickSingleEgadO131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O13_1_v2.pkl"


@configclass
class PickSingleEgadO132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O13_2_v2.pkl"


@configclass
class PickSingleEgadO133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O13_3_v2.pkl"


@configclass
class PickSingleEgadO140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O14_0_v2.pkl"


@configclass
class PickSingleEgadO141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O14_1_v2.pkl"


@configclass
class PickSingleEgadO142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O14_2_v2.pkl"


@configclass
class PickSingleEgadO150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O15_0_v2.pkl"


@configclass
class PickSingleEgadO151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O15_1_v2.pkl"


@configclass
class PickSingleEgadO152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O15_2_v2.pkl"


@configclass
class PickSingleEgadO153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O15_3_v2.pkl"


@configclass
class PickSingleEgadO160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O16_0_v2.pkl"


@configclass
class PickSingleEgadO162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O16_2_v2.pkl"


@configclass
class PickSingleEgadO163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O16_3_v2.pkl"


@configclass
class PickSingleEgadO170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O17_0_v2.pkl"


@configclass
class PickSingleEgadO171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O17_1_v2.pkl"


@configclass
class PickSingleEgadO172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O17_2_v2.pkl"


@configclass
class PickSingleEgadO173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O17_3_v2.pkl"


@configclass
class PickSingleEgadO180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O18_0_v2.pkl"


@configclass
class PickSingleEgadO181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O18_1_v2.pkl"


@configclass
class PickSingleEgadO182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O18_2_v2.pkl"


@configclass
class PickSingleEgadO183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O18_3_v2.pkl"


@configclass
class PickSingleEgadO190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O19_0_v2.pkl"


@configclass
class PickSingleEgadO191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O19_1_v2.pkl"


@configclass
class PickSingleEgadO192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O19_2_v2.pkl"


@configclass
class PickSingleEgadO193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O19_3_v2.pkl"


@configclass
class PickSingleEgadO200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O20_0_v2.pkl"


@configclass
class PickSingleEgadO201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O20_1_v2.pkl"


@configclass
class PickSingleEgadO202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O20_2_v2.pkl"


@configclass
class PickSingleEgadO203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O20_3_v2.pkl"


@configclass
class PickSingleEgadO211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O21_1_v2.pkl"


@configclass
class PickSingleEgadO212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O21_2_v2.pkl"


@configclass
class PickSingleEgadO213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O21_3_v2.pkl"


@configclass
class PickSingleEgadO220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O22_0_v2.pkl"


@configclass
class PickSingleEgadO221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O22_1_v2.pkl"


@configclass
class PickSingleEgadO222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O22_2_v2.pkl"


@configclass
class PickSingleEgadO223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O22_3_v2.pkl"


@configclass
class PickSingleEgadO230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O23_0_v2.pkl"


@configclass
class PickSingleEgadO231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O23_1_v2.pkl"


@configclass
class PickSingleEgadO232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O23_2_v2.pkl"


@configclass
class PickSingleEgadO233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O23_3_v2.pkl"


@configclass
class PickSingleEgadO240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O24_0_v2.pkl"


@configclass
class PickSingleEgadO241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O24_1_v2.pkl"


@configclass
class PickSingleEgadO242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O24_2_v2.pkl"


@configclass
class PickSingleEgadO243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O24_3_v2.pkl"


@configclass
class PickSingleEgadO250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O25_0_v2.pkl"


@configclass
class PickSingleEgadO251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O25_1_v2.pkl"


@configclass
class PickSingleEgadO252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O25_2_v2.pkl"


@configclass
class PickSingleEgadO253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/O25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/O25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-O25_3_v2.pkl"


@configclass
class PickSingleEgadP050MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P05_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P05_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P05_0_v2.pkl"


@configclass
class PickSingleEgadP051MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P05_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P05_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P05_1_v2.pkl"


@configclass
class PickSingleEgadP052MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P05_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P05_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P05_2_v2.pkl"


@configclass
class PickSingleEgadP053MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P05_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P05_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P05_3_v2.pkl"


@configclass
class PickSingleEgadP060MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P06_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P06_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P06_0_v2.pkl"


@configclass
class PickSingleEgadP061MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P06_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P06_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P06_1_v2.pkl"


@configclass
class PickSingleEgadP062MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P06_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P06_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P06_2_v2.pkl"


@configclass
class PickSingleEgadP070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P07_0_v2.pkl"


@configclass
class PickSingleEgadP071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P07_1_v2.pkl"


@configclass
class PickSingleEgadP072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P07_2_v2.pkl"


@configclass
class PickSingleEgadP080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P08_0_v2.pkl"


@configclass
class PickSingleEgadP081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P08_1_v2.pkl"


@configclass
class PickSingleEgadP083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P08_3_v2.pkl"


@configclass
class PickSingleEgadP090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P09_0_v2.pkl"


@configclass
class PickSingleEgadP091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P09_1_v2.pkl"


@configclass
class PickSingleEgadP092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P09_2_v2.pkl"


@configclass
class PickSingleEgadP093MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P09_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P09_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P09_3_v2.pkl"


@configclass
class PickSingleEgadP100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P10_0_v2.pkl"


@configclass
class PickSingleEgadP101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P10_1_v2.pkl"


@configclass
class PickSingleEgadP102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P10_2_v2.pkl"


@configclass
class PickSingleEgadP103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P10_3_v2.pkl"


@configclass
class PickSingleEgadP110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P11_0_v2.pkl"


@configclass
class PickSingleEgadP111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P11_1_v2.pkl"


@configclass
class PickSingleEgadP112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P11_2_v2.pkl"


@configclass
class PickSingleEgadP113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P11_3_v2.pkl"


@configclass
class PickSingleEgadP120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P12_0_v2.pkl"


@configclass
class PickSingleEgadP121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P12_1_v2.pkl"


@configclass
class PickSingleEgadP122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P12_2_v2.pkl"


@configclass
class PickSingleEgadP123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P12_3_v2.pkl"


@configclass
class PickSingleEgadP130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P13_0_v2.pkl"


@configclass
class PickSingleEgadP131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P13_1_v2.pkl"


@configclass
class PickSingleEgadP132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P13_2_v2.pkl"


@configclass
class PickSingleEgadP133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P13_3_v2.pkl"


@configclass
class PickSingleEgadP140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P14_0_v2.pkl"


@configclass
class PickSingleEgadP141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P14_1_v2.pkl"


@configclass
class PickSingleEgadP142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P14_2_v2.pkl"


@configclass
class PickSingleEgadP143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P14_3_v2.pkl"


@configclass
class PickSingleEgadP150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P15_0_v2.pkl"


@configclass
class PickSingleEgadP151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P15_1_v2.pkl"


@configclass
class PickSingleEgadP152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P15_2_v2.pkl"


@configclass
class PickSingleEgadP153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P15_3_v2.pkl"


@configclass
class PickSingleEgadP160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P16_0_v2.pkl"


@configclass
class PickSingleEgadP161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P16_1_v2.pkl"


@configclass
class PickSingleEgadP162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P16_2_v2.pkl"


@configclass
class PickSingleEgadP163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P16_3_v2.pkl"


@configclass
class PickSingleEgadP170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P17_0_v2.pkl"


@configclass
class PickSingleEgadP171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P17_1_v2.pkl"


@configclass
class PickSingleEgadP172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P17_2_v2.pkl"


@configclass
class PickSingleEgadP173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P17_3_v2.pkl"


@configclass
class PickSingleEgadP180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P18_0_v2.pkl"


@configclass
class PickSingleEgadP181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P18_1_v2.pkl"


@configclass
class PickSingleEgadP182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P18_2_v2.pkl"


@configclass
class PickSingleEgadP183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P18_3_v2.pkl"


@configclass
class PickSingleEgadP190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P19_0_v2.pkl"


@configclass
class PickSingleEgadP191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P19_1_v2.pkl"


@configclass
class PickSingleEgadP192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P19_2_v2.pkl"


@configclass
class PickSingleEgadP200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P20_0_v2.pkl"


@configclass
class PickSingleEgadP202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P20_2_v2.pkl"


@configclass
class PickSingleEgadP203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P20_3_v2.pkl"


@configclass
class PickSingleEgadP211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P21_1_v2.pkl"


@configclass
class PickSingleEgadP212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P21_2_v2.pkl"


@configclass
class PickSingleEgadP213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P21_3_v2.pkl"


@configclass
class PickSingleEgadP220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P22_0_v2.pkl"


@configclass
class PickSingleEgadP221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P22_1_v2.pkl"


@configclass
class PickSingleEgadP222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P22_2_v2.pkl"


@configclass
class PickSingleEgadP223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P22_3_v2.pkl"


@configclass
class PickSingleEgadP230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P23_0_v2.pkl"


@configclass
class PickSingleEgadP231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P23_1_v2.pkl"


@configclass
class PickSingleEgadP232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P23_2_v2.pkl"


@configclass
class PickSingleEgadP233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P23_3_v2.pkl"


@configclass
class PickSingleEgadP240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P24_0_v2.pkl"


@configclass
class PickSingleEgadP241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P24_1_v2.pkl"


@configclass
class PickSingleEgadP242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P24_2_v2.pkl"


@configclass
class PickSingleEgadP243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P24_3_v2.pkl"


@configclass
class PickSingleEgadP250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P25_0_v2.pkl"


@configclass
class PickSingleEgadP251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P25_1_v2.pkl"


@configclass
class PickSingleEgadP252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P25_2_v2.pkl"


@configclass
class PickSingleEgadP253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/P25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/P25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-P25_3_v2.pkl"


@configclass
class PickSingleEgadQ050MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q05_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q05_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q05_0_v2.pkl"


@configclass
class PickSingleEgadQ051MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q05_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q05_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q05_1_v2.pkl"


@configclass
class PickSingleEgadQ052MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q05_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q05_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q05_2_v2.pkl"


@configclass
class PickSingleEgadQ053MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q05_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q05_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q05_3_v2.pkl"


@configclass
class PickSingleEgadQ062MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q06_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q06_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q06_2_v2.pkl"


@configclass
class PickSingleEgadQ063MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q06_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q06_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q06_3_v2.pkl"


@configclass
class PickSingleEgadQ070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q07_0_v2.pkl"


@configclass
class PickSingleEgadQ072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q07_2_v2.pkl"


@configclass
class PickSingleEgadQ073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q07_3_v2.pkl"


@configclass
class PickSingleEgadQ080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q08_0_v2.pkl"


@configclass
class PickSingleEgadQ081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q08_1_v2.pkl"


@configclass
class PickSingleEgadQ083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q08_3_v2.pkl"


@configclass
class PickSingleEgadQ090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q09_0_v2.pkl"


@configclass
class PickSingleEgadQ091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q09_1_v2.pkl"


@configclass
class PickSingleEgadQ092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q09_2_v2.pkl"


@configclass
class PickSingleEgadQ093MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q09_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q09_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q09_3_v2.pkl"


@configclass
class PickSingleEgadQ100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q10_0_v2.pkl"


@configclass
class PickSingleEgadQ101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q10_1_v2.pkl"


@configclass
class PickSingleEgadQ102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q10_2_v2.pkl"


@configclass
class PickSingleEgadQ103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q10_3_v2.pkl"


@configclass
class PickSingleEgadQ110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q11_0_v2.pkl"


@configclass
class PickSingleEgadQ111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q11_1_v2.pkl"


@configclass
class PickSingleEgadQ112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q11_2_v2.pkl"


@configclass
class PickSingleEgadQ113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q11_3_v2.pkl"


@configclass
class PickSingleEgadQ120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q12_0_v2.pkl"


@configclass
class PickSingleEgadQ122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q12_2_v2.pkl"


@configclass
class PickSingleEgadQ123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q12_3_v2.pkl"


@configclass
class PickSingleEgadQ130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q13_0_v2.pkl"


@configclass
class PickSingleEgadQ131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q13_1_v2.pkl"


@configclass
class PickSingleEgadQ140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q14_0_v2.pkl"


@configclass
class PickSingleEgadQ141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q14_1_v2.pkl"


@configclass
class PickSingleEgadQ142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q14_2_v2.pkl"


@configclass
class PickSingleEgadQ143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q14_3_v2.pkl"


@configclass
class PickSingleEgadQ150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q15_0_v2.pkl"


@configclass
class PickSingleEgadQ151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q15_1_v2.pkl"


@configclass
class PickSingleEgadQ152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q15_2_v2.pkl"


@configclass
class PickSingleEgadQ153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q15_3_v2.pkl"


@configclass
class PickSingleEgadQ160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q16_0_v2.pkl"


@configclass
class PickSingleEgadQ161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q16_1_v2.pkl"


@configclass
class PickSingleEgadQ162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q16_2_v2.pkl"


@configclass
class PickSingleEgadQ163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q16_3_v2.pkl"


@configclass
class PickSingleEgadQ170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q17_0_v2.pkl"


@configclass
class PickSingleEgadQ171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q17_1_v2.pkl"


@configclass
class PickSingleEgadQ180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q18_0_v2.pkl"


@configclass
class PickSingleEgadQ181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q18_1_v2.pkl"


@configclass
class PickSingleEgadQ182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q18_2_v2.pkl"


@configclass
class PickSingleEgadQ183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q18_3_v2.pkl"


@configclass
class PickSingleEgadQ190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q19_0_v2.pkl"


@configclass
class PickSingleEgadQ191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q19_1_v2.pkl"


@configclass
class PickSingleEgadQ192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q19_2_v2.pkl"


@configclass
class PickSingleEgadQ193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q19_3_v2.pkl"


@configclass
class PickSingleEgadQ200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q20_0_v2.pkl"


@configclass
class PickSingleEgadQ202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q20_2_v2.pkl"


@configclass
class PickSingleEgadQ203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q20_3_v2.pkl"


@configclass
class PickSingleEgadQ210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q21_0_v2.pkl"


@configclass
class PickSingleEgadQ211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q21_1_v2.pkl"


@configclass
class PickSingleEgadQ212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q21_2_v2.pkl"


@configclass
class PickSingleEgadQ213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q21_3_v2.pkl"


@configclass
class PickSingleEgadQ220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q22_0_v2.pkl"


@configclass
class PickSingleEgadQ221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q22_1_v2.pkl"


@configclass
class PickSingleEgadQ222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q22_2_v2.pkl"


@configclass
class PickSingleEgadQ223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q22_3_v2.pkl"


@configclass
class PickSingleEgadQ230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q23_0_v2.pkl"


@configclass
class PickSingleEgadQ231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q23_1_v2.pkl"


@configclass
class PickSingleEgadQ232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q23_2_v2.pkl"


@configclass
class PickSingleEgadQ240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q24_0_v2.pkl"


@configclass
class PickSingleEgadQ241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q24_1_v2.pkl"


@configclass
class PickSingleEgadQ242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q24_2_v2.pkl"


@configclass
class PickSingleEgadQ243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q24_3_v2.pkl"


@configclass
class PickSingleEgadQ250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q25_0_v2.pkl"


@configclass
class PickSingleEgadQ251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q25_1_v2.pkl"


@configclass
class PickSingleEgadQ253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/Q25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/Q25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-Q25_3_v2.pkl"


@configclass
class PickSingleEgadR050MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R05_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R05_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R05_0_v2.pkl"


@configclass
class PickSingleEgadR052MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R05_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R05_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R05_2_v2.pkl"


@configclass
class PickSingleEgadR053MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R05_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R05_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R05_3_v2.pkl"


@configclass
class PickSingleEgadR060MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R06_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R06_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R06_0_v2.pkl"


@configclass
class PickSingleEgadR061MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R06_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R06_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R06_1_v2.pkl"


@configclass
class PickSingleEgadR062MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R06_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R06_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R06_2_v2.pkl"


@configclass
class PickSingleEgadR063MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R06_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R06_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R06_3_v2.pkl"


@configclass
class PickSingleEgadR070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R07_0_v2.pkl"


@configclass
class PickSingleEgadR071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R07_1_v2.pkl"


@configclass
class PickSingleEgadR073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R07_3_v2.pkl"


@configclass
class PickSingleEgadR081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R08_1_v2.pkl"


@configclass
class PickSingleEgadR082MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R08_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R08_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R08_2_v2.pkl"


@configclass
class PickSingleEgadR083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R08_3_v2.pkl"


@configclass
class PickSingleEgadR090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R09_0_v2.pkl"


@configclass
class PickSingleEgadR093MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R09_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R09_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R09_3_v2.pkl"


@configclass
class PickSingleEgadR100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R10_0_v2.pkl"


@configclass
class PickSingleEgadR101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R10_1_v2.pkl"


@configclass
class PickSingleEgadR103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R10_3_v2.pkl"


@configclass
class PickSingleEgadR110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R11_0_v2.pkl"


@configclass
class PickSingleEgadR111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R11_1_v2.pkl"


@configclass
class PickSingleEgadR112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R11_2_v2.pkl"


@configclass
class PickSingleEgadR113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R11_3_v2.pkl"


@configclass
class PickSingleEgadR121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R12_1_v2.pkl"


@configclass
class PickSingleEgadR122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R12_2_v2.pkl"


@configclass
class PickSingleEgadR123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R12_3_v2.pkl"


@configclass
class PickSingleEgadR130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R13_0_v2.pkl"


@configclass
class PickSingleEgadR131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R13_1_v2.pkl"


@configclass
class PickSingleEgadR133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R13_3_v2.pkl"


@configclass
class PickSingleEgadR140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R14_0_v2.pkl"


@configclass
class PickSingleEgadR141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R14_1_v2.pkl"


@configclass
class PickSingleEgadR143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R14_3_v2.pkl"


@configclass
class PickSingleEgadR150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R15_0_v2.pkl"


@configclass
class PickSingleEgadR151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R15_1_v2.pkl"


@configclass
class PickSingleEgadR152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R15_2_v2.pkl"


@configclass
class PickSingleEgadR153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R15_3_v2.pkl"


@configclass
class PickSingleEgadR161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R16_1_v2.pkl"


@configclass
class PickSingleEgadR162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R16_2_v2.pkl"


@configclass
class PickSingleEgadR170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R17_0_v2.pkl"


@configclass
class PickSingleEgadR171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R17_1_v2.pkl"


@configclass
class PickSingleEgadR172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R17_2_v2.pkl"


@configclass
class PickSingleEgadR173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R17_3_v2.pkl"


@configclass
class PickSingleEgadR180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R18_0_v2.pkl"


@configclass
class PickSingleEgadR181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R18_1_v2.pkl"


@configclass
class PickSingleEgadR182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R18_2_v2.pkl"


@configclass
class PickSingleEgadR191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R19_1_v2.pkl"


@configclass
class PickSingleEgadR193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R19_3_v2.pkl"


@configclass
class PickSingleEgadR200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R20_0_v2.pkl"


@configclass
class PickSingleEgadR201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R20_1_v2.pkl"


@configclass
class PickSingleEgadR202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R20_2_v2.pkl"


@configclass
class PickSingleEgadR203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R20_3_v2.pkl"


@configclass
class PickSingleEgadR210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R21_0_v2.pkl"


@configclass
class PickSingleEgadR211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R21_1_v2.pkl"


@configclass
class PickSingleEgadR212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R21_2_v2.pkl"


@configclass
class PickSingleEgadR213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R21_3_v2.pkl"


@configclass
class PickSingleEgadR220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R22_0_v2.pkl"


@configclass
class PickSingleEgadR221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R22_1_v2.pkl"


@configclass
class PickSingleEgadR222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R22_2_v2.pkl"


@configclass
class PickSingleEgadR223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R22_3_v2.pkl"


@configclass
class PickSingleEgadR230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R23_0_v2.pkl"


@configclass
class PickSingleEgadR231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R23_1_v2.pkl"


@configclass
class PickSingleEgadR232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R23_2_v2.pkl"


@configclass
class PickSingleEgadR233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R23_3_v2.pkl"


@configclass
class PickSingleEgadR240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R24_0_v2.pkl"


@configclass
class PickSingleEgadR241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R24_1_v2.pkl"


@configclass
class PickSingleEgadR242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R24_2_v2.pkl"


@configclass
class PickSingleEgadR243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R24_3_v2.pkl"


@configclass
class PickSingleEgadR250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R25_0_v2.pkl"


@configclass
class PickSingleEgadR251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R25_1_v2.pkl"


@configclass
class PickSingleEgadR252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R25_2_v2.pkl"


@configclass
class PickSingleEgadR253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/R25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/R25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-R25_3_v2.pkl"


@configclass
class PickSingleEgadS040MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S04_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S04_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S04_0_v2.pkl"


@configclass
class PickSingleEgadS041MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S04_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S04_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S04_1_v2.pkl"


@configclass
class PickSingleEgadS043MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S04_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S04_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S04_3_v2.pkl"


@configclass
class PickSingleEgadS051MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S05_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S05_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S05_1_v2.pkl"


@configclass
class PickSingleEgadS052MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S05_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S05_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S05_2_v2.pkl"


@configclass
class PickSingleEgadS053MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S05_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S05_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S05_3_v2.pkl"


@configclass
class PickSingleEgadS060MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S06_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S06_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S06_0_v2.pkl"


@configclass
class PickSingleEgadS061MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S06_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S06_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S06_1_v2.pkl"


@configclass
class PickSingleEgadS062MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S06_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S06_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S06_2_v2.pkl"


@configclass
class PickSingleEgadS070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S07_0_v2.pkl"


@configclass
class PickSingleEgadS071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S07_1_v2.pkl"


@configclass
class PickSingleEgadS072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S07_2_v2.pkl"


@configclass
class PickSingleEgadS080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S08_0_v2.pkl"


@configclass
class PickSingleEgadS081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S08_1_v2.pkl"


@configclass
class PickSingleEgadS082MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S08_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S08_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S08_2_v2.pkl"


@configclass
class PickSingleEgadS091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S09_1_v2.pkl"


@configclass
class PickSingleEgadS092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S09_2_v2.pkl"


@configclass
class PickSingleEgadS101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S10_1_v2.pkl"


@configclass
class PickSingleEgadS102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S10_2_v2.pkl"


@configclass
class PickSingleEgadS103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S10_3_v2.pkl"


@configclass
class PickSingleEgadS110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S11_0_v2.pkl"


@configclass
class PickSingleEgadS111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S11_1_v2.pkl"


@configclass
class PickSingleEgadS113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S11_3_v2.pkl"


@configclass
class PickSingleEgadS120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S12_0_v2.pkl"


@configclass
class PickSingleEgadS121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S12_1_v2.pkl"


@configclass
class PickSingleEgadS122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S12_2_v2.pkl"


@configclass
class PickSingleEgadS123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S12_3_v2.pkl"


@configclass
class PickSingleEgadS130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S13_0_v2.pkl"


@configclass
class PickSingleEgadS131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S13_1_v2.pkl"


@configclass
class PickSingleEgadS132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S13_2_v2.pkl"


@configclass
class PickSingleEgadS133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S13_3_v2.pkl"


@configclass
class PickSingleEgadS140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S14_0_v2.pkl"


@configclass
class PickSingleEgadS141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S14_1_v2.pkl"


@configclass
class PickSingleEgadS142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S14_2_v2.pkl"


@configclass
class PickSingleEgadS150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S15_0_v2.pkl"


@configclass
class PickSingleEgadS151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S15_1_v2.pkl"


@configclass
class PickSingleEgadS153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S15_3_v2.pkl"


@configclass
class PickSingleEgadS160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S16_0_v2.pkl"


@configclass
class PickSingleEgadS161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S16_1_v2.pkl"


@configclass
class PickSingleEgadS163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S16_3_v2.pkl"


@configclass
class PickSingleEgadS170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S17_0_v2.pkl"


@configclass
class PickSingleEgadS171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S17_1_v2.pkl"


@configclass
class PickSingleEgadS172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S17_2_v2.pkl"


@configclass
class PickSingleEgadS180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S18_0_v2.pkl"


@configclass
class PickSingleEgadS181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S18_1_v2.pkl"


@configclass
class PickSingleEgadS183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S18_3_v2.pkl"


@configclass
class PickSingleEgadS190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S19_0_v2.pkl"


@configclass
class PickSingleEgadS191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S19_1_v2.pkl"


@configclass
class PickSingleEgadS192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S19_2_v2.pkl"


@configclass
class PickSingleEgadS193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S19_3_v2.pkl"


@configclass
class PickSingleEgadS200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S20_0_v2.pkl"


@configclass
class PickSingleEgadS201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S20_1_v2.pkl"


@configclass
class PickSingleEgadS202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S20_2_v2.pkl"


@configclass
class PickSingleEgadS203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S20_3_v2.pkl"


@configclass
class PickSingleEgadS210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S21_0_v2.pkl"


@configclass
class PickSingleEgadS211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S21_1_v2.pkl"


@configclass
class PickSingleEgadS212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S21_2_v2.pkl"


@configclass
class PickSingleEgadS213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S21_3_v2.pkl"


@configclass
class PickSingleEgadS220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S22_0_v2.pkl"


@configclass
class PickSingleEgadS221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S22_1_v2.pkl"


@configclass
class PickSingleEgadS222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S22_2_v2.pkl"


@configclass
class PickSingleEgadS223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S22_3_v2.pkl"


@configclass
class PickSingleEgadS230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S23_0_v2.pkl"


@configclass
class PickSingleEgadS231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S23_1_v2.pkl"


@configclass
class PickSingleEgadS232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S23_2_v2.pkl"


@configclass
class PickSingleEgadS233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S23_3_v2.pkl"


@configclass
class PickSingleEgadS240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S24_0_v2.pkl"


@configclass
class PickSingleEgadS241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S24_1_v2.pkl"


@configclass
class PickSingleEgadS242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S24_2_v2.pkl"


@configclass
class PickSingleEgadS243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S24_3_v2.pkl"


@configclass
class PickSingleEgadS250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S25_0_v2.pkl"


@configclass
class PickSingleEgadS251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S25_1_v2.pkl"


@configclass
class PickSingleEgadS252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S25_2_v2.pkl"


@configclass
class PickSingleEgadS253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/S25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/S25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-S25_3_v2.pkl"


@configclass
class PickSingleEgadT041MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T04_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T04_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T04_1_v2.pkl"


@configclass
class PickSingleEgadT043MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T04_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T04_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T04_3_v2.pkl"


@configclass
class PickSingleEgadT050MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T05_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T05_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T05_0_v2.pkl"


@configclass
class PickSingleEgadT051MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T05_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T05_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T05_1_v2.pkl"


@configclass
class PickSingleEgadT052MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T05_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T05_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T05_2_v2.pkl"


@configclass
class PickSingleEgadT053MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T05_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T05_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T05_3_v2.pkl"


@configclass
class PickSingleEgadT060MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T06_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T06_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T06_0_v2.pkl"


@configclass
class PickSingleEgadT061MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T06_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T06_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T06_1_v2.pkl"


@configclass
class PickSingleEgadT062MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T06_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T06_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T06_2_v2.pkl"


@configclass
class PickSingleEgadT063MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T06_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T06_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T06_3_v2.pkl"


@configclass
class PickSingleEgadT070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T07_0_v2.pkl"


@configclass
class PickSingleEgadT071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T07_1_v2.pkl"


@configclass
class PickSingleEgadT072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T07_2_v2.pkl"


@configclass
class PickSingleEgadT073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T07_3_v2.pkl"


@configclass
class PickSingleEgadT080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T08_0_v2.pkl"


@configclass
class PickSingleEgadT081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T08_1_v2.pkl"


@configclass
class PickSingleEgadT082MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T08_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T08_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T08_2_v2.pkl"


@configclass
class PickSingleEgadT083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T08_3_v2.pkl"


@configclass
class PickSingleEgadT090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T09_0_v2.pkl"


@configclass
class PickSingleEgadT091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T09_1_v2.pkl"


@configclass
class PickSingleEgadT100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T10_0_v2.pkl"


@configclass
class PickSingleEgadT102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T10_2_v2.pkl"


@configclass
class PickSingleEgadT103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T10_3_v2.pkl"


@configclass
class PickSingleEgadT110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T11_0_v2.pkl"


@configclass
class PickSingleEgadT111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T11_1_v2.pkl"


@configclass
class PickSingleEgadT112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T11_2_v2.pkl"


@configclass
class PickSingleEgadT120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T12_0_v2.pkl"


@configclass
class PickSingleEgadT121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T12_1_v2.pkl"


@configclass
class PickSingleEgadT122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T12_2_v2.pkl"


@configclass
class PickSingleEgadT123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T12_3_v2.pkl"


@configclass
class PickSingleEgadT130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T13_0_v2.pkl"


@configclass
class PickSingleEgadT131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T13_1_v2.pkl"


@configclass
class PickSingleEgadT132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T13_2_v2.pkl"


@configclass
class PickSingleEgadT140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T14_0_v2.pkl"


@configclass
class PickSingleEgadT141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T14_1_v2.pkl"


@configclass
class PickSingleEgadT143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T14_3_v2.pkl"


@configclass
class PickSingleEgadT151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T15_1_v2.pkl"


@configclass
class PickSingleEgadT152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T15_2_v2.pkl"


@configclass
class PickSingleEgadT153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T15_3_v2.pkl"


@configclass
class PickSingleEgadT160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T16_0_v2.pkl"


@configclass
class PickSingleEgadT161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T16_1_v2.pkl"


@configclass
class PickSingleEgadT163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T16_3_v2.pkl"


@configclass
class PickSingleEgadT171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T17_1_v2.pkl"


@configclass
class PickSingleEgadT172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T17_2_v2.pkl"


@configclass
class PickSingleEgadT173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T17_3_v2.pkl"


@configclass
class PickSingleEgadT180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T18_0_v2.pkl"


@configclass
class PickSingleEgadT181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T18_1_v2.pkl"


@configclass
class PickSingleEgadT182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T18_2_v2.pkl"


@configclass
class PickSingleEgadT183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T18_3_v2.pkl"


@configclass
class PickSingleEgadT190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T19_0_v2.pkl"


@configclass
class PickSingleEgadT191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T19_1_v2.pkl"


@configclass
class PickSingleEgadT192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T19_2_v2.pkl"


@configclass
class PickSingleEgadT193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T19_3_v2.pkl"


@configclass
class PickSingleEgadT200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T20_0_v2.pkl"


@configclass
class PickSingleEgadT201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T20_1_v2.pkl"


@configclass
class PickSingleEgadT202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T20_2_v2.pkl"


@configclass
class PickSingleEgadT203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T20_3_v2.pkl"


@configclass
class PickSingleEgadT210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T21_0_v2.pkl"


@configclass
class PickSingleEgadT211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T21_1_v2.pkl"


@configclass
class PickSingleEgadT212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T21_2_v2.pkl"


@configclass
class PickSingleEgadT213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T21_3_v2.pkl"


@configclass
class PickSingleEgadT220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T22_0_v2.pkl"


@configclass
class PickSingleEgadT221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T22_1_v2.pkl"


@configclass
class PickSingleEgadT222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T22_2_v2.pkl"


@configclass
class PickSingleEgadT223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T22_3_v2.pkl"


@configclass
class PickSingleEgadT230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T23_0_v2.pkl"


@configclass
class PickSingleEgadT231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T23_1_v2.pkl"


@configclass
class PickSingleEgadT232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T23_2_v2.pkl"


@configclass
class PickSingleEgadT233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T23_3_v2.pkl"


@configclass
class PickSingleEgadT240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T24_0_v2.pkl"


@configclass
class PickSingleEgadT241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T24_1_v2.pkl"


@configclass
class PickSingleEgadT242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T24_2_v2.pkl"


@configclass
class PickSingleEgadT243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T24_3_v2.pkl"


@configclass
class PickSingleEgadT251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T25_1_v2.pkl"


@configclass
class PickSingleEgadT252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T25_2_v2.pkl"


@configclass
class PickSingleEgadT253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/T25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/T25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-T25_3_v2.pkl"


@configclass
class PickSingleEgadU020MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U02_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U02_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U02_0_v2.pkl"


@configclass
class PickSingleEgadU023MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U02_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U02_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U02_3_v2.pkl"


@configclass
class PickSingleEgadU030MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U03_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U03_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U03_0_v2.pkl"


@configclass
class PickSingleEgadU031MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U03_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U03_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U03_1_v2.pkl"


@configclass
class PickSingleEgadU033MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U03_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U03_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U03_3_v2.pkl"


@configclass
class PickSingleEgadU040MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U04_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U04_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U04_0_v2.pkl"


@configclass
class PickSingleEgadU043MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U04_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U04_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U04_3_v2.pkl"


@configclass
class PickSingleEgadU050MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U05_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U05_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U05_0_v2.pkl"


@configclass
class PickSingleEgadU052MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U05_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U05_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U05_2_v2.pkl"


@configclass
class PickSingleEgadU060MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U06_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U06_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U06_0_v2.pkl"


@configclass
class PickSingleEgadU061MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U06_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U06_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U06_1_v2.pkl"


@configclass
class PickSingleEgadU063MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U06_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U06_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U06_3_v2.pkl"


@configclass
class PickSingleEgadU070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U07_0_v2.pkl"


@configclass
class PickSingleEgadU081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U08_1_v2.pkl"


@configclass
class PickSingleEgadU083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U08_3_v2.pkl"


@configclass
class PickSingleEgadU090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U09_0_v2.pkl"


@configclass
class PickSingleEgadU093MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U09_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U09_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U09_3_v2.pkl"


@configclass
class PickSingleEgadU100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U10_0_v2.pkl"


@configclass
class PickSingleEgadU101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U10_1_v2.pkl"


@configclass
class PickSingleEgadU103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U10_3_v2.pkl"


@configclass
class PickSingleEgadU111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U11_1_v2.pkl"


@configclass
class PickSingleEgadU112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U11_2_v2.pkl"


@configclass
class PickSingleEgadU113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U11_3_v2.pkl"


@configclass
class PickSingleEgadU122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U12_2_v2.pkl"


@configclass
class PickSingleEgadU123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U12_3_v2.pkl"


@configclass
class PickSingleEgadU130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U13_0_v2.pkl"


@configclass
class PickSingleEgadU131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U13_1_v2.pkl"


@configclass
class PickSingleEgadU132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U13_2_v2.pkl"


@configclass
class PickSingleEgadU140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U14_0_v2.pkl"


@configclass
class PickSingleEgadU141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U14_1_v2.pkl"


@configclass
class PickSingleEgadU143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U14_3_v2.pkl"


@configclass
class PickSingleEgadU150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U15_0_v2.pkl"


@configclass
class PickSingleEgadU151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U15_1_v2.pkl"


@configclass
class PickSingleEgadU152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U15_2_v2.pkl"


@configclass
class PickSingleEgadU160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U16_0_v2.pkl"


@configclass
class PickSingleEgadU161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U16_1_v2.pkl"


@configclass
class PickSingleEgadU162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U16_2_v2.pkl"


@configclass
class PickSingleEgadU163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U16_3_v2.pkl"


@configclass
class PickSingleEgadU170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U17_0_v2.pkl"


@configclass
class PickSingleEgadU171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U17_1_v2.pkl"


@configclass
class PickSingleEgadU172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U17_2_v2.pkl"


@configclass
class PickSingleEgadU173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U17_3_v2.pkl"


@configclass
class PickSingleEgadU181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U18_1_v2.pkl"


@configclass
class PickSingleEgadU182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U18_2_v2.pkl"


@configclass
class PickSingleEgadU183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U18_3_v2.pkl"


@configclass
class PickSingleEgadU190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U19_0_v2.pkl"


@configclass
class PickSingleEgadU191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U19_1_v2.pkl"


@configclass
class PickSingleEgadU192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U19_2_v2.pkl"


@configclass
class PickSingleEgadU193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U19_3_v2.pkl"


@configclass
class PickSingleEgadU200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U20_0_v2.pkl"


@configclass
class PickSingleEgadU201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U20_1_v2.pkl"


@configclass
class PickSingleEgadU202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U20_2_v2.pkl"


@configclass
class PickSingleEgadU203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U20_3_v2.pkl"


@configclass
class PickSingleEgadU210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U21_0_v2.pkl"


@configclass
class PickSingleEgadU211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U21_1_v2.pkl"


@configclass
class PickSingleEgadU212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U21_2_v2.pkl"


@configclass
class PickSingleEgadU213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U21_3_v2.pkl"


@configclass
class PickSingleEgadU221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U22_1_v2.pkl"


@configclass
class PickSingleEgadU222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U22_2_v2.pkl"


@configclass
class PickSingleEgadU230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U23_0_v2.pkl"


@configclass
class PickSingleEgadU231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U23_1_v2.pkl"


@configclass
class PickSingleEgadU233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U23_3_v2.pkl"


@configclass
class PickSingleEgadU241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U24_1_v2.pkl"


@configclass
class PickSingleEgadU242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U24_2_v2.pkl"


@configclass
class PickSingleEgadU243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U24_3_v2.pkl"


@configclass
class PickSingleEgadU250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U25_0_v2.pkl"


@configclass
class PickSingleEgadU251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U25_1_v2.pkl"


@configclass
class PickSingleEgadU252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/U25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/U25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-U25_2_v2.pkl"


@configclass
class PickSingleEgadV020MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V02_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V02_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V02_0_v2.pkl"


@configclass
class PickSingleEgadV021MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V02_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V02_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V02_1_v2.pkl"


@configclass
class PickSingleEgadV022MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V02_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V02_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V02_2_v2.pkl"


@configclass
class PickSingleEgadV023MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V02_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V02_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V02_3_v2.pkl"


@configclass
class PickSingleEgadV031MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V03_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V03_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V03_1_v2.pkl"


@configclass
class PickSingleEgadV033MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V03_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V03_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V03_3_v2.pkl"


@configclass
class PickSingleEgadV041MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V04_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V04_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V04_1_v2.pkl"


@configclass
class PickSingleEgadV042MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V04_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V04_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V04_2_v2.pkl"


@configclass
class PickSingleEgadV050MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V05_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V05_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V05_0_v2.pkl"


@configclass
class PickSingleEgadV052MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V05_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V05_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V05_2_v2.pkl"


@configclass
class PickSingleEgadV053MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V05_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V05_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V05_3_v2.pkl"


@configclass
class PickSingleEgadV060MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V06_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V06_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V06_0_v2.pkl"


@configclass
class PickSingleEgadV061MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V06_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V06_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V06_1_v2.pkl"


@configclass
class PickSingleEgadV063MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V06_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V06_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V06_3_v2.pkl"


@configclass
class PickSingleEgadV070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V07_0_v2.pkl"


@configclass
class PickSingleEgadV072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V07_2_v2.pkl"


@configclass
class PickSingleEgadV073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V07_3_v2.pkl"


@configclass
class PickSingleEgadV080MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V08_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V08_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V08_0_v2.pkl"


@configclass
class PickSingleEgadV082MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V08_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V08_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V08_2_v2.pkl"


@configclass
class PickSingleEgadV092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V09_2_v2.pkl"


@configclass
class PickSingleEgadV100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V10_0_v2.pkl"


@configclass
class PickSingleEgadV101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V10_1_v2.pkl"


@configclass
class PickSingleEgadV102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V10_2_v2.pkl"


@configclass
class PickSingleEgadV103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V10_3_v2.pkl"


@configclass
class PickSingleEgadV110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V11_0_v2.pkl"


@configclass
class PickSingleEgadV111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V11_1_v2.pkl"


@configclass
class PickSingleEgadV112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V11_2_v2.pkl"


@configclass
class PickSingleEgadV113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V11_3_v2.pkl"


@configclass
class PickSingleEgadV121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V12_1_v2.pkl"


@configclass
class PickSingleEgadV122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V12_2_v2.pkl"


@configclass
class PickSingleEgadV123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V12_3_v2.pkl"


@configclass
class PickSingleEgadV130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V13_0_v2.pkl"


@configclass
class PickSingleEgadV131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V13_1_v2.pkl"


@configclass
class PickSingleEgadV132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V13_2_v2.pkl"


@configclass
class PickSingleEgadV133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V13_3_v2.pkl"


@configclass
class PickSingleEgadV140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V14_0_v2.pkl"


@configclass
class PickSingleEgadV141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V14_1_v2.pkl"


@configclass
class PickSingleEgadV150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V15_0_v2.pkl"


@configclass
class PickSingleEgadV151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V15_1_v2.pkl"


@configclass
class PickSingleEgadV153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V15_3_v2.pkl"


@configclass
class PickSingleEgadV160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V16_0_v2.pkl"


@configclass
class PickSingleEgadV162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V16_2_v2.pkl"


@configclass
class PickSingleEgadV171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V17_1_v2.pkl"


@configclass
class PickSingleEgadV172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V17_2_v2.pkl"


@configclass
class PickSingleEgadV173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V17_3_v2.pkl"


@configclass
class PickSingleEgadV181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V18_1_v2.pkl"


@configclass
class PickSingleEgadV182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V18_2_v2.pkl"


@configclass
class PickSingleEgadV190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V19_0_v2.pkl"


@configclass
class PickSingleEgadV191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V19_1_v2.pkl"


@configclass
class PickSingleEgadV192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V19_2_v2.pkl"


@configclass
class PickSingleEgadV193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V19_3_v2.pkl"


@configclass
class PickSingleEgadV200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V20_0_v2.pkl"


@configclass
class PickSingleEgadV201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V20_1_v2.pkl"


@configclass
class PickSingleEgadV202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V20_2_v2.pkl"


@configclass
class PickSingleEgadV203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V20_3_v2.pkl"


@configclass
class PickSingleEgadV210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V21_0_v2.pkl"


@configclass
class PickSingleEgadV211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V21_1_v2.pkl"


@configclass
class PickSingleEgadV213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V21_3_v2.pkl"


@configclass
class PickSingleEgadV221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V22_1_v2.pkl"


@configclass
class PickSingleEgadV222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V22_2_v2.pkl"


@configclass
class PickSingleEgadV223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V22_3_v2.pkl"


@configclass
class PickSingleEgadV230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V23_0_v2.pkl"


@configclass
class PickSingleEgadV232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V23_2_v2.pkl"


@configclass
class PickSingleEgadV233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V23_3_v2.pkl"


@configclass
class PickSingleEgadV240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V24_0_v2.pkl"


@configclass
class PickSingleEgadV241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V24_1_v2.pkl"


@configclass
class PickSingleEgadV242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V24_2_v2.pkl"


@configclass
class PickSingleEgadV250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V25_0_v2.pkl"


@configclass
class PickSingleEgadV251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V25_1_v2.pkl"


@configclass
class PickSingleEgadV252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V25_2_v2.pkl"


@configclass
class PickSingleEgadV253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/V25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/V25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-V25_3_v2.pkl"


@configclass
class PickSingleEgadW020MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W02_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W02_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W02_0_v2.pkl"


@configclass
class PickSingleEgadW030MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W03_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W03_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W03_0_v2.pkl"


@configclass
class PickSingleEgadW033MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W03_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W03_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W03_3_v2.pkl"


@configclass
class PickSingleEgadW040MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W04_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W04_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W04_0_v2.pkl"


@configclass
class PickSingleEgadW041MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W04_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W04_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W04_1_v2.pkl"


@configclass
class PickSingleEgadW042MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W04_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W04_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W04_2_v2.pkl"


@configclass
class PickSingleEgadW050MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W05_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W05_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W05_0_v2.pkl"


@configclass
class PickSingleEgadW052MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W05_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W05_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W05_2_v2.pkl"


@configclass
class PickSingleEgadW053MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W05_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W05_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W05_3_v2.pkl"


@configclass
class PickSingleEgadW060MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W06_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W06_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W06_0_v2.pkl"


@configclass
class PickSingleEgadW062MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W06_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W06_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W06_2_v2.pkl"


@configclass
class PickSingleEgadW063MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W06_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W06_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W06_3_v2.pkl"


@configclass
class PickSingleEgadW070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W07_0_v2.pkl"


@configclass
class PickSingleEgadW071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W07_1_v2.pkl"


@configclass
class PickSingleEgadW073MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W07_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W07_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W07_3_v2.pkl"


@configclass
class PickSingleEgadW081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W08_1_v2.pkl"


@configclass
class PickSingleEgadW082MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W08_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W08_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W08_2_v2.pkl"


@configclass
class PickSingleEgadW083MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W08_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W08_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W08_3_v2.pkl"


@configclass
class PickSingleEgadW090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W09_0_v2.pkl"


@configclass
class PickSingleEgadW091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W09_1_v2.pkl"


@configclass
class PickSingleEgadW092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W09_2_v2.pkl"


@configclass
class PickSingleEgadW093MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W09_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W09_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W09_3_v2.pkl"


@configclass
class PickSingleEgadW101MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W10_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W10_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W10_1_v2.pkl"


@configclass
class PickSingleEgadW110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W11_0_v2.pkl"


@configclass
class PickSingleEgadW111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W11_1_v2.pkl"


@configclass
class PickSingleEgadW113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W11_3_v2.pkl"


@configclass
class PickSingleEgadW121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W12_1_v2.pkl"


@configclass
class PickSingleEgadW122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W12_2_v2.pkl"


@configclass
class PickSingleEgadW123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W12_3_v2.pkl"


@configclass
class PickSingleEgadW130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W13_0_v2.pkl"


@configclass
class PickSingleEgadW131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W13_1_v2.pkl"


@configclass
class PickSingleEgadW132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W13_2_v2.pkl"


@configclass
class PickSingleEgadW133MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W13_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W13_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W13_3_v2.pkl"


@configclass
class PickSingleEgadW140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W14_0_v2.pkl"


@configclass
class PickSingleEgadW143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W14_3_v2.pkl"


@configclass
class PickSingleEgadW150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W15_0_v2.pkl"


@configclass
class PickSingleEgadW151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W15_1_v2.pkl"


@configclass
class PickSingleEgadW153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W15_3_v2.pkl"


@configclass
class PickSingleEgadW160MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W16_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W16_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W16_0_v2.pkl"


@configclass
class PickSingleEgadW161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W16_1_v2.pkl"


@configclass
class PickSingleEgadW162MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W16_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W16_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W16_2_v2.pkl"


@configclass
class PickSingleEgadW163MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W16_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W16_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W16_3_v2.pkl"


@configclass
class PickSingleEgadW170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W17_0_v2.pkl"


@configclass
class PickSingleEgadW171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W17_1_v2.pkl"


@configclass
class PickSingleEgadW172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W17_2_v2.pkl"


@configclass
class PickSingleEgadW173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W17_3_v2.pkl"


@configclass
class PickSingleEgadW180MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W18_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W18_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W18_0_v2.pkl"


@configclass
class PickSingleEgadW182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W18_2_v2.pkl"


@configclass
class PickSingleEgadW183MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W18_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W18_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W18_3_v2.pkl"


@configclass
class PickSingleEgadW190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W19_0_v2.pkl"


@configclass
class PickSingleEgadW192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W19_2_v2.pkl"


@configclass
class PickSingleEgadW193MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W19_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W19_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W19_3_v2.pkl"


@configclass
class PickSingleEgadW200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W20_0_v2.pkl"


@configclass
class PickSingleEgadW201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W20_1_v2.pkl"


@configclass
class PickSingleEgadW202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W20_2_v2.pkl"


@configclass
class PickSingleEgadW203MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W20_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W20_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W20_3_v2.pkl"


@configclass
class PickSingleEgadW210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W21_0_v2.pkl"


@configclass
class PickSingleEgadW211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W21_1_v2.pkl"


@configclass
class PickSingleEgadW220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W22_0_v2.pkl"


@configclass
class PickSingleEgadW221MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W22_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W22_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W22_1_v2.pkl"


@configclass
class PickSingleEgadW223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W22_3_v2.pkl"


@configclass
class PickSingleEgadW230MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W23_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W23_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W23_0_v2.pkl"


@configclass
class PickSingleEgadW231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W23_1_v2.pkl"


@configclass
class PickSingleEgadW232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W23_2_v2.pkl"


@configclass
class PickSingleEgadW233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W23_3_v2.pkl"


@configclass
class PickSingleEgadW240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W24_0_v2.pkl"


@configclass
class PickSingleEgadW241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W24_1_v2.pkl"


@configclass
class PickSingleEgadW242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W24_2_v2.pkl"


@configclass
class PickSingleEgadW243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W24_3_v2.pkl"


@configclass
class PickSingleEgadW250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W25_0_v2.pkl"


@configclass
class PickSingleEgadW251MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W25_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W25_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W25_1_v2.pkl"


@configclass
class PickSingleEgadW252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W25_2_v2.pkl"


@configclass
class PickSingleEgadW253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/W25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/W25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-W25_3_v2.pkl"


@configclass
class PickSingleEgadX000MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X00_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X00_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X00_0_v2.pkl"


@configclass
class PickSingleEgadX010MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X01_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X01_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X01_0_v2.pkl"


@configclass
class PickSingleEgadX011MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X01_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X01_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X01_1_v2.pkl"


@configclass
class PickSingleEgadX012MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X01_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X01_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X01_2_v2.pkl"


@configclass
class PickSingleEgadX013MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X01_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X01_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X01_3_v2.pkl"


@configclass
class PickSingleEgadX020MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X02_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X02_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X02_0_v2.pkl"


@configclass
class PickSingleEgadX021MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X02_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X02_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X02_1_v2.pkl"


@configclass
class PickSingleEgadX022MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X02_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X02_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X02_2_v2.pkl"


@configclass
class PickSingleEgadX023MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X02_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X02_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X02_3_v2.pkl"


@configclass
class PickSingleEgadX030MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X03_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X03_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X03_0_v2.pkl"


@configclass
class PickSingleEgadX032MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X03_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X03_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X03_2_v2.pkl"


@configclass
class PickSingleEgadX033MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X03_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X03_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X03_3_v2.pkl"


@configclass
class PickSingleEgadX040MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X04_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X04_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X04_0_v2.pkl"


@configclass
class PickSingleEgadX041MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X04_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X04_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X04_1_v2.pkl"


@configclass
class PickSingleEgadX042MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X04_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X04_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X04_2_v2.pkl"


@configclass
class PickSingleEgadX050MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X05_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X05_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X05_0_v2.pkl"


@configclass
class PickSingleEgadX052MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X05_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X05_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X05_2_v2.pkl"


@configclass
class PickSingleEgadX060MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X06_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X06_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X06_0_v2.pkl"


@configclass
class PickSingleEgadX063MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X06_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X06_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X06_3_v2.pkl"


@configclass
class PickSingleEgadX070MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X07_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X07_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X07_0_v2.pkl"


@configclass
class PickSingleEgadX071MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X07_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X07_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X07_1_v2.pkl"


@configclass
class PickSingleEgadX072MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X07_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X07_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X07_2_v2.pkl"


@configclass
class PickSingleEgadX081MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X08_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X08_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X08_1_v2.pkl"


@configclass
class PickSingleEgadX082MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X08_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X08_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X08_2_v2.pkl"


@configclass
class PickSingleEgadX090MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X09_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X09_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X09_0_v2.pkl"


@configclass
class PickSingleEgadX091MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X09_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X09_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X09_1_v2.pkl"


@configclass
class PickSingleEgadX092MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X09_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X09_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X09_2_v2.pkl"


@configclass
class PickSingleEgadX093MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X09_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X09_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X09_3_v2.pkl"


@configclass
class PickSingleEgadX100MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X10_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X10_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X10_0_v2.pkl"


@configclass
class PickSingleEgadX102MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X10_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X10_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X10_2_v2.pkl"


@configclass
class PickSingleEgadX103MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X10_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X10_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X10_3_v2.pkl"


@configclass
class PickSingleEgadX110MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X11_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X11_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X11_0_v2.pkl"


@configclass
class PickSingleEgadX111MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X11_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X11_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X11_1_v2.pkl"


@configclass
class PickSingleEgadX112MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X11_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X11_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X11_2_v2.pkl"


@configclass
class PickSingleEgadX113MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X11_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X11_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X11_3_v2.pkl"


@configclass
class PickSingleEgadX120MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X12_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X12_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X12_0_v2.pkl"


@configclass
class PickSingleEgadX121MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X12_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X12_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X12_1_v2.pkl"


@configclass
class PickSingleEgadX122MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X12_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X12_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X12_2_v2.pkl"


@configclass
class PickSingleEgadX123MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X12_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X12_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X12_3_v2.pkl"


@configclass
class PickSingleEgadX130MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X13_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X13_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X13_0_v2.pkl"


@configclass
class PickSingleEgadX131MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X13_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X13_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X13_1_v2.pkl"


@configclass
class PickSingleEgadX132MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X13_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X13_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X13_2_v2.pkl"


@configclass
class PickSingleEgadX140MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X14_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X14_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X14_0_v2.pkl"


@configclass
class PickSingleEgadX141MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X14_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X14_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X14_1_v2.pkl"


@configclass
class PickSingleEgadX142MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X14_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X14_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X14_2_v2.pkl"


@configclass
class PickSingleEgadX143MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X14_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X14_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X14_3_v2.pkl"


@configclass
class PickSingleEgadX150MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X15_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X15_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X15_0_v2.pkl"


@configclass
class PickSingleEgadX151MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X15_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X15_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X15_1_v2.pkl"


@configclass
class PickSingleEgadX152MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X15_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X15_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X15_2_v2.pkl"


@configclass
class PickSingleEgadX153MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X15_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X15_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X15_3_v2.pkl"


@configclass
class PickSingleEgadX161MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X16_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X16_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X16_1_v2.pkl"


@configclass
class PickSingleEgadX170MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X17_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X17_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X17_0_v2.pkl"


@configclass
class PickSingleEgadX171MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X17_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X17_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X17_1_v2.pkl"


@configclass
class PickSingleEgadX172MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X17_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X17_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X17_2_v2.pkl"


@configclass
class PickSingleEgadX173MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X17_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X17_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X17_3_v2.pkl"


@configclass
class PickSingleEgadX181MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X18_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X18_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X18_1_v2.pkl"


@configclass
class PickSingleEgadX182MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X18_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X18_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X18_2_v2.pkl"


@configclass
class PickSingleEgadX190MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X19_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X19_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X19_0_v2.pkl"


@configclass
class PickSingleEgadX191MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X19_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X19_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X19_1_v2.pkl"


@configclass
class PickSingleEgadX192MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X19_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X19_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X19_2_v2.pkl"


@configclass
class PickSingleEgadX200MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X20_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X20_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X20_0_v2.pkl"


@configclass
class PickSingleEgadX201MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X20_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X20_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X20_1_v2.pkl"


@configclass
class PickSingleEgadX202MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X20_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X20_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X20_2_v2.pkl"


@configclass
class PickSingleEgadX210MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X21_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X21_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X21_0_v2.pkl"


@configclass
class PickSingleEgadX211MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X21_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X21_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X21_1_v2.pkl"


@configclass
class PickSingleEgadX212MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X21_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X21_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X21_2_v2.pkl"


@configclass
class PickSingleEgadX213MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X21_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X21_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X21_3_v2.pkl"


@configclass
class PickSingleEgadX220MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X22_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X22_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X22_0_v2.pkl"


@configclass
class PickSingleEgadX222MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X22_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X22_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X22_2_v2.pkl"


@configclass
class PickSingleEgadX223MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X22_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X22_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X22_3_v2.pkl"


@configclass
class PickSingleEgadX231MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X23_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X23_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X23_1_v2.pkl"


@configclass
class PickSingleEgadX232MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X23_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X23_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X23_2_v2.pkl"


@configclass
class PickSingleEgadX233MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X23_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X23_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X23_3_v2.pkl"


@configclass
class PickSingleEgadX240MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X24_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X24_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X24_0_v2.pkl"


@configclass
class PickSingleEgadX241MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X24_1_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X24_1.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X24_1_v2.pkl"


@configclass
class PickSingleEgadX242MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X24_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X24_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X24_2_v2.pkl"


@configclass
class PickSingleEgadX243MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X24_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X24_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X24_3_v2.pkl"


@configclass
class PickSingleEgadX250MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X25_0_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X25_0.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X25_0_v2.pkl"


@configclass
class PickSingleEgadX252MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X25_2_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X25_2.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X25_2_v2.pkl"


@configclass
class PickSingleEgadX253MetaCfg(_PickSingleEgadBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/egad/usd/X25_3_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/egad/urdf/X25_3.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_egad/trajectory-franka-X25_3_v2.pkl"
