from app.chat.communication import Communication

class MockCommunication(Communication):
    def __init__(self):
        self.messages = []

    def send_message(self, message: str, chat_id: int):
        self.messages.append(message)

    def finish_chat(self):
        pass

    def get_messages(self):
        return self.messages
