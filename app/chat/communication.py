from abc import ABC, abstractmethod


class Communication(ABC):
    def __init__(self):
        self.messages = list()

    @abstractmethod
    def send_message(self, message: str, chat_id: int):
        pass

    @abstractmethod
    def finish_chat(self):
        pass

    def get_messages(self):
        return self.messages
