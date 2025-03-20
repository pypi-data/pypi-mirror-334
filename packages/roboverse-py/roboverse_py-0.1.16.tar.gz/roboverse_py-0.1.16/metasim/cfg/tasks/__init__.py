# ruff: noqa: F401

"""Sub-module containing the task configuration."""

import time

from loguru import logger as log

from .base_task_metacfg import BaseTaskMetaCfg


def __get_quick_ref():
    tic = time.time()

    from .calvin.calvin import MoveSliderLeftAMetaCfg
    from .debug.reach_origin_metacfg import ReachOriginMetaCfg
    from .dmcontrol.walker_walk_metacfg import WalkerWalkMetaCfg
    from .fetch import FetchCloseBoxMetaCfg
    from .gapartnet import GapartnetOpenDrawerMetaCfg
    from .humanoidbench import StandMetaCfg
    from .isaacgym_envs.ant_isaacgym_metacfg import AntIsaacGymMetaCfg
    from .libero.libero_objects.libero_pick_alphabet_soup import LiberoPickAlphabetSoupMetaCfg
    from .libero.libero_objects.libero_pick_bbq_sauce import LiberoPickBbqSauceMetaCfg
    from .libero.libero_objects.libero_pick_butter import LiberoPickButterMetaCfg
    from .libero.libero_objects.libero_pick_chocolate_pudding import LiberoPickChocolatePuddingMetaCfg
    from .libero.libero_objects.libero_pick_cream_cheese import LiberoPickCreamCheeseMetaCfg
    from .libero.libero_objects.libero_pick_ketchup import LiberoPickKetchupMetaCfg
    from .libero.libero_objects.libero_pick_milk import LiberoPickMilkMetaCfg
    from .libero.libero_objects.libero_pick_orange_juice import LiberoPickOrangeJuiceMetaCfg
    from .libero.libero_objects.libero_pick_salad_dressing import LiberoPickSaladDressingMetaCfg
    from .libero.libero_objects.libero_pick_tomato_sauce import LiberoPickTomatoSauceMetaCfg
    from .maniskill.pick_cube_metacfg import PickCubeMetaCfg
    from .maniskill.pick_single_ycb import PickSingleYcbCrackerBoxMetaCfg
    from .maniskill.stack_cube_metacfg import StackCubeMetaCfg
    from .rlafford.rl_afford_open_door_metacfg import RLAffordOpenDoorMetaCfg
    from .rlbench.basketball_in_hoop_metacfg import BasketballInHoopMetaCfg
    from .rlbench.close_box_metacfg import CloseBoxMetaCfg
    from .robosuite import SquareD0MetaCfg, SquareD1MetaCfg, SquareD2MetaCfg, StackD0MetaCfg
    from .simpler_env.simpler_env_grasp_opened_coke_can_metacfg import SimplerEnvGraspOpenedCokeCanMetaCfg
    from .skillblender import G1BaseTaskMetaCfg, H1BaseTaskMetaCfg
    from .uh1 import MabaoguoMetaCfg

    toc = time.time()

    log.trace(f"Time taken to load quick ref: {toc - tic:.2f} seconds")

    return locals()


__quick_ref = __get_quick_ref()


def __getattr__(name):
    if name in __quick_ref:
        return __quick_ref[name]
    else:
        raise AttributeError(f"Module {__name__} has no attribute {name}")
