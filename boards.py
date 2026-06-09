from pathlib import Path
from typing import Iterator
from generators import build_generator, ChoiceOptions, safe_next

SAVE_FOLDER = Path("./out")
BACKGROUND_COLOR = (255, 255, 255, 255)
TEAM_COLORS = [
    (0, 0, 0, 255),
    (255, 0, 0, 255),
    (0, 255, 0, 255),
    (0, 0, 255, 255),
    (255, 255, 0, 255),
    (0, 255, 255, 255),
    (255, 0, 255, 255),
    (255, 128, 0, 255),
]

CoordData = tuple[int, int]


class Piece:
    def __init__(self, value: int, moves: tuple[tuple[int, int], ...]) -> None:
        self.value = value
        self.moves = moves


class Board:
    def __init__(
        self, height: int, width: int, piece_orders: list[Piece], choice: ChoiceOptions
    ) -> None:
        self.height = height
        self.width = width
        self.cell_amount = height * width
        self.piece_orders = piece_orders
        self.colours_amount = max([p.value for p in piece_orders])
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.ordered_cells: list[CoordData] = []
        self.choice = choice
        self.generators: list[Iterator[CoordData]] = [
            build_generator(self) for _ in range(self.colours_amount)
        ]

    def is_inside(self, y: int, x: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def is_coord_safe(self, coord: CoordData, piece: Piece) -> bool:
        y, x = coord
        for dy, dx in piece.moves:
            ay = y + dy
            ax = x + dx
            if not self.is_inside(ay, ax):
                continue
            cell = self.board[ay][ax]
            if cell and cell != piece:
                return False
        return True

    def solve(self) -> None:
        turn = 0
        while True:
            piece = self.piece_orders[turn]
            generator = self.generators[piece.value - 1]
            coord = safe_next(generator)
            self.render_debug(coord, piece)
            if not coord:
                break
            y, x = coord
            cell = self.board[y][x]
            if cell != 0 or not self.is_coord_safe(coord, piece):
                continue
            self.board[y][x] = piece.value
            turn += 1
            if turn >= len(self.piece_orders):
                turn = 0
        self.render()

    def render(self) -> None:
        from PIL import Image

        img = Image.new("RGBA", (self.width, self.height), BACKGROUND_COLOR)
        for y in range(self.height):
            for x in range(self.width):
                piece = self.board[y][x]
                if piece == 0:
                    continue
                img.putpixel((x, y), TEAM_COLORS[piece - 1])
        file_amount = sum(1 for item in SAVE_FOLDER.iterdir() if item.is_file())
        output_image = SAVE_FOLDER / f"output_{file_amount}.png"
        img.save(output_image)

    def render_debug(self, coord: CoordData | None, piece_lol: Piece) -> None:
        from PIL import Image

        if coord is None:
            return

        img = Image.new("RGBA", (self.width, self.height), BACKGROUND_COLOR)
        for y in range(self.height):
            for x in range(self.width):
                piece = self.board[y][x]
                if piece == 0:
                    continue
                img.putpixel((x, y), TEAM_COLORS[piece - 1])
        y, x = coord
        img.putpixel((x, y), TEAM_COLORS[piece - 1])
        file_amount = sum(1 for item in SAVE_FOLDER.iterdir() if item.is_file())
        output_image = SAVE_FOLDER / f"output_{file_amount}.png"
        img.save(output_image)
