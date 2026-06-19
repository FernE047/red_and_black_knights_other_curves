from boards import Board
import effects
import generators
import pieces

WIDTH = 1000
HEIGHT = 1000


def main() -> None:
    generator_builder = effects.apply_effects(
        generators.gilbert(),
        effects.center_out_effect(),
    )
    board = Board(
        HEIGHT,
        WIDTH,
        [pieces.Knight(1), pieces.Knight(2)],
        generator_builder,
    )
    board.solve()


if __name__ == "__main__":
    main()
