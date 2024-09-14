# app/chat/communication.py
from abc import ABC, abstractmethod

class Communication(ABC):
    @abstractmethod
    def send_message(self, message: str, chat_id: int):
        pass

    @abstractmethod
    def finish_chat(self):
        pass
