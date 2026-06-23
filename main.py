from boards import Board
import effects
from fractal_tilling import Fractal
# import generators
from models import Action, Direction, Rotation
import pieces

# WIDTH = 1440
# HEIGHT = 1920


def main() -> None:
    fractal = Fractal([Direction.RIGHT], [Action.PASTE, Rotation.ONCE, Action.PASTE])
    for level in range(20):
        generator_builder = effects.apply_effects(
            fractal.build_generator(level),
            effects.normal_effect(),
        )
        size, _ = fractal.get_info(level)
        board = Board(
            size[0],
            size[1],
            [pieces.Knight(1), pieces.Knight(2)],
            generator_builder,
        )
        board.solve()


if __name__ == "__main__":
    main()
