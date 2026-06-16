from typing import Iterator


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
        n = 0
        while True:
            for move in self.rule_moves:
                y, x = move
                yield (y * n, x * n)
            n += 1


def Knight(team: int) -> Piece:
    return Piece(
        team,
        (
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