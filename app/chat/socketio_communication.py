# app/chat/socketio_communication.py
from app.extensions import socketio
from app.chat.communication import Communication

class SocketIOCommunication(Communication):
    def send_message(self, message: str, chat_id: int):
        socketio.emit("receive_message", {"message": message, "chat_id": chat_id})

    def finish_chat(self):
        socketio.emit("finished")
