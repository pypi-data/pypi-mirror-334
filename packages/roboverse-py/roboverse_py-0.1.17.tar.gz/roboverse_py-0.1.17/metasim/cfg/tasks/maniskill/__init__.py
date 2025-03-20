# ruff: noqa: F401

import importlib

__CANDIDATE_MODULES = [
    "peg_insertion_side",
    "pick_single_egad",
    "pick_single_ycb",
]


def __getattr__(name):
    from .pick_cube_metacfg import PickCubeMetaCfg
    from .plug_charger_metacfg import PlugChargerMetaCfg
    from .stack_cube_metacfg import StackCubeMetaCfg
    from .stack_green_cube_metacfg import StackGreenCubeMetaCfg

    if name in locals():
        return locals()[name]

    # Lazy load modules
    for module_name in __CANDIDATE_MODULES:
        module = importlib.import_module(f".{module_name}", __name__)
        if name in module.__dict__:
            return getattr(module, name)

    raise AttributeError(f"module {__name__} has no attribute {name}")
