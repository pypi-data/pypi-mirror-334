def size() -> tuple[int, int]:
    return (0, 0)


def color(x: int, y: int) -> int:
    return 0


def is_color(colors: list[tuple[int, int, int]], precision: float = 1.0) -> bool:
    return True


def find_color(
    color: int,
    offset: list[tuple[int, int, int]] = [],
    precision: float = 1.0,
    region: tuple[int, int, int, int] = (0, 0, -1, -1),
    max_miss: int = 0,
    all: bool = False,
) -> list[tuple[int, int]]:
    return [(-1, -1)]


def find_image(
    path: str,
    ignore: list[int] = [],
    precision: float = 1.0,
    region: tuple[int, int, int, int] = (0, 0, -1, -1),
    max_miss: int = 0,
    all: bool = False,
) -> list[tuple[int, int]]:
    return [(-1, -1)]


def snapshot(
    path: str, region: tuple[int, int, int, int] = (0, 0, -1, -1), scale: float = 1.0
) -> None:
    pass
