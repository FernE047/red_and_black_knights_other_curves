import random
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

SIZE_LIMIT = 2500
UP = Direction.UP
UPRIGHT = Direction.UPRIGHT
RIGHT = Direction.RIGHT
DOWNRIGHT = Direction.DOWNRIGHT
DOWN = Direction.DOWN
DOWNLEFT = Direction.DOWNLEFT
LEFT = Direction.LEFT
UPLEFT = Direction.UPLEFT
PASTE = Action.PASTE
RONCE = Rotation.ONCE
RWICE = Rotation.TWICE
RHICE = Rotation.THRICE
REVERSE = Action.REVERSE
HORIZONTAL = Reflection.HORIZONTAL
VERTICAL = Reflection.VERTICAL

ROTATIONS_DICT = {
    RONCE: {
        UP: RIGHT,
        UPRIGHT: DOWNRIGHT,
        RIGHT: DOWN,
        DOWNRIGHT: DOWNLEFT,
        DOWN: LEFT,
        DOWNLEFT: UPLEFT,
        LEFT: UP,
        UPLEFT: UPRIGHT,
    },
    RWICE: {
        UP: DOWN,
        UPRIGHT: DOWNLEFT,
        RIGHT: LEFT,
        DOWNRIGHT: UPLEFT,
        DOWN: UP,
        DOWNLEFT: UPRIGHT,
        LEFT: RIGHT,
        UPLEFT: DOWNRIGHT,
    },
    RHICE: {
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
    VERTICAL: {
        UP: DOWN,
        UPRIGHT: DOWNRIGHT,
        RIGHT: RIGHT,
        DOWNRIGHT: UPRIGHT,
        DOWN: UP,
        DOWNLEFT: UPLEFT,
        LEFT: LEFT,
        UPLEFT: DOWNLEFT,
    },
    HORIZONTAL: {
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


translation_dict: dict[str, Direction | Rotation | Reflection | Action] = {
    "uu": UP,
    "ur": UPRIGHT,
    "rr": RIGHT,
    "dr": DOWNRIGHT,
    "dd": DOWN,
    "dl": DOWNLEFT,
    "ll": LEFT,
    "ul": UPLEFT,
    "r1": RONCE,
    "r2": RWICE,
    "r3": RHICE,
    "mh": HORIZONTAL,
    "mv": VERTICAL,
    "mm": Reflection.MAIN_DIAGONAL,
    "ma": Reflection.ANTI_DIAGONAL,
    "pp": PASTE,
    "rv": REVERSE,
}


def translate_path(path: PathData | str) -> PathData:
    if not isinstance(path, str):
        return path
    new_path: PathData = []
    for segment in path.lower().split(","):
        new_path.append(translation_dict[segment])  # type:ignore
    return new_path


def translate_procedure(procedure: Procedure | str) -> Procedure:
    if not isinstance(procedure, str):
        return procedure
    new_procedure: Procedure = []
    for segment in procedure.lower().split(","):
        new_procedure.append(translation_dict[segment])
    return new_procedure


class Fractal:
    def __init__(
        self, building_block: PathData | str, procedure: Procedure | str
    ) -> None:
        self.procedure = translate_procedure(procedure)
        self.levels = [translate_path(building_block)]

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
        if (
            height * width >= SIZE_LIMIT * SIZE_LIMIT
            or max((height, width)) > 2 * SIZE_LIMIT
        ):
            raise ValueError(
                f"Oops! O fractal ficou gigante demais, amada ({height}x{width}). "
                f"Tamanho máximo permitido é {SIZE_LIMIT}X{SIZE_LIMIT}! 🛑🎀"
            )
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


def custom_hilbert(starting_block: PathData|str) -> Fractal:
    return Fractal(starting_block, "MA,PP,DD,PP,RR,PP,UU,MM,PP")


def hilbert_curve() -> Fractal:
    return custom_hilbert([DOWN, RIGHT, UP])  # "DD,RR,UU"


def wilbert_curve() -> Fractal:
    return custom_hilbert([DOWNRIGHT, LEFT, UPRIGHT])  # "DR,LL,UR"


def dragon_curve() -> Fractal:
    return Fractal([RIGHT], [PASTE, REVERSE, RONCE, PASTE])  # "RR", "PP,RV,R1,PP"


def custom_peano(starting_block: PathData | str) -> Fractal:
    return Fractal(
        starting_block,
        "PP,DD,MH,PP,DD,PP,RR,MV,PP,UU,MV,MH,PP,UU,MV,PP,RR,PP,DD,MH,PP,DD,PP",
    )


def peano_curve() -> Fractal:
    return custom_peano("DD,DD,RR,UU,UU,RR,DD,DD")


def simpler_peano() -> Fractal:
    return custom_peano([DOWN, UPRIGHT, DOWN])  # "DD,UR,DD"


def minkowski_curve() -> Fractal:
    return Fractal(
        [RIGHT], [PASTE, RHICE, PASTE, PASTE, RONCE, PASTE, PASTE]
    )  # "RR", "PP,R2,PP,PP,R1,PP,PP"


def hilbert_self_replicator(building_block: PathData | str) -> Fractal:
    before_path = translate_path(building_block)
    path: PathData = []
    for direction in before_path:
        if direction in (RIGHT,DOWN,LEFT,UP):
            path.append(direction)
            continue
        if direction == UPRIGHT:
            path.extend([UP,RIGHT])
            continue
        if direction == UPLEFT:
            path.extend([UP, LEFT])
            continue
        if direction == DOWNRIGHT:
            path.extend([DOWN, RIGHT])
            continue
        if direction == DOWNLEFT:
            path.extend([DOWN, LEFT])
            continue
    direction_procedures: dict[Direction, Procedure] = {
        RIGHT: [PASTE],
        DOWN: [RONCE, HORIZONTAL, PASTE],
        LEFT: [RWICE, PASTE],
        UP: [RONCE, VERTICAL, PASTE],
    }
    procedure: Procedure = []
    procedure.extend(direction_procedures[path[0]])
    for index in range(len(path) - 1):
        current_direction = path[index]
        next_direction = path[index + 1]
        procedure.append(current_direction)
        if current_direction == next_direction:
            procedure.extend(direction_procedures[current_direction])
            continue
        transition = (current_direction, next_direction)
        if transition == (RIGHT, DOWN):
            procedure.extend(direction_procedures[DOWN])
            continue
        if transition == (RIGHT, UP):
            procedure.extend(direction_procedures[RIGHT])
            continue
        if transition == (LEFT, DOWN):
            procedure.extend(direction_procedures[LEFT])
            continue
        if transition == (LEFT, UP):
            procedure.extend(direction_procedures[UP])
            continue
        if transition == (DOWN, RIGHT):
            procedure.extend(direction_procedures[RIGHT])
            continue
        if transition == (DOWN, LEFT):
            procedure.extend(direction_procedures[DOWN])
            continue
        if transition == (UP, RIGHT):
            procedure.extend(direction_procedures[UP])
            continue
        if transition == (UP, LEFT):
            procedure.extend(direction_procedures[LEFT])
            continue
    procedure.append(path[-1])
    procedure.extend(direction_procedures[path[-1]])
    return Fractal(path, procedure)


def hilbert_like(variation: int) -> Fractal:
    if variation == 1:
        return hilbert_self_replicator("RR,RR,DD,LL,LL,DD,DD,RR,UU,RR,DD,RR,UU,UU,UU")
    if variation == 2:
        return hilbert_self_replicator("DD,DD,DD,RR,UU,UU,UU,RR,DD,DD,DD,RR,UU,UU,UU")
    if variation == 3:
        return hilbert_self_replicator("DD,RR,UU,RR,DD,DD,LL,LL,DD,RR,RR,RR,UU,UU,UU")
    if variation == 4:
        return hilbert_self_replicator("RR,RR,DD,DD,LL,UU,LL,DD,DD,RR,RR,RR,UU,UU,UU")
    return hilbert_self_replicator("RR,DD,LL,DD,RR,RR,UU,UU")

INVALID_PAIRS = {
    ("uu", "dd"),
    ("dd", "uu"),
    ("rr", "ll"),
    ("ll", "rr"),
    ("ur", "dl"),
    ("dl", "ur"),
    ("ul", "dr"),
    ("dr", "ul"),
    ("r1", "r3"),
    ("r3", "r1"),
    ("r2", "r2"),
    ("mh", "mh"),
    ("mv", "mv"),
    ("rv", "rv"),
}


def get_inverse(item: str) -> str | None:
    """Retorna a operação inversa/anuladora de um item, se existir."""
    for pair in INVALID_PAIRS:
        if pair[0] == item and pair[0] != pair[1]:  # Para pares distintos
            return pair[1]
        elif pair[0] == item and pair[0] == pair[1]:  # Para pares iguais (ex: r2)
            return item
    return None


def get_valid_sequence(pool: list[str], length: int) -> list[str]:
    sequence: list[str] = []
    current_block: list[str] = []

    for _ in range(length - 1):
        available_pool = set(pool)
        for existing_item in current_block:
            invalid_item = get_inverse(existing_item)
            if invalid_item and invalid_item in available_pool:
                available_pool.remove(invalid_item)
        if not available_pool:
            available_pool = set(pool)
        next_item = random.choice(list(available_pool))
        if next_item == "pp":
            current_block.clear()
        else:
            current_block.append(next_item)
        sequence.append(next_item)
    if "pp" in pool:
        sequence.append("pp")
    else:
        sequence.append(random.choice(pool))
    return sequence


procedure_keys = [
    "uu",
    "ur",
    "rr",
    "dr",
    "dd",
    "dl",
    "ll",
    "ul",
    "r1",
    "r2",
    "r3",
    "mh",
    "mv",
    "pp",
    "rv",
]
path_keys = ["uu", "ur", "rr", "dr", "dd", "dl", "ll", "ul"]


def create_random_fractal(procedure_length: int, path_length: int) -> "Fractal":
    random_procedure = get_valid_sequence(procedure_keys, procedure_length)
    random_path = [random.choice(path_keys) for _ in range(path_length)]
    procedure_str = ",".join(random_procedure)
    building_block_str = ",".join(random_path)
    print(procedure_str)
    print(building_block_str)
    return Fractal(building_block=building_block_str, procedure=procedure_str)
