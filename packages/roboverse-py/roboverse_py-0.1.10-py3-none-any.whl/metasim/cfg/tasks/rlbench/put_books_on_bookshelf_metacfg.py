from metasim.cfg.objects import RigidObjMetaCfg
from metasim.constants import PhysicStateType
from metasim.utils import configclass

from .rlbench_task_metacfg import RLBenchTaskMetaCfg


@configclass
class PutBooksOnBookshelfMetaCfg(RLBenchTaskMetaCfg):
    episode_length = 200
    traj_filepath = "roboverse_data/trajs/rlbench/put_books_on_bookshelf/v2"
    objects = [
        RigidObjMetaCfg(
            name="bookshelf_visual",
            filepath="roboverse_data/assets/rlbench/put_books_on_bookshelf/bookshelf_visual/usd/bookshelf_visual.usd",
            physics=PhysicStateType.GEOM,
        ),
        RigidObjMetaCfg(
            name="book0_visual",
            filepath="roboverse_data/assets/rlbench/put_books_on_bookshelf/book0_visual/usd/book0_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book1_visual",
            filepath="roboverse_data/assets/rlbench/put_books_on_bookshelf/book1_visual/usd/book1_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
        RigidObjMetaCfg(
            name="book2_visual",
            filepath="roboverse_data/assets/rlbench/put_books_on_bookshelf/book2_visual/usd/book2_visual.usd",
            physics=PhysicStateType.RIGIDBODY,
        ),
    ]
    # TODO: add checker
