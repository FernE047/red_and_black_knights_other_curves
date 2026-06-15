from boards import Board, Piece
import effects
import generators


WIDTH = 256
HEIGHT = 256
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
TRI_KNIGHT_MOVES = (
    (-3, -1),
    (-3, 1),
    (-1, -3),
    (-1, 3),
    (1, -3),
    (1, 3),
    (3, -1),
    (3, 1),
)


def main() -> None:
    generator_builder = effects.apply_effects(
        generators.gilbert(),
        effects.normal_effect(),
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
