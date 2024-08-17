from flask import render_template

from app.chat import bp
from app.chat.models import Chat, Message
from app.chat.view import chat_handler
from app.extensions import db, socketio


@bp.route("/")
def index():
    return render_template("chat.html")


@socketio.on("send_message")
def read_sent_message(data):
    chat_id = data["chatId"]
    message = data["message"]

    print(chat_id)

    if not chat_id:
        chat = Chat()
        db.session.add(chat)
        db.session.commit()
    else:
        chat = Chat.query.filter_by(id=chat_id).first()

    chat_handler.save_mensage(message=message, chat=chat, is_it_mine=True)
    chat_handler.handle_received_message(chat, message)
