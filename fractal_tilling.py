from models import (
    Action,
    Direction,
    Generator,
    PathData,
    Procedure,
    Reflection,
    Rotation,
)
from generators import apply_direction, GeneratorRecipe

UP = Direction.UP
UPRIGHT = Direction.UPRIGHT
RIGHT = Direction.RIGHT
DOWNRIGHT = Direction.DOWNRIGHT
DOWN = Direction.DOWN
DOWNLEFT = Direction.DOWNLEFT
LEFT = Direction.LEFT
UPLEFT = Direction.UPLEFT
PASTE = Action.PASTE

ROTATIONS_DICT = {
    Rotation.ONCE: {
        UP: RIGHT,
        UPRIGHT: DOWNRIGHT,
        RIGHT: DOWN,
        DOWNRIGHT: DOWNLEFT,
        DOWN: LEFT,
        DOWNLEFT: UPLEFT,
        LEFT: UP,
        UPLEFT: UPRIGHT,
    },
    Rotation.TWICE: {
        UP: DOWN,
        UPRIGHT: DOWNLEFT,
        RIGHT: LEFT,
        DOWNRIGHT: UPLEFT,
        DOWN: UP,
        DOWNLEFT: UPRIGHT,
        LEFT: RIGHT,
        UPLEFT: DOWNRIGHT,
    },
    Rotation.THRICE: {
        UP: LEFT,
        UPRIGHT: UPLEFT,
        RIGHT: UP,
        DOWNRIGHT: UPRIGHT,
        DOWN: RIGHT,
        DOWNLEFT: DOWNRIGHT,
        LEFT: DOWN,
        UPLEFT: DOWNLEFT,
    },
}
REFLECTIONS_DICT = {
    Reflection.VERTICAL: {
        UP: DOWN,
        UPRIGHT: DOWNRIGHT,
        RIGHT: RIGHT,
        DOWNRIGHT: UPRIGHT,
        DOWN: UP,
        DOWNLEFT: UPLEFT,
        LEFT: LEFT,
        UPLEFT: DOWNLEFT,
    },
    Reflection.HORIZONTAL: {
        UP: UP,
        UPRIGHT: UPLEFT,
        RIGHT: LEFT,
        DOWNRIGHT: DOWNLEFT,
        DOWN: DOWN,
        DOWNLEFT: DOWNRIGHT,
        LEFT: RIGHT,
        UPLEFT: UPRIGHT,
    },
    Reflection.MAIN_DIAGONAL: {
        UP: RIGHT,
        UPRIGHT: UPRIGHT,
        RIGHT: UP,
        DOWNRIGHT: UPLEFT,
        DOWN: LEFT,
        DOWNLEFT: DOWNLEFT,
        LEFT: DOWN,
        UPLEFT: DOWNRIGHT,
    },
    Reflection.ANTI_DIAGONAL: {
        UP: LEFT,
        UPRIGHT: DOWNLEFT,
        RIGHT: DOWN,
        DOWNRIGHT: DOWNRIGHT,
        DOWN: RIGHT,
        DOWNLEFT: UPRIGHT,
        LEFT: UP,
        UPLEFT: UPLEFT,
    },
}
REVERSE_DICT = {
    UP: DOWN,
    UPRIGHT: DOWNLEFT,
    RIGHT: LEFT,
    DOWNRIGHT: UPLEFT,
    DOWN: UP,
    DOWNLEFT: UPRIGHT,
    LEFT: RIGHT,
    UPLEFT: DOWNRIGHT,
}


def rotate_path(path_input: PathData, rotation: Rotation) -> PathData:
    rotation_dict = ROTATIONS_DICT[rotation]
    new_path: PathData = []
    for direction in path_input:
        new_path.append(rotation_dict[direction])
    return new_path


def reflect_path(path_input: PathData, reflection: Reflection) -> PathData:
    reflection_dict = REFLECTIONS_DICT[reflection]
    new_path: PathData = []
    for direction in path_input:
        new_path.append(reflection_dict[direction])
    return new_path


def reverse_path(path_input: PathData) -> PathData:
    new_path: PathData = []
    for direction in reversed(path_input):
        new_path.append(REVERSE_DICT[direction])
    return new_path


class Fractal:
    def __init__(self, building_block: PathData, procedure: Procedure) -> None:
        self.procedure = procedure
        self.levels = [building_block]

    def build_level(self, level: int) -> None:
        while len(self.levels) - 1 < level:
            current_block = self.levels[-1]
            new_path: PathData = []
            for action in self.procedure:
                if action == Action.PASTE:
                    new_path.extend(current_block)
                    current_block = self.levels[-1]
                    continue
                if action == Action.REVERSE:
                    current_block = reverse_path(current_block)
                    continue
                if isinstance(action, Rotation):
                    current_block = rotate_path(current_block, action)
                    continue
                if isinstance(action, Reflection):
                    current_block = reflect_path(current_block, action)
                    continue
                new_path.append(action)
            self.levels.append(new_path)

    def get_boundaries(self, level: int) -> tuple[int, int, int, int]:
        self.build_level(level)
        current_position = (0, 0)
        current_path = self.levels[level]
        max_y = 0
        max_x = 0
        min_x = 0
        min_y = 0
        for direction in current_path:
            y, x = apply_direction(current_position, direction)
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            current_position = (y, x)
        return (min_y, max_y, min_x, max_x)

    def get_info(self, level: int) -> tuple[tuple[int, int], tuple[int, int]]:
        self.build_level(level)
        min_y, max_y, min_x, max_x = self.get_boundaries(level)
        width = abs(min_x - max_x) + 1
        height = abs(min_y - max_y) + 1
        start_y = 0
        start_x = 0
        if min_x < 0:
            start_x = -min_x
        if min_y < 0:
            start_y = -min_y
        return ((height, width), (start_y, start_x))

    def build_generator(self, level: int) -> GeneratorRecipe:
        self.build_level(level)
        _, start_position = self.get_info(level)
        path = self.levels[level]

        def generator(_: int, __: int) -> Generator:
            coord = start_position
            yield coord
            for direction in path:
                coord = apply_direction(coord, direction)
                yield coord

        return generator


def custom_hilbert(starting_block: PathData) -> Fractal:
    return Fractal(
        starting_block,
        [
            Reflection.ANTI_DIAGONAL,
            PASTE,
            DOWN,
            PASTE,
            RIGHT,
            PASTE,
            UP,
            Reflection.MAIN_DIAGONAL,
            PASTE,
        ],
    )


def hilbert_curve() -> Fractal:
    return custom_hilbert([DOWN, RIGHT, UP])


def wilbert_curve() -> Fractal:
    return custom_hilbert([DOWNRIGHT, LEFT, UPRIGHT])


def dragon_curve() -> Fractal:
    return Fractal([RIGHT], [PASTE, Action.REVERSE, Rotation.ONCE, PASTE])


def custom_peano(starting_block: PathData) -> Fractal:
    return Fractal(
        starting_block,
        [
            PASTE,
            DOWN,
            Reflection.HORIZONTAL,
            PASTE,
            DOWN,
            PASTE,
            RIGHT,
            Reflection.VERTICAL,
            PASTE,
            UP,
            Reflection.MAIN_DIAGONAL,
            PASTE,
            UP,
            Reflection.VERTICAL,
            PASTE,
            RIGHT,
            PASTE,
            DOWN,
            Reflection.HORIZONTAL,
            PASTE,
            DOWN,
            PASTE,
        ],
    )


def peano_curve() -> Fractal:
    return custom_peano(
        [
            DOWN,
            DOWN,
            RIGHT,
            UP,
            UP,
            RIGHT,
            DOWN,
            DOWN,
        ]
    )


def simpler_peano() -> Fractal:
    return custom_peano([DOWN, UPRIGHT, DOWN])


def minkowski_curve() -> Fractal:
    return Fractal([RIGHT], [
        PASTE,
        Rotation.THRICE,
        PASTE,
        PASTE,
        Rotation.ONCE,
        PASTE,
        PASTE
    ])
