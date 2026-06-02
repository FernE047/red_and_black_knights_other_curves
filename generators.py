from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from boards import Board


class ChoiceOptions(Enum):
    SIMPLE = 0
    SPIRAL = 1
    SPIRAL_2 = 2
    SPIRAL_3 = 3
    SNAKE = 4
    SPIRAL_DIAGONAL = 5
    SPIRAL_DIAGONAL_2 = 6


class Direction(Enum):
    UP = 0
    UPRIGHT = 1
    RIGHT = 2
    DOWNRIGHT = 3
    DOWN = 4
    DOWNLEFT = 5
    LEFT = 6
    UPLEFT = 7


ORTHOGONAL_DIRECTIONS = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)
DIAGONAL_DIRECTIONS = (
    Direction.UPRIGHT,
    Direction.DOWNRIGHT,
    Direction.DOWNLEFT,
    Direction.UPLEFT,
)

CoordData = tuple[int, int]


def apply_direction(coord: CoordData, direction: Direction) -> CoordData:
    y, x = coord
    if direction == Direction.UP:
        return (y - 1, x)
    if direction == Direction.UPRIGHT:
        return (y - 1, x + 1)
    if direction == Direction.RIGHT:
        return (y, x + 1)
    if direction == Direction.DOWNRIGHT:
        return (y + 1, x + 1)
    if direction == Direction.DOWN:
        return (y + 1, x)
    if direction == Direction.DOWNLEFT:
        return (y + 1, x - 1)
    if direction == Direction.LEFT:
        return (y, x - 1)
    if direction == Direction.UPLEFT:
        return (y - 1, x - 1)

def fill_simple_board(board:Board) -> Iterator[CoordData]:
    for y in range(board.height):
        for x in range(board.width):
            coord = (y, x)
            yield coord

def fill_spiral_board(board:Board, initial_coord: CoordData) -> Iterator[CoordData]:
    is_finished = False
    coord = initial_coord
    yield coord
    movement = 1
    while not is_finished:
        is_finished = True
        for direction in ORTHOGONAL_DIRECTIONS:
            for _ in range(movement):
                coord = apply_direction(coord, direction)
                if board.is_inside(coord[0], coord[1]):
                    is_finished = False
                    yield coord
            if direction in [Direction.RIGHT, Direction.LEFT]:
                movement += 1
    board.cell_amount = len(board.ordered_cells)

def fill_snake_board(board:Board) -> Iterator[CoordData]:
    is_finished = False
    coord = (0, 0)
    yield coord
    movement = 1
    coord = apply_direction(coord, Direction.DOWN)
    if not board.is_inside(coord[0], coord[1]):
        board.cell_amount = len(board.ordered_cells)
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
                if board.is_inside(coord[0], coord[1]):
                    is_finished = False
                    yield coord
            if direction == Direction.UP:
                
                coord = apply_direction(coord,  Direction.RIGHT)
                if board.is_inside(coord[0], coord[1]):
                    is_finished = False
                    yield coord
                movement += 1
            if direction == Direction.LEFT:
                
                coord = apply_direction(coord, Direction.DOWN)
                if board.is_inside(coord[0], coord[1]):
                    is_finished = False
                    yield coord
                movement += 1
    board.cell_amount = len(board.ordered_cells)

def fill_spiral_diagonal_board(board:Board, left_first: bool) -> Iterator[CoordData]:
    is_finished = False
    coord = (0, 0)
    yield coord
    movement = 1
    while not is_finished:
        coord = apply_direction(coord, Direction.LEFT)
        if left_first:
            if board.is_inside(coord[0], coord[1]):
                yield coord
        is_finished = True
        for direction in DIAGONAL_DIRECTIONS:
            for step in range(movement):
                if (
                    left_first
                    and direction == Direction.UPLEFT
                    and step == movement - 1
                ):
                    break
                coord = apply_direction(coord, direction)
                if board.is_inside(coord[0], coord[1]):
                    is_finished = False
                    yield coord
        movement += 1
    board.cell_amount = len(board.ordered_cells)

def build_generator(board:Board) -> Iterator[CoordData]:
    if board.choice == ChoiceOptions.SIMPLE:
        return fill_simple_board(board)
    if board.choice == ChoiceOptions.SPIRAL:
        return fill_spiral_board(board, (board.height // 2, board.width // 2))
    if board.choice == ChoiceOptions.SPIRAL_2:
        return fill_spiral_board(board, (0, 0))
    if board.choice == ChoiceOptions.SPIRAL_3:
        return fill_spiral_board(board, (0, board.width // 2))
    if board.choice == ChoiceOptions.SNAKE:
        return fill_snake_board(board, )
    if board.choice == ChoiceOptions.SPIRAL_DIAGONAL:
        return fill_spiral_diagonal_board(board, True)
    if board.choice == ChoiceOptions.SPIRAL_DIAGONAL_2:
        return fill_spiral_diagonal_board(board, False)
    raise NotImplementedError("choose a valid option")

def safe_next(iterator: Iterator[CoordData]) -> CoordData | None:
    try:
        return next(iterator)
    except StopIteration as _:
        return None