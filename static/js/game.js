
class Fruit {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    static build(item) {
        return (item) ? new Fruit(item.x, item.y) : null;
    }
}


class BodyItem {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    static build(item) {
        return new BodyItem(item.x, item.y);
    }
}

class Snake {

    constructor(name, sid, is_alive, direction, body_item_list) {
        this.name = name;
        this.sid = sid;
        this.is_alive = is_alive;
        this.direction = direction;
        this.body_item_list = /** @type {BodyItem[]} */body_item_list;

    }

    /**
     * Constructs a new Snake object based on the provided data.
     *
     * @param {Object} x - The raw data for the snake.
     * @param {string} x.sid - Client ID.
     * @param {string} x.name - The name of the snake.
     * @param {boolean} x.is_alive - Indicates if the snake is alive.
     * @param {string} x.direction - The current direction of the snake.
     * @param {Array<Object>} x.body_item_list - The list of body items for the snake.
     * @param {string} x.body_item_list[].name - The name of the body item.
     * @param {number} x.body_item_list[].size - The size of the body item.
     * @param {string} x.body_item_list[].color - The color of the body item.
     *
     * @return {Snake} The constructed Snake object.
     */
    static build(x) {
        return new Snake(x.name, x.sid, x.is_alive, x.direction, x.body_item_list.map(x => BodyItem.build(x)));
    }
}

class GameState {
    constructor(snake_list, fruit, score) {
        this.snake_list = /** @type {Snake[]} */snake_list.map(x => Snake.build(x));
        this.fruit = /** @type {Fruit} */Fruit.build(fruit);
        this.score = /** @type {number} */score;
        this.direction = 'NA';
        this.map = new GameMap(20, 20, document.querySelector('#target_canvas'));
    }

    update(snake_list, fruit, score) {
        this.snake_list = /** @type {Snake[]} */snake_list.map(x => Snake.build(x));
        this.fruit = /** @type {Fruit} */Fruit.build(fruit);
        this.score = /** @type {number} */score;
    }
}

let my_client = /** @type {Client | null} */ null;
let game_state = /** @type {GameState|null} */null;

let socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function () {
    console.log('connected:', socket.id);
    my_client = new Client(socket.id)

    //socket.emit('my event', {data: 'I\'m connected!'});
});

socket.on('game_state', (data) => {

    // Render the new state
    if (!game_state)
        game_state = new GameState(data.snake_list, data.fruit, data.score);
    game_state.update(data.snake_list, data.fruit, data.score);
    console.log(game_state.snake_list)
    renderGameState(game_state);
});

socket.on('echor', (dat) => {
    console.log("GOT HERE");
})

function renderGameState(game_state) {
    game_state.map.reset_map();
    game_state.snake_list.forEach(/** @param snake {Snake} */
    (snake, index) => {

        let color = 'green';
        if (snake.sid === my_client.sid) {
            // Current Player
            let pos = snake.body_item_list[0];
            document.querySelector('title').innerHTML = `${pos.x}, ${pos.y} - ${snake.is_alive ? "Alive": "Dead"}`;
            color = 'blue'
        }
        if (!snake.is_alive) {
            return;
        }

        snake.body_item_list.forEach((body_item) => {
            // Code to render each body item
            if (body_item.y < 0 || body_item.y >= game_state.map.height)
                return;
            if (body_item.x < 0 || body_item.x >= game_state.map.width)
                return;
            game_state.map.grid[body_item.y][body_item.x].set_color(color)
        });
    })
    if (game_state.fruit) {
        if (game_state.fruit.y < 0 || game_state.fruit.y >= game_state.map.height)
            throw Error("Fruit Outside map")
        if (game_state.fruit.x < 0 || game_state.fruit.x >= game_state.map.width)
            throw Error("Fruit Outside map")
        game_state.map.grid[game_state.fruit.y][game_state.fruit.x].set_color('red')
    }
    game_state.map.render();
}

window.addEventListener('keydown', (e) => {

    switch (e.key) {
        case "ArrowLeft":
        case "ArrowRight":
        case "ArrowUp":
        case "ArrowDown":
            game_state.direction = e.key.substr(5).toUpperCase();
            break;
    }
    console.log("Arrow Key = ", game_state.direction)

    socket.emit('move_snake', {'direction': game_state.direction});
})