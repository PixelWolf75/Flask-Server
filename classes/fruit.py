from __future__ import annotations

from pydantic import BaseModel


class Pos(BaseModel):
    x: int
    y: int

    def __eq__(self, other: Pos) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"{self.x},{self.y}"


class Fruit:
    position: Pos

    def __init__(self, position: Pos):
        self.position = position
