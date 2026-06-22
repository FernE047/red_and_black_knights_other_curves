from boards import Board
import effects
import generators
import pieces

WIDTH = 1440
HEIGHT = 1920


def main() -> None:
    generator_builder = effects.apply_effects(
        generators.image_based(
            "C:\\Users\\Vallen\\Downloads\\722956455_18097342463520866_1968801134722390899_n.jpg"
        ),
        effects.normal_effect(),
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
