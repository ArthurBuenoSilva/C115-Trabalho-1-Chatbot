const socket = io();

function getMessages(id) {
    socket.emit("get_messages", id);
}

socket.on("show_messages", function(data) {
    const modalTitle = document.getElementById("modal-title");
    const modalBody = document.getElementById("modal-body");

    modalBody.innerHTML = "";

    modalTitle.innerText = `Chat ${data.chat} - ${data.created_at}`;

    data.messages.forEach(message => {
        if (message.is_it_mine) {
            const messageElement = document.createElement('div');
            messageElement.className = "flex justify-end w-full mb-2 snap-center"
            messageElement.innerHTML = `
                <div class="flex items-start gap-2.5">
                    <div class="flex flex-col max-w-[320px] leading-1.5 px-4 py-1 border-gray-200 bg-chatMyMessageBackground rounded-s-3xl rounded-br-3xl">
                        <p class="text-sm font-normal py-1.5 text-chatMyMessageText break-words">
                            ${message.message}
                        </p>
                    </div>
                </div>
            `;
            modalBody.appendChild(messageElement);
        } else {
            const messageText = message.message.split('\n').map(line => `<span>${line}</span>`).join('<br>');
            const messageElement = document.createElement("div");
            messageElement.className = "w-full grow-0 mb-2 snap-center";

            messageElement.innerHTML = `
                <div class="flex items-start gap-2.5">
                    <div class="flex flex-col max-w-[320px] leading-1.5 px-4 py-1 border-gray-200 bg-chatMessageBackground rounded-e-3xl rounded-bl-3xl">
                        <p class="text-sm font-normal py-1.5 text-chatMessageText break-words">
                            ${messageText}
                        </p>
                    </div>
                </div>
            `;
            modalBody.appendChild(messageElement);
        }
    });
})
