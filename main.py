from boards import Board
import effects
import generators
import pieces

WIDTH = 100
HEIGHT = 100


def main() -> None:
    generator_builder = effects.apply_effects(
        generators.spiral((HEIGHT // 2, WIDTH // 2)),
        effects.normal_effect(),
    )
    board = Board(
        HEIGHT,
        WIDTH,
        [pieces.Knight(1) + pieces.Bishop(1), pieces.Knight(2) + pieces.Bishop(2)],
        generator_builder,
    )
    board.solve()


if __name__ == "__main__":
    main()
