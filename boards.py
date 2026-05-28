from pathlib import Path
from typing import Literal

SAVE_FOLDER = Path("./out")

ChoiceOptions = Literal["Simple"]
ColourData = tuple[int, int, int, int]
CoordData = tuple[int, int]


class Cell:
    def __init__(self) -> None:
        self.value = 0
        self.occupied_by = 0
        self.attacked_by: set[int] = set()

    def set_value(self, n: int) -> None:
        self.value = n

    def get_value(self) -> int:
        return self.value

    def set_piece(self, piece: int) -> None:
        self.occupied_by = piece

    def get_piece(self) -> int:
        return self.occupied_by

    def attack(self, piece: int) -> None:
        self.attacked_by.add(piece)

    def is_safe_to(self, piece: int) -> bool:
        if self.occupied_by:
            return False
        if not self.attacked_by:
            return True
        if len(self.attacked_by) > 1:
            return False
        if piece in self.attacked_by:
            return True
        return False


BoardData = list[list[Cell]]


class Board:
    def __init__(
        self, height: int, width: int, colours_amount: int, choice: ChoiceOptions | None
    ) -> None:
        self.height = height
        self.width = width
        self.colours_amount = colours_amount
        self.board = [[Cell() for _ in range(width)] for _ in range(height)]
        self.choice = choice  # used later to render
        self.build_place_board()

    def fill_simple_board(self) -> None:
        n = 0
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x].set_value(n)
                n += 1

    def build_place_board(self) -> None:
        if self.choice == "Simple":
            return self.fill_simple_board()
        raise NotImplementedError("choose a valid option")

    def get_cell(self, coord: CoordData) -> Cell:
        y, x = coord
        return self.board[y][x]

    def find_safe_lowest_place(self, turn: int) -> CoordData:
        piece = turn + 1
        lowest_coord = (-1, -1)
        lowest_value: float | int = float("inf")
        for y in range(self.height):
            for x in range(self.width):
                coord = (y, x)
                cell = self.get_cell(coord)
                if not cell.is_safe_to(piece):
                    continue
                if cell.value > lowest_value:
                    continue
                lowest_coord = coord
                lowest_value = cell.value
        return lowest_coord

    def place_attack(self, coord: CoordData, piece: int) -> None:
        y, x = coord
        if y < 0:
            return
        if y >= self.height:
            return
        if x < 0:
            return
        if x >= self.width:
            return
        self.get_cell((y, x)).attack(piece)

    def place_attacks(self, coord: CoordData, piece: int) -> None:
        y, x = coord
        self.place_attack((y - 2, x - 1), piece)
        self.place_attack((y - 2, x + 1), piece)
        self.place_attack((y - 1, x - 2), piece)
        self.place_attack((y - 1, x + 2), piece)
        self.place_attack((y + 1, x - 2), piece)
        self.place_attack((y + 1, x + 2), piece)
        self.place_attack((y + 2, x - 1), piece)
        self.place_attack((y + 2, x + 1), piece)

    def place_piece(self, coord: CoordData, turn: int) -> None:
        piece = turn + 1
        cell = self.get_cell(coord)
        cell.set_piece(piece)
        self.place_attacks(coord, piece)

    def solve(self, colours: list[ColourData], background_color: ColourData) -> None:
        turn = 0
        while True:
            coord = self.find_safe_lowest_place(turn)
            if coord == (-1, -1):
                break
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
                cell = self.get_cell((y, x))
                piece = cell.get_piece()
                if piece == 0:
                    continue
                img.putpixel((x, y), colours[piece - 1])
        file_amount = sum(1 for item in SAVE_FOLDER.iterdir() if item.is_file())
        output_image = SAVE_FOLDER / f"output_{file_amount}.png"
        img.save(output_image)
