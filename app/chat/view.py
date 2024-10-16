import random
from enum import Enum

from app.chat.communication import Communication
from app.chat.models import Chat, Message
from app.chat.socketio_communication import SocketIOCommunication
from app.extensions import db


class States(Enum):
    FIRST_MESSAGE = -1
    OPTIONS = 0
    CONSUMPTION = 1
    BILL = 2
    SUPPORT = 3
    FINISH = 4
    UNKNOWN = 5


class ChatHandler:
    def __init__(self, communication: Communication):
        self.communication = communication
        self.current_state = States.FIRST_MESSAGE
        self.current_chat = None

    def handle_received_message(self, chat: Chat, message: str):
        self.current_chat = chat

        if self.current_state == States.FIRST_MESSAGE:
            self.communication.send_message("Olá, meu nome é Samuel!", chat.id)
            self.communication.send_message("Como posso te ajuda?", chat.id)
            self.communication.send_message(
                "Digite:\n\n1 - Consumo de energia\n2 - Fatura\n3 - Falar com um atendente\n4 - Finalizar atendimento",
                chat.id,
            )
            self.current_state = States.OPTIONS
            return

        if self.current_state == States.OPTIONS:
            match message:
                case "1":
                    self.current_state = States.CONSUMPTION
                case "2":
                    self.current_state = States.BILL
                case "3":
                    self.current_state = States.SUPPORT
                case "4":
                    self.current_state = States.FINISH
                case _:
                    self.current_state = States.UNKNOWN

        if self.current_state == States.CONSUMPTION:
            consumption = self.get_random_consumption()
            message = f"O seu consumo de energia do último mês foi de R$ {consumption}"
            self.communication.send_message(message, chat.id)
            self.current_state = States.FINISH

        if self.current_state == States.BILL:
            consumption = self.get_random_consumption()
            message = f"A fatura no valor de R$ {consumption} foi enviado para o seu email!"
            self.communication.send_message(message, chat.id)
            self.current_state = States.FINISH

        if self.current_state == States.SUPPORT:
            message = "Um atendente irá falar com você em breve. Por favor, aguarde."
            self.communication.send_message(message, chat.id)
            self.current_state = States.FINISH

        if self.current_state == States.UNKNOWN:
            message = f"Não entendi a mensagem '{message}'"
            self.communication.send_message(message, chat.id)
            self.current_state = States.FINISH

        if self.current_state == States.FINISH:
            message = "Seu atendimento foi finalizado."
            self.communication.send_message(message, chat.id)

            message = "Espero ter ajudado :)"
            self.communication.send_message(message, chat.id)

            self.current_state = States.FIRST_MESSAGE
            self.finish_chat()

    def finish_chat(self):
        self.current_chat = None
        self.communication.finish_chat()

    @staticmethod
    def get_random_consumption() -> float:
        return round(random.uniform(100.00, 300.00), 2)

    @staticmethod
    def save_message(message: str, chat: Chat | None, is_it_mine: bool = True):
        message_obj = Message(message=message, chat_id=chat.id, is_it_mine=is_it_mine)
        db.session.add(message_obj)
        db.session.commit()


# Initialize chat_handler with SocketIOCommunication
chat_handler = ChatHandler(SocketIOCommunication())
