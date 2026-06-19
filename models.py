from enum import Enum
from typing import Iterator


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


ORTHOGONAL_DIRECTIONS = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)
DIAGONAL_DIRECTIONS = (
    Direction.UPRIGHT,
    Direction.DOWNRIGHT,
    Direction.DOWNLEFT,
    Direction.UPLEFT,
)
Generator = Iterator[CoordData]