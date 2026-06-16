from boards import Board, Piece
import effects
import generators


WIDTH = 512
HEIGHT = 512
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


def main() -> None:
    generator_builder = effects.apply_effects(
        generators.spiral((HEIGHT//2,WIDTH//2)),
        effects.glitch_swap_effect(0.01),
    )
    board = Board(
        HEIGHT,
        WIDTH,
        [Piece(n, KNIGHT_MOVES) for n in range(1, 3)],
        generator_builder,
    )
    board.solve()


if __name__ == "__main__":
    main()
