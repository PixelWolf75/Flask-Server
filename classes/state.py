import random
from random import randint

from classes.client import Client
from classes.fruit import Fruit, Pos
from classes.snake import Snake, SnakeItem, Direction

ClientSocketIDType: type = str


class GameState:
    room_name: str
    client_map: dict[ClientSocketIDType, Client]
    snake_map: dict[ClientSocketIDType, Snake]
    fruit: Fruit | None
    score: int
    map_size: tuple[int, int]

    def __init__(self, room_name: str):
        self.room_name = room_name
        self.client_map = {}
        self.snake_map = {}
        self.fruit = None
        self.score = 0
        self.map_size = (20, 20)

    def add_client(self, sid: ClientSocketIDType):
        """
        Adds a client to the client list.

        :param sid: The identifier for the client.
        :type sid: str
        :return: None
        """
        self.client_map[sid] = Client(sid)
        # TODO:  pass map details to game state
        #for snake in self.snake_map.values():
            #snake.body_items.clear()
            #x = random.randint(0, self.map_size[0] - 1)
            #y = random.randint(0, self.map_size[1] - 1)
            #snake.body_items.append(SnakeItem(Pos(x=x, y=y)))
            #snake.is_alive = True
            #snake.direction = Direction.RIGHT if x < self.map_size[0] / 2 else Direction.LEFT

        x = random.randint(0, self.map_size[0] - 1)
        y = random.randint(0, self.map_size[1] - 1)
        self.snake_map.setdefault(sid, Snake(self.client_map[sid], SnakeItem(Pos(x=x, y=y))))

    def remove_client(self, sid: ClientSocketIDType):
        """
        Adds a client to the client list.
    
        :param sid: The identifier for the client.
        :type sid: str
        :return: None
        """
        del self.client_map[sid]
        del self.snake_map[sid]

    def move_snake(self, sid: ClientSocketIDType, direction: str):
        if direction == Direction.NA.value:
            return
        self.snake_map[sid].direction = Direction(direction)

    def update_game_state(self):
        """
        Updates the game state.

        :return: None
        """
        if not self.fruit:
            # create a new fruit
            self.fruit = Fruit(Pos(x=randint(0, self.map_size[0]-1),
                                   y=randint(0, self.map_size[1]-1)))

        for snake in self.snake_map.values():
            if not snake.is_alive:
                continue
            snake.move()

            # todo: check for snake touching fruit
            if self.fruit:
                if snake.body_items[0].position == self.fruit.position:
                    # snake ate the fruit
                    snake.grow()
                    self.score += 1
                    self.fruit = None
                    continue

            # if snake.check_if_overlapped(snake.body_items[0].position, include_head=False):
            #     snake.is_alive = False
            #     continue
            for other_snake in self.snake_map.values():
                is_head = snake != other_snake
                if other_snake.check_if_overlapped(snake.body_items[0].position, include_head=is_head):
                    snake.is_alive = False
                    break
