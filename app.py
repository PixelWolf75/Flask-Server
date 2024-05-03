import random
import time
from pathlib import Path
from threading import Thread

from flask import Flask, request, jsonify, send_file, session
from flask import send_from_directory
from pydantic import BaseModel
from flask_socketio import SocketIO, join_room, emit, leave_room

from classes.state import GameState

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

socketio = SocketIO(app)
game_state: GameState = GameState("First")


@socketio.on('connect')
def connect(_auth: any):
    """
    Create a new client for the new connection
    :param _auth:
    :return:
    """
    # noinspection PyUnresolvedReferences
    game_state.add_client(request.sid)
    # In Theory a client connecting should join the Lobby
    # But for now,  join the "Game" room
    join_room("Game")
    socketio.emit('echo', {'hi': 123}, to='Game')


@socketio.on('disconnect')
def disconnect():

    # noinspection PyUnresolvedReferences
    game_state.remove_client(request.sid)
    leave_room("Game")


class MoveSnakeReq(BaseModel):
    direction: str


@socketio.on('move_snake')
def move_snake(data):
    """
    Move the snake based on the received data
    :param data: The data containing the direction of the snake
    :return:
    """
    r = MoveSnakeReq.model_validate(data)
    # CHeck if server knows about the snake being moved.
    if request.sid not in game_state.client_map:
        # Unknown Snake.
        # Recreate it
        game_state.add_client(request.sid)

    # noinspection PyUnresolvedReferences
    game_state.move_snake(request.sid, r.direction)


def game_loop():
    # Game Loop
    # tick every second
    while True:
        # Game logic goes here
        time.sleep(1)
        game_state.update_game_state()
        # Output the state to all clients
        # socketio.emit('echo', {'hi': 456})
        payload = {
            'snake_list': [{
                'sid': snake.client.socket_id,
                'is_alive': snake.is_alive,
                'direction': snake.direction.value,
                'body_item_list': [item.position.__dict__ for item in snake.body_items]
            } for sid, snake in game_state.snake_map.items()],
            'fruit': game_state.fruit.position.__dict__ if game_state.fruit else None,
            'score': game_state.score
        }
        socketio.emit('game_state', payload, to="Game")


game_loop_thread = Thread(target=game_loop)
game_loop_thread.name = "GameLoop"
game_loop_thread.start()


def background_thread():
    while True:
        socketio.emit('message', {'goodbye': "Goodbye"})
        time.sleep(5)

    # global num_player
    # socketio.emit('gameStart', {'ID': num_player})
    # num_player = num_player + 1
    # global thread
    # if thread is None:
    #    thread = socketio.start_background_task(target=background_thread)
    print(f"New Player Connected with ID: {request.sid}")


@socketio.on('joined')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    # Add client to client list

    game_state.add_client(request.sid)

    room = session.get('room')
    join_room(room)

    # emit to the first client that joined the room
    socketio.emit('status', {
        'msg':  session.get('name') + ' has entered the room'
    }, to="Game")
    # emit('status', {'msg': session.get('name') + ' has entered the room.'}, room='Game')


@app.route('/')
def hello_world():  # put application's code here
    return send_file((Path(__file__).parent / 'static' / 'index.html').as_posix())


@app.route('/s/<path:path>')
def send_report(path):
    # return 'Hello A!'
    return send_from_directory('C:\\Users\\sonic\\PycharmProjects\\Canvas', path)


# Least priority
@app.route('/api/<tag>/<test>', methods=['GET', 'POST'])
def do_test(tag, test):
    if request.method == "GET":
        return jsonify("testGet")
    if request.method == "POST":
        print(request.json["test"])
        return jsonify("testPost")


# Second Highest
@app.route('/api/<test>/check', methods=['GET', 'POST'])
def do_specificB(test):
    try:
        if request.method == "GET":
            return jsonify("testSpecificBGet")
        if request.method == "POST":
            print(request.json["test"])
            return jsonify("testSpecificBPost")
    except:
        return "$H!T H@PP3N3D L0LZ"


# Highest priority
@app.route('/api/eric/<test>', methods=['GET', 'POST'])
def do_specific(test):
    try:
        if request.method == "GET":
            return jsonify("testSpecificGet")
        if request.method == "POST":
            print(request.json["test"])
            return jsonify("testSpecificPost")
    except:
        return "$H!T H@PP3N3D L0LZ"


client_count = -1
fruitX = random.randint(0, 19)
fruitY = random.randint(0, 19)


@app.route('/api/connection/<connect>', methods=['GET', 'POST'])
def connection_routing(connect):
    global client_count
    try:
        if request.method == "GET":
            if connect == "initiate":
                client_count = client_count + 1
            return jsonify([client_count, fruitX, fruitY])
    except:
        return "Error in connection"


@app.route('/api/packet/<packet>', methods=['GET', 'POST'])
def packet_routing(packet):
    global fruitX
    global fruitY
    try:
        if request.method == "GET":
            if packet == "update":
                fruitX = random.randint(0, 19)
                fruitY = random.randint(0, 19)
                return jsonify([fruitX, fruitY])

        if request.method == "POST":
            if packet == "update":
                player_dir = request.json["currentDir"]
                player_id = request.json["myId"]
                return
    except:
        return "Error in packet"


if __name__ == '__main__':
    socketio.run(app, debug=True)
