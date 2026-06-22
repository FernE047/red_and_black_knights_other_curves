from models import Action, Direction, PathData, Procedure, Reflection, Rotation

rotations_dict = {
    Rotation.ONCE: {
        Direction.UP: Direction.RIGHT,
        Direction.UPRIGHT: Direction.DOWNRIGHT,
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWNRIGHT: Direction.DOWNLEFT,
        Direction.DOWN: Direction.LEFT,
        Direction.DOWNLEFT: Direction.UPLEFT,
        Direction.LEFT: Direction.UP,
        Direction.UPLEFT: Direction.UPRIGHT,
    },
    Rotation.TWICE: {
        Direction.UP: Direction.DOWN,
        Direction.UPRIGHT: Direction.DOWNLEFT,
        Direction.RIGHT: Direction.LEFT,
        Direction.DOWNRIGHT: Direction.UPLEFT,
        Direction.DOWN: Direction.UP,
        Direction.DOWNLEFT: Direction.UPRIGHT,
        Direction.LEFT: Direction.RIGHT,
        Direction.UPLEFT: Direction.DOWNRIGHT,
    },
    Rotation.THRICE: {
        Direction.UP: Direction.LEFT,
        Direction.UPRIGHT: Direction.UPLEFT,
        Direction.RIGHT: Direction.UP,
        Direction.DOWNRIGHT: Direction.UPRIGHT,
        Direction.DOWN: Direction.RIGHT,
        Direction.DOWNLEFT: Direction.DOWNRIGHT,
        Direction.LEFT: Direction.DOWN,
        Direction.UPLEFT: Direction.DOWNLEFT,
    },
}
reflections_dict = {
    Reflection.VERTICAL: {
        Direction.UP: Direction.DOWN,
        Direction.UPRIGHT: Direction.DOWNRIGHT,
        Direction.RIGHT: Direction.RIGHT,
        Direction.DOWNRIGHT: Direction.UPRIGHT,
        Direction.DOWN: Direction.UP,
        Direction.DOWNLEFT: Direction.UPLEFT,
        Direction.LEFT: Direction.LEFT,
        Direction.UPLEFT: Direction.DOWNLEFT,
    },
    Reflection.HORIZONTAL: {
        Direction.UP: Direction.UP,
        Direction.UPRIGHT: Direction.UPLEFT,
        Direction.RIGHT: Direction.LEFT,
        Direction.DOWNRIGHT: Direction.DOWNLEFT,
        Direction.DOWN: Direction.DOWN,
        Direction.DOWNLEFT: Direction.DOWNRIGHT,
        Direction.LEFT: Direction.RIGHT,
        Direction.UPLEFT: Direction.UPRIGHT,
    },
    Reflection.MAIN_DIAGONAL: {
        Direction.UP: Direction.RIGHT,
        Direction.UPRIGHT: Direction.UPRIGHT,
        Direction.RIGHT: Direction.UP,
        Direction.DOWNRIGHT: Direction.UPLEFT,
        Direction.DOWN: Direction.LEFT,
        Direction.DOWNLEFT: Direction.DOWNLEFT,
        Direction.LEFT: Direction.DOWN,
        Direction.UPLEFT: Direction.DOWNRIGHT,
    },
    Reflection.ANTI_DIAGONAL: {
        Direction.UP: Direction.LEFT,
        Direction.UPRIGHT: Direction.DOWNLEFT,
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWNRIGHT: Direction.DOWNRIGHT,
        Direction.DOWN: Direction.RIGHT,
        Direction.DOWNLEFT: Direction.UPRIGHT,
        Direction.LEFT: Direction.UP,
        Direction.UPLEFT: Direction.UPLEFT,
    },
}


def rotate_path(path_input: PathData, rotation: Rotation) -> PathData:
    rotation_dict = rotations_dict[rotation]
    new_path: PathData = []
    for direction in path_input:
        new_path.append(rotation_dict[direction])
    return new_path


def reflect_path(path_input: PathData, reflection: Reflection) -> PathData:
    reflection_dict = reflections_dict[reflection]
    new_path: PathData = []
    for direction in path_input:
        new_path.append(reflection_dict[direction])
    return new_path


class Fractal:
    def __init__(self, building_block: PathData, procedure: Procedure) -> None:
        self.procedure = procedure
        self.levels = [building_block]

    def build_level(self, level: int) -> None:
        if len(self.levels) - 1 >= level:
            return
        while len(self.levels) - 1 >= level:
            current_block = self.levels[-1]
            new_path: PathData = []
            for action in self.procedure:
                if action == Action.PASTE:
                    new_path.extend(current_block)
                    current_block = self.levels[-1]
                    continue
                if isinstance(action, Rotation):
                    current_block = rotate_path(current_block, action)
                    continue
                if isinstance(action, Reflection):
                    current_block = reflect_path(current_block, action)
                    continue
                new_path.append(action)