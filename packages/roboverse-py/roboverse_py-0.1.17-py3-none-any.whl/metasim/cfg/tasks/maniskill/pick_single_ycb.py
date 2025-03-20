from metasim.cfg.checkers import PositionShiftChecker
from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .maniskill_task_metacfg import ManiskillTaskMetaCfg


@configclass
class _PickSingleYcbBaseMetaCfg(ManiskillTaskMetaCfg):
    """ManiSkill pick_single_ycb task, migrated from https://github.com/haosulab/ManiSkill/blob/main/mani_skill/envs/tasks/tabletop/pick_single_ycb.py"""

    episode_length = 250
    checker = PositionShiftChecker(
        obj_name="obj",
        distance=0.075,
        axis="z",
    )


@configclass
class PickSingleYcbLegoDuploMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/073-g_lego_duplo/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/073-g_lego_duplo/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-073-g_lego_duplo_v2.pkl"


@configclass
class PickSingleYcbWoodBlockMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/036_wood_block/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/036_wood_block/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-036_wood_block_v2.pkl"


@configclass
class PickSingleYcbFlatScrewdriverMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/044_flat_screwdriver/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/044_flat_screwdriver/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-044_flat_screwdriver_v2.pkl"


@configclass
class PickSingleYcbExtraLargeClampMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/052_extra_large_clamp/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/052_extra_large_clamp/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-052_extra_large_clamp_v2.pkl"


@configclass
class PickSingleYcbForkMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/030_fork/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/030_fork/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-030_fork_v2.pkl"


@configclass
class PickSingleYcbCupsMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/065-j_cups/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/065-j_cups/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-065-j_cups_v2.pkl"


@configclass
class PickSingleYcbPowerDrillMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/035_power_drill/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/035_power_drill/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-035_power_drill_v2.pkl"


@configclass
class PickSingleYcbBananaMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/011_banana/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/011_banana/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-011_banana_v2.pkl"


@configclass
class PickSingleYcbMasterChefCanMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/002_master_chef_can/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/002_master_chef_can/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-002_master_chef_can_v2.pkl"


@configclass
class PickSingleYcbPhillipsScrewdriverMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/043_phillips_screwdriver/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/043_phillips_screwdriver/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-043_phillips_screwdriver_v2.pkl"


@configclass
class PickSingleYcbHammerMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/048_hammer/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/048_hammer/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-048_hammer_v2.pkl"


@configclass
class PickSingleYcbPadlockMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/038_padlock/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/038_padlock/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-038_padlock_v2.pkl"


@configclass
class PickSingleYcbOrangeMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/017_orange/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/017_orange/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-017_orange_v2.pkl"


@configclass
class PickSingleYcbRubiksCubeMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/077_rubiks_cube/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/077_rubiks_cube/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-077_rubiks_cube_v2.pkl"


@configclass
class PickSingleYcbSpatulaMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/033_spatula/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/033_spatula/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-033_spatula_v2.pkl"


@configclass
class PickSingleYcbToyAirplaneMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/072-e_toy_airplane/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/072-e_toy_airplane/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-072-e_toy_airplane_v2.pkl"


@configclass
class PickSingleYcbStrawberryMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/012_strawberry/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/012_strawberry/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-012_strawberry_v2.pkl"


@configclass
class PickSingleYcbLemonMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/014_lemon/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/014_lemon/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-014_lemon_v2.pkl"


@configclass
class PickSingleYcbNineHolePegTestMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/071_nine_hole_peg_test/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/071_nine_hole_peg_test/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-071_nine_hole_peg_test_v2.pkl"


@configclass
class PickSingleYcbDiceMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/062_dice/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/062_dice/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-062_dice_v2.pkl"


@configclass
class PickSingleYcbRacquetballMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/057_racquetball/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/057_racquetball/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-057_racquetball_v2.pkl"


@configclass
class PickSingleYcbBowlMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/024_bowl/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/024_bowl/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-024_bowl_v2.pkl"


@configclass
class PickSingleYcbTomatoSoupCanMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/005_tomato_soup_can/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/005_tomato_soup_can/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-005_tomato_soup_can_v2.pkl"


@configclass
class PickSingleYcbCrackerBoxMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/003_cracker_box/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/003_cracker_box/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-003_cracker_box_v2.pkl"


@configclass
class PickSingleYcbScissorsMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/037_scissors/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/037_scissors/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-037_scissors_v2.pkl"


@configclass
class PickSingleYcbPlumMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/018_plum/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/018_plum/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-018_plum_v2.pkl"


@configclass
class PickSingleYcbBleachCleanserMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/021_bleach_cleanser/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/021_bleach_cleanser/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-021_bleach_cleanser_v2.pkl"


@configclass
class PickSingleYcbMediumClampMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/050_medium_clamp/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/050_medium_clamp/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-050_medium_clamp_v2.pkl"


@configclass
class PickSingleYcbSpongeMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/026_sponge/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/026_sponge/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-026_sponge_v2.pkl"


@configclass
class PickSingleYcbPitcherBaseMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/019_pitcher_base/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/019_pitcher_base/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-019_pitcher_base_v2.pkl"


@configclass
class PickSingleYcbTennisBallMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/056_tennis_ball/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/056_tennis_ball/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-056_tennis_ball_v2.pkl"


@configclass
class PickSingleYcbColoredWoodBlocksMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/070-b_colored_wood_blocks/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/070-b_colored_wood_blocks/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-070-b_colored_wood_blocks_v2.pkl"


@configclass
class PickSingleYcbMugMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/025_mug/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/025_mug/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-025_mug_v2.pkl"


@configclass
class PickSingleYcbBaseballMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/055_baseball/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/055_baseball/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-055_baseball_v2.pkl"


@configclass
class PickSingleYcbGelatinBoxMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/009_gelatin_box/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/009_gelatin_box/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-009_gelatin_box_v2.pkl"


@configclass
class PickSingleYcbTunaFishCanMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/007_tuna_fish_can/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/007_tuna_fish_can/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-007_tuna_fish_can_v2.pkl"


@configclass
class PickSingleYcbLargeClampMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/051_large_clamp/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/051_large_clamp/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-051_large_clamp_v2.pkl"


@configclass
class PickSingleYcbPeachMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/015_peach/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/015_peach/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-015_peach_v2.pkl"


@configclass
class PickSingleYcbKnifeMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/032_knife/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/032_knife/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-032_knife_v2.pkl"


@configclass
class PickSingleYcbAppleMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/013_apple/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/013_apple/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-013_apple_v2.pkl"


@configclass
class PickSingleYcbMustardBottleMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/006_mustard_bottle/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/006_mustard_bottle/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-006_mustard_bottle_v2.pkl"


@configclass
class PickSingleYcbPearMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/016_pear/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/016_pear/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-016_pear_v2.pkl"


@configclass
class PickSingleYcbLargeMarkerMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/040_large_marker/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/040_large_marker/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-040_large_marker_v2.pkl"


@configclass
class PickSingleYcbAdjustableWrenchMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/042_adjustable_wrench/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/042_adjustable_wrench/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-042_adjustable_wrench_v2.pkl"


@configclass
class PickSingleYcbSoftballMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/054_softball/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/054_softball/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-054_softball_v2.pkl"


@configclass
class PickSingleYcbFoamBrickMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/061_foam_brick/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/061_foam_brick/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-061_foam_brick_v2.pkl"


@configclass
class PickSingleYcbSugarBoxMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/004_sugar_box/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/004_sugar_box/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-004_sugar_box_v2.pkl"


@configclass
class PickSingleYcbMarblesMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/063-b_marbles/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/063-b_marbles/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-063-b_marbles_v2.pkl"


@configclass
class PickSingleYcbPottedMeatCanMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/010_potted_meat_can/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/010_potted_meat_can/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-010_potted_meat_can_v2.pkl"


@configclass
class PickSingleYcbGolfBallMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/058_golf_ball/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/058_golf_ball/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-058_golf_ball_v2.pkl"


@configclass
class PickSingleYcbMiniSoccerBallMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/053_mini_soccer_ball/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/053_mini_soccer_ball/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-053_mini_soccer_ball_v2.pkl"


@configclass
class PickSingleYcbPuddingBoxMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/008_pudding_box/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/008_pudding_box/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-008_pudding_box_v2.pkl"


@configclass
class PickSingleYcbSpoonMetaCfg(_PickSingleYcbBaseMetaCfg):
    objects = [
        RigidObjMetaCfg(
            name="obj",
            usd_path="roboverse_data/assets/maniskill/ycb/031_spoon/object_proc.usd",
            urdf_path="roboverse_data/assets/maniskill/ycb/031_spoon/model_scaled.urdf",
            physics=PhysicStateType.RIGIDBODY,
        )
    ]
    traj_filepath = "roboverse_data/trajs/maniskill/pick_single_ycb/trajectory-franka-031_spoon_v2.pkl"
