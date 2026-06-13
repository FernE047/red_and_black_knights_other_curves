from boards import Board, ChoiceOptions, Piece


WIDTH = 250
HEIGHT = 250
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
    for _ in range(10):
        board = Board(
            HEIGHT,
            WIDTH,
            [Piece(n, KNIGHT_MOVES) for n in range(1, 3)],
            ChoiceOptions.RANDOM,
        )
        board.solve()


if __name__ == "__main__":
    main()
