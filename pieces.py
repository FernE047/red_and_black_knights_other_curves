from typing import Any, Iterator


class Piece:
    rule_moves: tuple[tuple[int, int], ...]
    fixed_moves: tuple[tuple[int, int], ...]

    def __init__(
        self,
        value: int,
        fixed_moves: tuple[tuple[int, int], ...] | None = None,
        rule_moves: tuple[tuple[int, int], ...] | None = None,
    ) -> None:
        self.value = value
        if fixed_moves is None:
            self.fixed_moves = ()
        else:
            self.fixed_moves = fixed_moves
        if rule_moves is None:
            self.rule_moves = ()
        else:
            self.rule_moves = rule_moves

    def get_moves(self) -> Iterator[tuple[int, int]]:
        for move in self.fixed_moves:
            yield move
        if self.rule_moves:
            n = 1
            while True:
                for move in self.rule_moves:
                    y, x = move
                    yield (y * n, x * n)
                n += 1

    def get_opposite_moves(self) -> Iterator[tuple[int, int]]:
        for move in self.get_moves():
            yield (-1 * move[0], -1 * move[1])

    def __add__(self, other: Any) -> "Piece":
        if not isinstance(other, Piece):
            raise NotImplementedError("only pieces can add to pieces")
        fixed_moves = other.fixed_moves + self.fixed_moves
        rule_moves = other.rule_moves + self.rule_moves
        return Piece(self.value, fixed_moves, rule_moves)


def Leaper(team: int, jump_a: int, jump_b: int) -> Piece:
    return Piece(
        team,
        (
            (-jump_a, -jump_b),
            (-jump_a, jump_b),
            (-jump_b, -jump_a),
            (-jump_b, jump_a),
            (jump_b, -jump_a),
            (jump_b, jump_a),
            (jump_a, -jump_b),
            (jump_a, jump_b),
        ),
    )


def Knight(team: int) -> Piece:
    return Leaper(team, 1, 2)


def Camel(team: int) -> Piece:
    return Leaper(team, 1, 3)


def Jump_Knight(team: int) -> Piece:
    return Piece(
        team,
        rule_moves=(
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ),
    )


def Pawn(team: int) -> Piece:
    return Piece(
        team,
        (
            (-1, -1),
            (-1, 1),
        ),
    )


def Black_Pawn(team: int) -> Piece:
    return Piece(
        team,
        (
            (1, -1),
            (1, 1),
        ),
    )


def King(team: int) -> Piece:
    return Piece(
        team,
        (
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ),
    )


def Rook(team: int) -> Piece:
    return Piece(
        team,
        rule_moves=(
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ),
    )


def Bishop(team: int) -> Piece:
    return Piece(
        team,
        rule_moves=(
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ),
    )


def Queen(team: int) -> Piece:
    return Piece(
        team,
        rule_moves=(
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ),
    )


def Crab(team: int) -> Piece:
    return Piece(team, rule_moves=((0, 1), (0, -1)))


def Jump_King(team: int) -> Piece:
    return Piece(
        team,
        (
            (-2, 0),
            (2, 0),
            (0, -2),
            (0, 2),
            (-2, -2),
            (-2, 2),
            (2, -2),
            (2, 2),
        ),
    )


def Bat(team: int) -> Piece:
    return Piece(
        team,
        rule_moves=(
            (-2, 0),
            (2, 0),
            (0, -2),
            (0, 2),
        ),
    )


def Baby_Bat(team: int) -> Piece:
    return Piece(
        team,
        (
            (-2, 0),
            (2, 0),
            (0, -2),
            (0, 2),
        ),
    )


def Sea_Star(team: int, variation: int = 0) -> Piece:
    moves = ((0, 2), (2, 1), (1, -2), (-1, -2), (-2, 1))
    if variation == 1:
        moves = ((0, 2), (-2, 0), (-1, -2), (2, 1), (-2, 2))
    elif variation == 2:
        moves = ((-1, 2), (-2, 0), (-1, -2), (2, -1), (2, 1))
    elif variation == 3:
        moves = ((-1, 2), (-2, 0), (0, -2), (2, -1), (2, 2))
    elif variation == 4:
        moves = ((-1, 2), (-2, -1), (0, -2), (2, -1), (1, 2))
    elif variation == 5:
        moves = ((-2, 2), (-2, -1), (0, -2), (2, 0), (1, 2))
    elif variation == 6:
        moves = ((-2, 1), (-2, -1), (1, -2), (2, 0), (1, 2))
    elif variation == 7:
        moves = ((-2, 1), (-2, -2), (1, -2), (2, 0), (0, 2))
    return Piece(team, moves)
