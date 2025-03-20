from metasim.utils import configclass

from .scene.scene_A import SCENE_A
from .scene.scene_B import SCENE_B
from .scene.scene_C import SCENE_C
from .scene.scene_D import SCENE_D
from .task.close_drawer_metacfg import CloseDrawerMetaCfg
from .task.lift_blue_block_drawer_metacfg import LiftBlueBlockDrawerMetaCfg
from .task.lift_blue_block_slider_metacfg import LiftBlueBlockSliderMetaCfg
from .task.lift_blue_block_table_metacfg import LiftBlueBlockTableMetaCfg
from .task.lift_pink_block_drawer_metacfg import LiftPinkBlockDrawerMetaCfg
from .task.lift_pink_block_slider_metacfg import LiftPinkBlockSliderMetaCfg
from .task.lift_pink_block_table_metacfg import LiftPinkBlockTableMetaCfg
from .task.lift_red_block_drawer_metacfg import LiftRedBlockDrawerMetaCfg
from .task.lift_red_block_slider_metacfg import LiftRedBlockSliderMetaCfg
from .task.lift_red_block_table_metacfg import LiftRedBlockTableMetaCfg
from .task.move_slider_left_metacfg import MoveSliderLeftMetaCfg
from .task.move_slider_right_metacfg import MoveSliderRightMetaCfg
from .task.open_drawer_metacfg import OpenDrawerMetaCfg
from .task.place_in_drawer_metacfg import PlaceInDrawerMetaCfg
from .task.place_in_slider_metacfg import PlaceInSliderMetaCfg
from .task.push_blue_block_left_metacfg import PushBlueBlockLeftMetaCfg
from .task.push_blue_block_right_metacfg import PushBlueBlockRightMetaCfg
from .task.push_into_drawer_metacfg import PushIntoDrawerMetaCfg
from .task.push_pink_block_left_metacfg import PushPinkBlockLeftMetaCfg
from .task.push_pink_block_right_metacfg import PushPinkBlockRightMetaCfg
from .task.push_red_block_left_metacfg import PushRedBlockLeftMetaCfg
from .task.push_red_block_right_metacfg import PushRedBlockRightMetaCfg
from .task.rotate_blue_block_left_metacfg import RotateBlueBlockLeftMetaCfg
from .task.rotate_blue_block_right_metacfg import RotateBlueBlockRightMetaCfg
from .task.rotate_pink_block_left_metacfg import RotatePinkBlockLeftMetaCfg
from .task.rotate_pink_block_right_metacfg import RotatePinkBlockRightMetaCfg
from .task.rotate_red_block_left_metacfg import RotateRedBlockLeftMetaCfg
from .task.rotate_red_block_right_metacfg import RotateRedBlockRightMetaCfg
from .task.stack_block_metacfg import StackBlockMetaCfg
from .task.unstack_block_metacfg import UnstackBlockMetaCfg


@configclass
class LiftRedBlockTableAMetaCfg(LiftRedBlockTableMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_red_block_table_a/v2"


@configclass
class LiftRedBlockTableBMetaCfg(LiftRedBlockTableMetaCfg):
    objects = SCENE_B.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_red_block_table_a/v2"  # TODO: use scene_a for testing


@configclass
class LiftRedBlockTableCMetaCfg(LiftRedBlockTableMetaCfg):
    objects = SCENE_C.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_red_block_table_a/v2"  # TODO: use scene_a for testing


@configclass
class LiftRedBlockTableDMetaCfg(LiftRedBlockTableMetaCfg):
    objects = SCENE_D.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_red_block_table_a/v2"  # TODO: use scene_a for testing


@configclass
class LiftRedBlockSliderAMetaCfg(LiftRedBlockSliderMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_red_block_slider_a/v2"


@configclass
class LiftRedBlockDrawerAMetaCfg(LiftRedBlockDrawerMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_red_block_drawer_a/v2"


@configclass
class LiftBlueBlockTableAMetaCfg(LiftBlueBlockTableMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_blue_block_table_a/v2"


@configclass
class LiftBlueBlockSliderAMetaCfg(LiftBlueBlockSliderMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_blue_block_slider_a/v2"


@configclass
class LiftBlueBlockDrawerAMetaCfg(LiftBlueBlockDrawerMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_blue_block_drawer_a/v2"


@configclass
class LiftPinkBlockTableAMetaCfg(LiftPinkBlockTableMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_pink_block_table_a/v2"


@configclass
class LiftPinkBlockSliderAMetaCfg(LiftPinkBlockSliderMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_pink_block_slider_a/v2"


@configclass
class LiftPinkBlockDrawerAMetaCfg(LiftPinkBlockDrawerMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/lift_pink_block_drawer_a/v2"


@configclass
class PlaceInSliderAMetaCfg(PlaceInSliderMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/place_in_slider_a/v2"


@configclass
class PlaceInDrawerAMetaCfg(PlaceInDrawerMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/place_in_drawer_a/v2"


@configclass
class RotateRedBlockRightAMetaCfg(RotateRedBlockRightMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/rotate_red_block_right_a/v2"


@configclass
class RotateRedBlockLeftAMetaCfg(RotateRedBlockLeftMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/rotate_red_block_left_a/v2"


@configclass
class RotateBlueBlockRightAMetaCfg(RotateBlueBlockRightMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/rotate_blue_block_right_a/v2"


@configclass
class RotateBlueBlockLeftAMetaCfg(RotateBlueBlockLeftMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/rotate_blue_block_left_a/v2"


@configclass
class RotatePinkBlockRightAMetaCfg(RotatePinkBlockRightMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/rotate_pink_block_right_a/v2"


@configclass
class RotatePinkBlockLeftAMetaCfg(RotatePinkBlockLeftMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/rotate_pink_block_left_a/v2"


@configclass
class PushRedBlockRightAMetaCfg(PushRedBlockRightMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/push_red_block_right_a/v2"


@configclass
class PushRedBlockLeftAMetaCfg(PushRedBlockLeftMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/push_red_block_left_a/v2"


@configclass
class PushBlueBlockRightAMetaCfg(PushBlueBlockRightMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/push_blue_block_right_a/v2"


@configclass
class PushBlueBlockLeftAMetaCfg(PushBlueBlockLeftMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/push_blue_block_left_a/v2"


@configclass
class PushPinkBlockRightAMetaCfg(PushPinkBlockRightMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/push_pink_block_right_a/v2"


@configclass
class PushPinkBlockLeftAMetaCfg(PushPinkBlockLeftMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/push_pink_block_left_a/v2"


@configclass
class MoveSliderLeftAMetaCfg(MoveSliderLeftMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/move_slider_left_a/v2"


@configclass
class MoveSliderRightAMetaCfg(MoveSliderRightMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/move_slider_right_a/v2"


@configclass
class OpenDrawerAMetaCfg(OpenDrawerMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/open_drawer_a/v2"


@configclass
class CloseDrawerAMetaCfg(CloseDrawerMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/close_drawer_a/v2"


@configclass
class StackBlockAMetaCfg(StackBlockMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/stack_block_a/v2"


@configclass
class UnstackBlockAMetaCfg(UnstackBlockMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/unstack_block_a/v2"


@configclass
class PushIntoDrawerAMetaCfg(PushIntoDrawerMetaCfg):
    objects = SCENE_A.objects
    traj_filepath = "roboverse_data/trajs/calvin/push_into_drawer_a/v2"
