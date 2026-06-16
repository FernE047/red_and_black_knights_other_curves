from boards import Board, Piece
import effects
import generators


WIDTH = 1000
HEIGHT = 1000
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
    for size in range(1,1000):
        generator_builder = effects.apply_effects(
            generators.spiral((size//2, size//2)),
            effects.normal_effect(),
        )
        board = Board(
            size,
            size,
            [Piece(n, KNIGHT_MOVES) for n in range(1, 3)],
            generator_builder,
        )
        board.solve()


if __name__ == "__main__":
    main()
