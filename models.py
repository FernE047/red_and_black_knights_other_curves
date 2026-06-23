from enum import Enum
from typing import Callable, Iterator


CoordData = tuple[int, int]


class Direction(Enum):
    UP = (-1, 0)
    UPRIGHT = (-1, 1)
    RIGHT = (0, 1)
    DOWNRIGHT = (1, 1)
    DOWN = (1, 0)
    DOWNLEFT = (1, -1)
    LEFT = (0, -1)
    UPLEFT = (-1, -1)


class Rotation(Enum):
    ONCE = 90
    TWICE = 180
    THRICE = 270


class Reflection(Enum):
    VERTICAL = 0
    HORIZONTAL = 1
    MAIN_DIAGONAL = 2
    ANTI_DIAGONAL = 3


class Action(Enum):
    PASTE = 0
    REVERSE = 1


Command = Direction | Rotation | Reflection | Action
Procedure = list[Command]
PathData = list[Direction]
ORTHOGONAL_DIRECTIONS = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)
DIAGONAL_DIRECTIONS = (
    Direction.UPRIGHT,
    Direction.DOWNRIGHT,
    Direction.DOWNLEFT,
    Direction.UPLEFT,
)
Generator = Iterator[CoordData]
GeneratorRecipe = Callable[[int, int], Generator]
