from boards import Board
import effects
import generators
import pieces

WIDTH = 200
HEIGHT = 200


def main() -> None:
    generator_builder = effects.apply_effects(
        generators.gilbert(),
        effects.normal_effect(),
    )
    board = Board(
        HEIGHT,
        WIDTH,
        [pieces.Queen(1), pieces.Knight(2)],
        generator_builder,
    )
    board.solve()


if __name__ == "__main__":
    main()
