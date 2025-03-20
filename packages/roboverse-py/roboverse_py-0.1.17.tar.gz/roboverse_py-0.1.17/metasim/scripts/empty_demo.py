from __future__ import annotations

from typing import Literal

try:
    import isaacgym  # noqa: F401
except ImportError:
    pass

import imageio
import rootutils
import torch
import tyro
from loguru import logger as log
from rich.logging import RichHandler

rootutils.setup_root(__file__, pythonpath=True)
log.configure(handlers=[{"sink": RichHandler(), "format": "{message}"}])


from metasim.cfg.cameras import PinholeCameraMetaCfg
from metasim.cfg.objects import PrimitiveCubeMetaCfg
from metasim.cfg.randomization import RandomizationMetaCfg
from metasim.cfg.render import RenderMetaCfg
from metasim.cfg.scenario import ScenarioMetaCfg
from metasim.constants import PhysicStateType, SimType
from metasim.utils import configclass
from metasim.utils.setup_util import get_sim_handler_class


@configclass
class Args:
    robot: str = "franka"
    scene: str | None = None
    render: RenderMetaCfg = RenderMetaCfg()
    random: RandomizationMetaCfg = RandomizationMetaCfg()

    ## Handlers
    sim: Literal["isaaclab", "isaacgym", "genesis", "pyrep", "pybullet", "sapien", "mujoco", "blender"] = "isaaclab"
    renderer: Literal["isaaclab", "isaacgym", "genesis", "pyrep", "pybullet", "sapien", "mujoco", "blender"] | None = (
        None
    )

    ## Others
    num_envs: int = 1
    try_add_table: bool = True
    object_states: bool = False
    split: Literal["train", "val", "test", "all"] = "all"
    headless: bool = False

    ## Only in args
    save_image_dir: str | None = "tmp"
    save_video_path: str | None = None
    stop_on_runout: bool = False

    def __post_init__(self):
        log.info(f"Args: {self}")


args = tyro.cli(Args)

camera = PinholeCameraMetaCfg(
    name="camera",
    data_types=["rgb", "depth"],
    width=256,
    height=256,
    pos=(1.5, -1.5, 1.5),  # near
    # pos=(12.0, -12.0, 20.0),  # far
    look_at=(0.0, 0.0, 0.0),
)
scenario = ScenarioMetaCfg(
    robot=args.robot,
    try_add_table=False,
    sim=args.sim,
    cameras=[camera],
    headless=args.headless,
)
scenario.objects = [
    PrimitiveCubeMetaCfg(
        name="cube",
        size=(0.1, 0.1, 0.1),
        color=(1.0, 0.0, 0.0),
        physics=PhysicStateType.RIGIDBODY,
        mjcf_path="roboverse_data/assets/maniskill/cube/cube.mjcf",
    )
]

handler_class = get_sim_handler_class(SimType(args.sim))
handler = handler_class(scenario, 1, headless=args.headless)
handler.launch()

handler.set_states([
    {
        "cube": {
            "pos": torch.tensor([0.3, 0.3, 0.05]),
            "rot": torch.tensor([1.0, 0.0, 0.0, 0.0]),
        },
        "franka": {
            "pos": torch.tensor([0.0, 0.0, 0.0]),
            "rot": torch.tensor([1.0, 0.0, 0.0, 0.0]),
            "dof_pos": {
                "panda_joint1": 0.0,
                "panda_joint2": 0.0,
                "panda_joint3": 0.0,
                "panda_joint4": 0.0,
                "panda_joint5": 0.0,
                "panda_joint6": 0.0,
                "panda_joint7": 0.0,
                "panda_finger_joint1": 0.0,
                "panda_finger_joint2": 0.0,
            },
        },
    }
])
if args.sim == "isaaclab":
    obs, _ = handler.reset()
else:
    handler.simulate()
    obs = handler.get_observation()

imageio.imwrite("test.png", obs["rgb"][0])
