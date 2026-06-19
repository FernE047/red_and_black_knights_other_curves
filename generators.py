from typing import Callable
from gilbert_curve import gilbert_xy_generator
import random
from models import (
    DIAGONAL_DIRECTIONS,
    ORTHOGONAL_DIRECTIONS,
    CoordData,
    Direction,
    Generator,
)

GeneratorRecipe = Callable[[int, int], Generator]


def apply_direction(coord: CoordData, direction: Direction) -> CoordData:
    y, x = coord
    return (y + direction.value[0], x + direction.value[1])


def is_inside(y: int, x: int, height: int, width: int) -> bool:
    return 0 <= y < height and 0 <= x < width


def simple() -> GeneratorRecipe:
    def generator(height: int, width: int) -> Generator:
        for y in range(height):
            for x in range(width):
                yield (y, x)

    return generator


def spiral(initial_coord: CoordData) -> GeneratorRecipe:
    def generator(height: int, width: int) -> Generator:
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
    snake_sequence = (
        Direction.RIGHT,
        Direction.UP,
        Direction.DOWN,
        Direction.LEFT,
    )

    def generator(height: int, width: int) -> Generator:
        is_finished = False
        coord = (0, 0)
        yield coord
        movement = 1
        coord = apply_direction(coord, Direction.DOWN)
        if not is_inside(coord[0], coord[1], height, width):
            return
        while not is_finished:
            is_finished = True
            for direction in snake_sequence:
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
    def generator(height: int, width: int) -> Generator:
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
    # just a wrapper LMAO
    def generator(height: int, width: int) -> Generator:
        yield from gilbert_xy_generator(height, width)

    return generator


def random_generator() -> GeneratorRecipe:
    def generator(height: int, width: int) -> Generator:
        coords = [(y, x) for y in range(height) for x in range(width)]
        random.shuffle(coords)
        for coord in coords:
            yield coord

    return generator


def random_rows() -> GeneratorRecipe:
    def generator(height: int, width: int) -> Generator:
        rows = list(range(height))
        random.shuffle(rows)
        for y in rows:
            for x in range(width):
                yield (y, x)

    return generator


def center_out_spiral() -> GeneratorRecipe:
    """Gera coordenadas do centro para as bordas em uma espiral anti-horária contínua."""
    import math

    def generator(height: int, width: int) -> Generator:
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

    def generator(height: int, width: int) -> Generator:
        coords = [(y, x) for y in range(height) for x in range(width)]

        def get_density(y: int, x: int) -> float:
            val = math.sin(y * scale) + math.cos(x * scale) + math.sin((y + x) * scale)
            return val

        coords.sort(key=lambda c: get_density(c[0], c[1]))
        for coord in coords:
            yield coord

    return generator
