from app.chat.communication import Communication
from app.chat.models import Chat
from app.extensions import socketio


class SocketIOCommunication(Communication):
    def send_message(self, message: str, chat_id: int):
        socketio.emit("receive_message", {"message": message, "chat_id": chat_id})
        Chat.save_message(message, chat_id, False)

    def finish_chat(self):
        socketio.emit("finished")
