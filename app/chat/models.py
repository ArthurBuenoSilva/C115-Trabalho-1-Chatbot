from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, ForeignKey, Integer, String

from app.extensions import db


def model_to_dict(model_instance):
    return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}


class Chat(db.Model):
    id = db.Column(Integer, primary_key=True)
    messages = db.relationship("Message", backref="chat", lazy=True, cascade="all, delete")
    created_at = db.Column(String(150), default=datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    def __repr__(self):
        return f'<Chat "{self.id}" created at {self.created_at}>'

    def get_all_messages(self) -> list[dict[str, Any]]:
        messages = list()

        for message in self.messages:  # type: ignore
            messages.append({"id": message.id, "message": message.message, "is_it_mine": message.is_it_mine})

        return messages

    @staticmethod
    def get_all_chats() -> list[dict[str, Any]]:
        chats = list()

        for chat in Chat.query.all():
            chats.append(model_to_dict(chat))

        return chats

    @staticmethod
    def clear_all():
        for chat in Chat.query.all():
            db.session.delete(chat)
        db.session.commit()


class Message(db.Model):
    id = db.Column(Integer, primary_key=True)
    message = db.Column(String(150), nullable=False)
    is_it_mine = db.Column(Boolean, nullable=False)

    # Chat foreign key
    chat_id = db.Column(Integer, ForeignKey("chat.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'<Message "{self.message}">'
