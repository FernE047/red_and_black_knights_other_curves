from pathlib import Path
from typing import Literal

SAVE_FOLDER = Path("./out")

ChoiceOptions = Literal["Simple"]
ColourData = tuple[int, int, int, int]
CoordData = tuple[int, int]
BoardData = list[list[int]]


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

    def build_place_board(self) -> None:
        if self.choice == "Simple":
            return self.fill_simple_board()
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
