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
COLOURS_AMOUNT = 2

turn = 0
board = Board(HEIGHT, WIDTH, COLOURS_AMOUNT, ChoiceOptions.SPIRAL_DIAGONAL_2)
board.solve(TEAM_COLORS, BACKGROUND_COLOR)
