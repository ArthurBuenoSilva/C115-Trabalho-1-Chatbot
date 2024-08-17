import random
from enum import Enum

from app.chat.models import Chat, Message
from app.extensions import db, socketio


class States(Enum):
    FIRST_MESSAGE = -1
    OPTIONS = 0
    CONSUMPTION = 1
    BILL = 2
    SUPPORT = 3
    FINISH = 4
    UNKNOWN = 5


class ChatHandler:
    def __init__(self):
        self.current_state: States = States.FIRST_MESSAGE
        self.current_chat: Chat | None = None

    def handle_received_message(self, chat, message: str):
        self.current_chat = chat

        if self.current_state == States.FIRST_MESSAGE:
            self.send_message("Olá, meu nome é Samuel!")
            self.send_message("Como posso te ajuda?")
            self.send_message(
                "Digite:\n\n1 - Consumo de energia\n2 - Fatura\n3 - Falar com um atendente\n4 - Finalizar atendimento"
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
            self.send_message(message)
            self.current_state = States.FINISH

        if self.current_state == States.BILL:
            consumption = self.get_random_consumption()
            message = f"A fatura no valor de R$ {consumption} foi enviado para o seu email!"
            self.send_message(message)
            self.current_state = States.FINISH

        if self.current_state == States.SUPPORT:
            message = "Um atendente irá falar com você em breve. Por favor, aguarde."
            self.send_message(message)
            self.current_state = States.FINISH

        if self.current_state == States.UNKNOWN:
            message = f"Não entendi a mensagem '{message}'"
            self.send_message(message)
            self.current_state = States.FINISH

        if self.current_state == States.FINISH:
            message = "Seu atendimento foi finalizado."
            self.send_message(message)

            message = "Espero ter ajudado :)"
            self.send_message(message)

            self.current_state = States.FIRST_MESSAGE
            self.finish_chat()

    def send_message(self, message: str):
        socketio.emit("receive_message", {"message": message, "chat_id": self.current_chat.id})
        self.save_mensage(message=message, chat=self.current_chat, is_it_mine=False)

    def finish_chat(self):
        self.current_chat = None
        socketio.emit("finished")

    def get_random_consumption(self) -> float:
        return round(random.uniform(100.00, 300.00), 2)

    @staticmethod
    def save_mensage(message: str, chat: Chat | None, is_it_mine: bool = True):
        message_obj = Message(message=message, chat_id=chat.id, is_it_mine=is_it_mine)
        db.session.add(message_obj)
        db.session.commit()


chat_handler = ChatHandler()
