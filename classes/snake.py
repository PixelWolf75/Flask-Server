import sys
from enum import Enum
from classes.client import Client
from classes.fruit import Pos


class Direction(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    NA = 'NA'


class SnakeItem:
    position: Pos

    def __init__(self, position: Pos):
        self.position = position

    def __str__(self):
        return f"{self.position}"


class Snake:
    client: Client
    body_items: list[SnakeItem]
    direction: Direction
    is_alive: bool = False
    tail_node: SnakeItem | None

    def __init__(self, client: Client, initial_start: SnakeItem):
        self.client = client
        self.body_items = [initial_start]
        self.direction = Direction.UP
        self.is_alive = True
        self.tail_node = None

    def move(self):
        if self.direction == Direction.NA:
            return
        # Insert new node in the snake
        current_pos: Pos = self.body_items[0].position
        new_node = SnakeItem(Pos(x=current_pos.x, y=current_pos.y))

        if self.direction == Direction.UP:
            new_node.position.y -= 1
        if self.direction == Direction.DOWN:
            new_node.position.y += 1
        if self.direction == Direction.LEFT:
            new_node.position.x -= 1
        if self.direction == Direction.RIGHT:
            new_node.position.x += 1
        self.body_items.insert(0, new_node)
        self.tail_node = self.body_items.pop()

    def grow(self):
        if not self.tail_node:
            print("Trying to grow the snake without a tail :-O", file=sys.stderr)
            return
        self.body_items.append(self.tail_node)
        self.tail_node = None

    def check_if_overlapped(self, target: Pos, include_head=True) -> bool:
        for item in self.body_items[0 if include_head else 1:]:
            if item.position == target:
                return True
        return False
