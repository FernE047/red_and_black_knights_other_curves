from enum import Enum
from pathlib import Path
from typing import Literal

SAVE_FOLDER = Path("./out")

ChoiceOptions = Literal["Simple", "Spiral"]
ColourData = tuple[int, int, int, int]
CoordData = tuple[int, int]

class Direction(Enum):
    UP = 0,
    RIGHT = 1,
    DOWN = 2,
    LEFT = 3

def apply_direction(coord: CoordData, direction: Direction) -> CoordData:
    y, x = coord
    if direction == Direction.UP:
        return (y - 1, x)
    if direction == Direction.RIGHT:
        return (y, x + 1)
    if direction == Direction.DOWN:
        return (y + 1, x)
    if direction == Direction.LEFT:
        return (y, x - 1)

class Board:
    KNIGHT_MOVES = (
        (-2, -1),
        (-2, 1),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
        (2, -1),
        (2, 1),
    )

    def __init__(
        self, height: int, width: int, colours_amount: int, choice: ChoiceOptions | None
    ) -> None:
        self.height = height
        self.width = width
        self.cell_amount = height * width
        self.colours_amount = colours_amount
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.ordered_cells: list[CoordData] = []
        self.cursors: list[int] = [0 for _ in range(colours_amount)]
        self.choice = choice
        self.build_place_board()

    def fill_simple_board(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                coord = (y, x)
                self.ordered_cells.append(coord)

    def fill_spiral_board(self) -> None:
        is_finished = False
        coord = (self.height//2, self.width//2)
        self.ordered_cells.append(coord)
        movement = 1
        while not is_finished:
            is_finished = True
            for direction in Direction:
                for _ in range(movement):
                    coord = apply_direction(coord, direction)
                    if self.is_inside(coord[0],coord[1]):
                        is_finished = False
                        self.ordered_cells.append(coord)
                if direction in [Direction.RIGHT, Direction.LEFT]:
                    movement += 1
        self.cell_amount = len(self.ordered_cells)

    def build_place_board(self) -> None:
        if self.choice == "Simple":
            return self.fill_simple_board()
        if self.choice == "Spiral":
            return self.fill_spiral_board()
        raise NotImplementedError("choose a valid option")

    def is_inside(self, y: int, x: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def is_coord_safe(self, coord: CoordData, turn: int) -> bool:
        piece = turn + 1
        y, x = coord
        for dy, dx in self.KNIGHT_MOVES:
            ay = y + dy
            ax = x + dx
            if not self.is_inside(ay, ax):
                continue
            cell = self.board[ay][ax]
            if cell and cell!= piece:
                return False
        return True

    def solve(self, colours: list[ColourData], background_color: ColourData) -> None:
        turn = 0
        while True:
            cursor = self.cursors[turn]
            coord = self.ordered_cells[cursor]
            y,x = coord
            cell = self.board[y][x]
            if cell != 0 or not self.is_coord_safe(coord, turn):
                cursor += 1
                if cursor >= self.cell_amount:
                    break
                self.cursors[turn] = cursor
                continue
            turn += 1
            self.board[y][x] = turn
            if turn >= len(colours):
                turn = 0
        self.render(colours, background_color)

    def render(self, colours: list[ColourData], background_color: ColourData) -> None:
        from PIL import Image

        img = Image.new("RGBA", (self.width, self.height), background_color)
        for y in range(self.height):
            for x in range(self.width):
                piece = self.board[y][x]
                if piece == 0:
                    continue
                img.putpixel((x, y), colours[piece - 1])
        file_amount = sum(1 for item in SAVE_FOLDER.iterdir() if item.is_file())
        output_image = SAVE_FOLDER / f"output_{file_amount}.png"
        img.save(output_image)
