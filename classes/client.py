

class Client:
    # The socket id given for the connection
    socket_id: str

    def __init__(self, socket_id: str):
        self.socket_id = socket_id

