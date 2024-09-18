import pytest
from mock.mock_communication import MockCommunication

from app.chat.models import Chat
from app.chat.view import ChatHandler


@pytest.fixture
def chat_handler_instance():
    # Initialize chat_handler with MockCommunication
    chat_handler = ChatHandler(MockCommunication())
    yield chat_handler


@pytest.fixture
def chat_instance():
    chat = Chat()
    yield chat


def test_verify_first_message_with_help_str(chat_handler_instance: ChatHandler, chat_instance: Chat):
    chat_instance.id = 1
    chat_handler_instance.handle_received_message(chat=chat_instance, message="help")

    expected_message = [
        "Olá, meu nome é Samuel!",
        "Como posso te ajuda?",
        "Digite:\n\n1 - Consumo de energia\n2 - Fatura\n3 - Falar com um atendente\n4 - Finalizar atendimento",
    ]

    assert chat_handler_instance.communication.messages == expected_message


def test_verify_first_message_with_empty_str(chat_handler_instance: ChatHandler, chat_instance: Chat):
    # Verify if the first message is sent correctly
    chat_handler_instance.handle_received_message(chat=chat_instance, message="")

    expected_message = [
        "Olá, meu nome é Samuel!",
        "Como posso te ajuda?",
        "Digite:\n\n1 - Consumo de energia\n2 - Fatura\n3 - Falar com um atendente\n4 - Finalizar atendimento",
    ]

    assert chat_handler_instance.communication.get_messages() == expected_message


def test_verify_consumption_message(chat_handler_instance: ChatHandler, chat_instance: Chat):
    chat_instance.id = 2
    # Verify if the first message is sent correctly
    chat_handler_instance.handle_received_message(chat=chat_instance, message="help")

    expected_message = [
        "Olá, meu nome é Samuel!",
        "Como posso te ajuda?",
        "Digite:\n\n1 - Consumo de energia\n2 - Fatura\n3 - Falar com um atendente\n4 - Finalizar atendimento",
    ]

    assert chat_handler_instance.communication.get_messages() == expected_message

    chat_handler_instance.handle_received_message(chat=chat_instance, message="1")

    random_consumption = chat_handler_instance.communication.get_messages()[3].split(" ")[-1]

    assert 100.0 <= float(random_consumption) <= 300.0

    expected_message.append(f"O seu consumo de energia do último mês foi de R$ {random_consumption}")
    expected_message.append("Seu atendimento foi finalizado.")
    expected_message.append("Espero ter ajudado :)")

    assert chat_handler_instance.communication.get_messages() == expected_message


def test_verify_billing_message(chat_handler_instance: ChatHandler, chat_instance: Chat):
    chat_instance.id = 3
    # Verify if the first message is sent correctly
    chat_handler_instance.handle_received_message(chat=chat_instance, message="help")

    expected_message = [
        "Olá, meu nome é Samuel!",
        "Como posso te ajuda?",
        "Digite:\n\n1 - Consumo de energia\n2 - Fatura\n3 - Falar com um atendente\n4 - Finalizar atendimento",
    ]

    assert chat_handler_instance.communication.get_messages() == expected_message

    chat_handler_instance.handle_received_message(chat=chat_instance, message="2")

    random_consumption = chat_handler_instance.communication.get_messages()[3].split(" ")[6]

    assert 100.0 <= float(random_consumption) <= 300.0

    expected_message.append(f"A fatura no valor de R$ {random_consumption} foi enviado para o seu email!")
    expected_message.append("Seu atendimento foi finalizado.")
    expected_message.append("Espero ter ajudado :)")

    assert chat_handler_instance.communication.get_messages() == expected_message


def test_verify_human_agent_request(chat_handler_instance: ChatHandler, chat_instance: Chat):
    chat_instance.id = 4
    # Verify if the first message is sent correctly
    chat_handler_instance.handle_received_message(chat=chat_instance, message="help")

    expected_message = [
        "Olá, meu nome é Samuel!",
        "Como posso te ajuda?",
        "Digite:\n\n1 - Consumo de energia\n2 - Fatura\n3 - Falar com um atendente\n4 - Finalizar atendimento",
    ]

    assert chat_handler_instance.communication.get_messages() == expected_message

    chat_handler_instance.handle_received_message(chat=chat_instance, message="3")

    expected_message.append("Um atendente irá falar com você em breve. Por favor, aguarde.")
    expected_message.append("Seu atendimento foi finalizado.")
    expected_message.append("Espero ter ajudado :)")

    assert chat_handler_instance.communication.get_messages() == expected_message


def test_verify_finish_chat(chat_handler_instance: ChatHandler, chat_instance: Chat):
    chat_instance.id = 5
    # Verify if the first message is sent correctly
    chat_handler_instance.handle_received_message(chat=chat_instance, message="help")

    expected_message = [
        "Olá, meu nome é Samuel!",
        "Como posso te ajuda?",
        "Digite:\n\n1 - Consumo de energia\n2 - Fatura\n3 - Falar com um atendente\n4 - Finalizar atendimento",
    ]

    assert chat_handler_instance.communication.get_messages() == expected_message

    chat_handler_instance.handle_received_message(chat=chat_instance, message="4")

    expected_message.append("Seu atendimento foi finalizado.")
    expected_message.append("Espero ter ajudado :)")

    assert chat_handler_instance.communication.get_messages() == expected_message


def test_verify_unknown_command(chat_handler_instance: ChatHandler, chat_instance: Chat):
    chat_instance.id = 6
    # Verify if the first message is sent correctly
    chat_handler_instance.handle_received_message(chat=chat_instance, message="help")

    expected_message = [
        "Olá, meu nome é Samuel!",
        "Como posso te ajuda?",
        "Digite:\n\n1 - Consumo de energia\n2 - Fatura\n3 - Falar com um atendente\n4 - Finalizar atendimento",
    ]

    assert chat_handler_instance.communication.get_messages() == expected_message

    chat_handler_instance.handle_received_message(chat=chat_instance, message="unknown")

    expected_message.append("Não entendi a mensagem 'unknown'")
    expected_message.append("Seu atendimento foi finalizado.")
    expected_message.append("Espero ter ajudado :)")

    assert chat_handler_instance.communication.get_messages() == expected_message
