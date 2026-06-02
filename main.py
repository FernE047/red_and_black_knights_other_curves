from boards import Board, ChoiceOptions


WIDTH = 1000
HEIGHT = 1000
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


def main() -> None:
    board = Board(HEIGHT, WIDTH, 2, ChoiceOptions.SPIRAL_DIAGONAL)
    for a in range(2, 9):
        board.restart(a)
        board.solve(TEAM_COLORS, BACKGROUND_COLOR)


if __name__ == "__main__":
    main()
