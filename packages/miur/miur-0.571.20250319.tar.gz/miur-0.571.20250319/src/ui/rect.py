from typing import Iterator, override


# ALT:SEE: /usr/lib/python3.12/site-packages/Onboard/utils.py:425
class Rect:
    __slots__ = ("w", "h", "x", "y")

    def __init__(self, w: int = 0, h: int = 0, *, x: int = 0, y: int = 0) -> None:
        assert w > 0 and h > 0 and x >= 0 and y >= 0, "TEMP: incompatible with curses"
        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def __iter__(self) -> Iterator[int]:
        yield self.w
        yield self.h
        yield self.x
        yield self.y

    @property
    def xw(self) -> int:
        return self.x + self.w

    @property
    def yh(self) -> int:
        return self.y + self.h

    @override
    def __str__(self) -> str:
        return f"[{self.w}x{self.h}+{self.x}+{self.y}]"

    @override
    def __repr__(self) -> str:
        clsnm = self.__class__.__name__
        return f"{clsnm}(w={self.w}, h={self.h}, x={self.x}, y={self.y})"
