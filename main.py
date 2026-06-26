from boards import Board
import effects
from fractal_tilling import hilbert_self_replicator
# import generators
import pieces

# WIDTH = 1440
# HEIGHT = 1920


def main() -> None:
    fractal = hilbert_self_replicator(
        "dr,dd,dr,rr,ll,ul,uu,ur,rr,rr,"
        "dr,dd,dr,rr,ur,uu,ul,ll,rr,dr,ur,"
        "dr,dd,dr,ur,uu,uu,dd,dd,dr,ur,uu,ur,"
        "rr,dr,dd,uu,ur,rr,dr,dr,dd,dd,dd,dl,ul,uu,uu,uu,ur,ur,rr,dr,dd,dr,rr,ur,uu,ul,ll,rr,dr,ur"
    )
    for level in range(8):
        generator_builder = effects.apply_effects(
            fractal.build_generator(level),
            effects.normal_effect()
        )
        size, _ = fractal.get_info(level)
        board = Board(
            size[0],
            size[1],
            [pieces.Knight(1), pieces.Knight(2)],
            generator_builder,
        )
        board.solve()


if __name__ == "__main__":
    main()
