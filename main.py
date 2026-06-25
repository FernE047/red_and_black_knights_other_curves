from boards import Board
import effects
from fractal_tilling import hilbert_like
# import generators
import pieces

# WIDTH = 1440
# HEIGHT = 1920


def main() -> None:
    fractal = hilbert_like(1)
    for level in range(8):
        generator_builder = effects.apply_effects(
            fractal.build_generator(level),
            effects.center_out_effect(),
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
