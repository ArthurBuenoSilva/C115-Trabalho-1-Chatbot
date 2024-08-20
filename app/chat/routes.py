from flask import redirect, render_template

from app.chat import bp
from app.chat.models import Chat
from app.chat.view import States, chat_handler
from app.extensions import db, socketio


@bp.route("/")
def index():
    return render_template("chat.html")


@bp.route("/history")
def history():
    context = {"chats": Chat.get_all_chats()}

    return render_template("history.html", context=context)


@bp.route("/clear")
def clear():
    Chat.clear_all()
    return redirect("history")


@socketio.on("send_message")
def read_sent_message(data):
    chat_id = data["chatId"]
    message = data["message"]

    if not chat_id:
        chat = Chat()
        db.session.add(chat)
        db.session.commit()
        chat_handler.current_state = States.FIRST_MESSAGE
    else:
        chat = Chat.query.filter_by(id=chat_id).first()

    chat_handler.save_mensage(message=message, chat=chat, is_it_mine=True)
    chat_handler.handle_received_message(chat, message)


@socketio.on("get_messages")
def get_all_messages(id):
    chat = Chat.query.filter_by(id=id).first()
    messages = chat.get_all_messages()
    socketio.emit("show_messages", {"chat": chat.id, "created_at": chat.created_at, "messages": messages})
