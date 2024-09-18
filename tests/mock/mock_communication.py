from app.chat.communication import Communication


class MockCommunication(Communication):
    def send_message(self, message: str, chat_id: int):
        self.messages.append(message)

    def finish_chat(self):
        pass
