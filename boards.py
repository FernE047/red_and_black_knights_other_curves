from pathlib import Path
from pieces import Piece
from typing import TYPE_CHECKING
from generators import GeneratorRecipe, safe_next

if TYPE_CHECKING:
    from PIL import Image

SAVE_FOLDER = Path("./out")
DEBUG_FOLDER = Path("./debug")
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


class Board:
    def __init__(
        self,
        height: int,
        width: int,
        piece_orders: list[Piece],
        generator_recipe: GeneratorRecipe,
        is_debug: bool = False,
    ) -> None:
        self.height = height
        self.width = width
        self.piece_orders = piece_orders
        self.colours_amount = max([p.value for p in piece_orders])
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.ordered_cells: list[CoordData] = []
        self.generators = [
            generator_recipe(height, width) for _ in range(self.colours_amount)
        ]
        self.is_debug = is_debug

    def is_inside(self, y: int, x: int) -> bool:
        return 0 <= y < self.height and 0 <= x < self.width

    def is_coord_safe(self, coord: CoordData, piece: Piece) -> bool:
        y, x = coord
        consecutive_fails = 0
        for dy, dx in piece.get_moves():
            ay = y + dy
            ax = x + dx
            if not self.is_inside(ay, ax):
                consecutive_fails += 1
                if consecutive_fails >= len(piece.rule_moves):
                    break
                continue
            cell = self.board[ay][ax]
            if cell and cell != piece.value:
                return False
            consecutive_fails = 0
        return True

    def solve(self) -> None:
        turn = 0
        while True:
            piece = self.piece_orders[turn]
            generator = self.generators[piece.value - 1]
            coord = safe_next(generator)
            self.save_debug(coord, piece)
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
        self.save()

    def save(self) -> None:
        img = self.render()
        self.save_file(img, SAVE_FOLDER)

    def save_debug(self, coord: CoordData | None, piece_lol: Piece) -> None:
        if not self.is_debug:
            return
        if coord is None:
            return
        img = self.render()
        y, x = coord
        img.putpixel((x, y), TEAM_COLORS[piece_lol.value - 1])
        self.save_file(img, DEBUG_FOLDER)

    def save_file(self, img: Image.Image, folder: Path) -> None:
        file_amount = sum(1 for item in folder.iterdir() if item.is_file())
        output_image = folder / f"output_{file_amount}.png"
        img.save(output_image)

    def render(self) -> Image.Image:
        from PIL import Image

        img = Image.new("RGBA", (self.width, self.height), BACKGROUND_COLOR)
        for y in range(self.height):
            for x in range(self.width):
                piece = self.board[y][x]
                if piece == 0:
                    continue
                img.putpixel((x, y), TEAM_COLORS[piece - 1])
        return img
