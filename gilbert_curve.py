# Based on work by Jakub Červený
# BSD-2-Clause License
# Copyright (c) 2018 Jakub Červený


from typing import Generator


def gilbert_xy_generator(w: int, h: int) -> Generator[tuple[int, int], None, None]:
    if w >= h:
        yield from gilbert_xy_r(0, 0, w, 0, 0, h)
    else:
        yield from gilbert_xy_r(0, 0, 0, h, w, 0)


def gilbert_xy_r(
    x: int, y: int, ax: int, ay: int, bx: int, by: int
) -> Generator[tuple[int, int], None, None]:
    w = abs(ax + ay)
    h = abs(bx + by)

    (dax, day) = (
        -1 if ax < 0 else (1 if ax > 0 else 0),
        -1 if ay < 0 else (1 if ay > 0 else 0),
    )
    (dbx, dby) = (
        -1 if bx < 0 else (1 if bx > 0 else 0),
        -1 if by < 0 else (1 if by > 0 else 0),
    )

    if h == 1:
        for i in range(w):
            yield (x + dax * i, y + day * i)
        return

    if w == 1:
        for i in range(h):
            yield (x + dbx * i, y + dby * i)
        return

    ax2, ay2 = ax // 2, ay // 2
    bx2, by2 = bx // 2, by // 2

    w2 = abs(ax2 + ay2)
    h2 = abs(bx2 + by2)

    if 2 * w > 3 * h:
        if (w2 % 2) and (w > 2):
            ax2, ay2 = ax2 + dax, ay2 + day

        yield from gilbert_xy_r(x, y, ax2, ay2, bx, by)
        yield from gilbert_xy_r(x + ax2, y + ay2, ax - ax2, ay - ay2, bx, by)
        return

    if (h2 % 2) and (h > 2):
        bx2, by2 = bx2 + dbx, by2 + dby

    yield from gilbert_xy_r(x, y, bx2, by2, ax2, ay2)
    yield from gilbert_xy_r(x + bx2, y + by2, ax, ay, bx - bx2, by - by2)
    yield from gilbert_xy_r(
        x + (ax - dax) + (bx2 - dbx),
        y + (ay - day) + (by2 - dby),
        -bx2,
        -by2,
        -(ax - ax2),
        -(ay - ay2),
    )