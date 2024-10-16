from app.chat.communication import Communication
from app.extensions import socketio


class SocketIOCommunication(Communication):
    def send_message(self, message: str, chat_id: int):
        socketio.emit("receive_message", {"message": message, "chat_id": chat_id})

    def finish_chat(self):
        socketio.emit("finished")
