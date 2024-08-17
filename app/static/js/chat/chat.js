const socket = io();
const chat = document.getElementById("chat");
let chatId = null;

function sendMessage() {
    const message = document.getElementById("message");

    if (message.value) {
        const messageElement = document.createElement('div');
        messageElement.className = "flex justify-end w-full mb-2 snap-center"
        messageElement.innerHTML = `
            <div class="flex items-start gap-2.5">
                <div class="flex flex-col max-w-[320px] leading-1.5 px-4 py-1 border-gray-200 bg-chatMyMessageBackground rounded-s-3xl rounded-br-3xl">
                    <p class="text-sm font-normal py-1.5 text-chatMyMessageText break-words">
                        ${message.value}
                    </p>
                </div>
            </div>
        `;
        chat.appendChild(messageElement);
    
        socket.emit("send_message", {chatId: chatId, message: message.value});
    
        message.value = "";
    };
}

function startNewChat() {
    chat.innerHTML = '';
    sendMessage();

    const button = document.getElementById("sendMessage");
    button.onclick = sendMessage;
}

function scrollToBottom() {
    chat.scrollTop = chat.scrollHeight;
}

socket.on("receive_message", function(data) {
    if (data.message) {
        const message = data.message.split('\n').map(line => `<span>${line}</span>`).join('<br>');
        const messageElement = document.createElement("div");
        messageElement.className = "w-full grow-0 mb-2 snap-center";

        messageElement.innerHTML = `
            <div class="flex items-start gap-2.5">
                <div class="flex flex-col max-w-[320px] leading-1.5 px-4 py-1 border-gray-200 bg-chatMessageBackground rounded-e-3xl rounded-bl-3xl">
                    <p class="text-sm font-normal py-1.5 text-chatMessageText break-words">
                        ${message}
                    </p>
                </div>
            </div>
        `;
        chat.appendChild(messageElement);
        scrollToBottom();
    }

    if (data.chat_id) {
        chatId = data.chat_id;
    }
});


socket.on("finished", function() {
    const button = document.getElementById("sendMessage");
    button.onclick = startNewChat;
    chatId = null;
});