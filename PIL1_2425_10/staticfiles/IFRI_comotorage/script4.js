document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('span');
    const sidebar = document.getElementById('footer');
    let hideSidebarTimeout;

    if (window.matchMedia("(min-width: 500px)").matches) {
        toggleBtn.addEventListener('mouseenter', () => {
            clearTimeout(hideSidebarTimeout);
            sidebar.style.left = '0';
            toggleBtn.innerHTML = '<i class="fas fa-angle-left"></i>';
            toggleBtn.style.left = '100px';

            hideSidebarTimeout = setTimeout(() => {
                sidebar.style.left = '-120px';
                toggleBtn.innerHTML = '<i class="fas fa-angle-right"></i>';
                toggleBtn.style.left = '0';
            }, 2000);
        });

        sidebar.addEventListener('mouseenter', () => {
            clearTimeout(hideSidebarTimeout);
            sidebar.style.left = '0';
            toggleBtn.innerHTML = '<i class="fas fa-angle-left"></i>';
            toggleBtn.style.left = '100px';
        });

        sidebar.addEventListener('mouseleave', () => {
            hideSidebarTimeout = setTimeout(() => {
                sidebar.style.left = '-120px';
                toggleBtn.innerHTML = '<i class="fas fa-angle-right"></i>';
                toggleBtn.style.left = '0';
            }, 200);
        });
    }

    const chatSocket = new WebSocket("ws://" + window.location.host + "/");

        chatSocket.onopen = function (e) {
            console.log("The connection was setup successfully!");
        };

        chatSocket.onclose = function (e) {
            console.log("Something unexpected happened!");
        };
        
        document.querySelector("#id_message_send_input").focus();
        document.querySelector("#id_message_send_input").onkeyup = function (e) {
            if (e.keyCode === 13) { 
                document.querySelector("#id_message_send_button").click();
            }
        };

        document.querySelector("#id_message_send_button").onclick = function (e) {
            var messageInput = document.querySelector("#id_message_send_input").value;
            
            if (messageInput.trim() !== "") { 
                const username = document.body.dataset.username;
                chatSocket.send(JSON.stringify({ message: messageInput, username: username }));
                document.querySelector("#id_message_send_input").value = "";
            }
        };

        chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        var div = document.createElement("div");
        div.innerHTML = data.username + " : " + data.message;

        const currentUser = document.body.dataset.username; 

        if (data.username === currentUser) {
            div.classList.add("my-message"); 
        } else {
            div.classList.add("other-message"); 
        }

        const chatContainer = document.querySelector("#id_chat_item_container");
        chatContainer.insertBefore(div, chatContainer.firstChild);
    };

});