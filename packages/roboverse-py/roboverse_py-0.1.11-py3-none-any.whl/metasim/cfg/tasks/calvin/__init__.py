## TODO: only export task metacfg whose suffix is A/B/C/D + MetaCfg
from .calvin import *

__all__ = [task for task in dir() if task.endswith("AMetaCfg")]
