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
        self.colours_amount = colours_amount
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.ordered_cells: list[list[CoordData]] = [[] for _ in range(colours_amount)]
        self.choice = choice  # used later to render
        self.build_place_board()

    def fill_simple_board(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                coord = (y, x)
                for cell_orders in self.ordered_cells:
                    cell_orders.append(coord)

    def build_place_board(self) -> None:
        if self.choice == "Simple":
            return self.fill_simple_board()
        raise NotImplementedError("choose a valid option")

    def remove_coord(self, coord: CoordData, turn: int) -> None:
        for colour_index in range(self.colours_amount):
            if colour_index == turn:
                continue
            cell_order = self.ordered_cells[colour_index]
            if coord in cell_order:
                cell_order.remove(coord)

    def is_inside(self, y: int, x: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def place_attacks(self, coord: CoordData, turn: int) -> None:
        y, x = coord
        for dy, dx in self.KNIGHT_MOVES:
            ay = y + dy
            ax = x + dx
            if not self.is_inside(ay, ax):
                continue
            self.remove_coord((ay, ax), turn)

    def place_piece(self, coord: CoordData, turn: int) -> None:
        piece = turn + 1
        y, x = coord
        self.board[y][x] = piece
        self.remove_coord(coord, turn)
        self.place_attacks(coord, turn)

    def solve(self, colours: list[ColourData], background_color: ColourData) -> None:
        turn = 0
        while True:
            cell_order = self.ordered_cells[turn]
            if len(cell_order) == 0:
                break
            coord = cell_order.pop(0)
            self.place_piece(coord, turn)
            turn += 1
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
