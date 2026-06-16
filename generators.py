from enum import Enum
from typing import Callable, Iterator
from gilbert_curve import gilbert_d2xy  # type: ignore
import random


class ChoiceOptions(Enum):
    SIMPLE = 0
    SPIRAL = 1
    SPIRAL_2 = 2
    SPIRAL_3 = 3
    SNAKE = 4
    SPIRAL_DIAGONAL = 5
    SPIRAL_DIAGONAL_2 = 6
    GILBERT_CURVE = 7
    MID_GILBERT_CURVE = 8
    RANDOM = 9
    RANDOM_ROWS = 10
    CHECKERBOARD = 11
    CENTER_OUT_ROWS = 12
    DIAGONAL_SWEEP = 13


class Direction(Enum):
    UP = 0
    UPRIGHT = 1
    RIGHT = 2
    DOWNRIGHT = 3
    DOWN = 4
    DOWNLEFT = 5
    LEFT = 6
    UPLEFT = 7


DIRECTION_OFFSETS = {
    Direction.UP: (-1, 0),
    Direction.UPRIGHT: (-1, 1),
    Direction.RIGHT: (0, 1),
    Direction.DOWNRIGHT: (1, 1),
    Direction.DOWN: (1, 0),
    Direction.DOWNLEFT: (1, -1),
    Direction.LEFT: (0, -1),
    Direction.UPLEFT: (-1, -1),
}
ORTHOGONAL_DIRECTIONS = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)
DIAGONAL_DIRECTIONS = (
    Direction.UPRIGHT,
    Direction.DOWNRIGHT,
    Direction.DOWNLEFT,
    Direction.UPLEFT,
)

CoordData = tuple[int, int]
GeneratorRecipe = Callable[[int, int], Iterator[CoordData]]


def apply_direction(coord: CoordData, direction: Direction) -> CoordData:
    y, x = coord
    offsets = DIRECTION_OFFSETS[direction]
    return (y + offsets[0], x + offsets[1])


def is_inside(y: int, x: int, height: int, width: int) -> bool:
    return 0 <= y < height and 0 <= x < width


def simple() -> GeneratorRecipe:
    def generator(height: int, width: int) -> Iterator[CoordData]:
        for y in range(height):
            for x in range(width):
                yield (y, x)

    return generator


def spiral(initial_coord: CoordData) -> GeneratorRecipe:
    def generator(height: int, width: int) -> Iterator[CoordData]:
        is_finished = False
        coord = initial_coord
        yield coord
        movement = 1
        while not is_finished:
            is_finished = True
            for direction in ORTHOGONAL_DIRECTIONS:
                for _ in range(movement):
                    coord = apply_direction(coord, direction)
                    if is_inside(coord[0], coord[1], height, width):
                        is_finished = False
                        yield coord
                if direction in [Direction.RIGHT, Direction.LEFT]:
                    movement += 1
    return generator


def snake() -> GeneratorRecipe:
    def generator(height: int, width: int) -> Iterator[CoordData]:
        is_finished = False
        coord = (0, 0)
        yield coord
        movement = 1
        coord = apply_direction(coord, Direction.DOWN)
        if not is_inside(coord[0], coord[1], height, width):
            return
        while not is_finished:
            is_finished = True
            for direction in (
                Direction.RIGHT,
                Direction.UP,
                Direction.DOWN,
                Direction.LEFT,
            ):
                for _ in range(movement):
                    coord = apply_direction(coord, direction)
                    if is_inside(coord[0], coord[1], height, width):
                        is_finished = False
                        yield coord
                if direction == Direction.UP:
                    coord = apply_direction(coord, Direction.RIGHT)
                    if is_inside(coord[0], coord[1], height, width):
                        is_finished = False
                        yield coord
                    movement += 1
                if direction == Direction.LEFT:
                    coord = apply_direction(coord, Direction.DOWN)
                    if is_inside(coord[0], coord[1], height, width):
                        is_finished = False
                        yield coord
                    movement += 1
    return generator


def spiral_diagonal(initial_coord: CoordData) -> GeneratorRecipe:
    def generator(height: int, width: int) -> Iterator[CoordData]:
        is_finished = False
        coord = initial_coord
        yield coord
        movement = 1
        while not is_finished:
            coord = apply_direction(coord, Direction.LEFT)
            is_finished = True
            for direction in DIAGONAL_DIRECTIONS:
                for _ in range(movement):
                    coord = apply_direction(coord, direction)
                    if is_inside(coord[0], coord[1], height, width):
                        is_finished = False
                        yield coord
            movement += 1
    return generator


def gilbert() -> GeneratorRecipe:
    #just a wrapper LMAO
    def generator(height: int, width: int) -> Iterator[CoordData]:
        for i in range(height * width):
            coord = gilbert_d2xy(i, height, width)
            yield coord
    return generator


def random_generator() -> GeneratorRecipe:
    def generator(height: int, width: int) -> Iterator[CoordData]:
        coords = [(y, x) for y in range(height) for x in range(width)]
        random.shuffle(coords)
        for coord in coords:
            yield coord
    return generator


def random_rows() -> GeneratorRecipe:
    def generator(height: int, width: int) -> Iterator[CoordData]:
        rows = list(range(height))
        random.shuffle(rows)
        for y in rows:
            for x in range(width):
                yield (y, x)
    return generator

def center_out_spiral() -> GeneratorRecipe:
    """Gera coordenadas do centro para as bordas em uma espiral anti-horária contínua."""
    import math

    def generator(height: int, width: int) -> Iterator[CoordData]:
        center_y, center_x = height // 2, width // 2
        coords = [(y, x) for y in range(height) for x in range(width)]
        def get_spiral_weight(coord: CoordData) -> float:
            y, x = coord
            dy = y - center_y
            dx = x - center_x
            distance_sq = dy**2 + dx**2
            angle = math.atan2(dy, dx) + math.pi
            return (distance_sq * 10) + angle
        coords.sort(key=get_spiral_weight)
        for coord in coords:
            yield coord

    return generator

def perlin_noise_flow(scale: float = 0.1) -> GeneratorRecipe:
    import math
    def generator(height: int, width: int) -> Iterator[CoordData]:
        coords = [(y, x) for y in range(height) for x in range(width)]
        def get_density(y: int, x: int) -> float:
            val = math.sin(y * scale) + math.cos(x * scale) + math.sin((y + x) * scale)
            return val
        coords.sort(key=lambda c: get_density(c[0], c[1]))
        for coord in coords:
            yield coord
    return generator

def safe_next(iterator: Iterator[CoordData]) -> CoordData | None:
    try:
        return next(iterator)
    except StopIteration as _:
        return None
