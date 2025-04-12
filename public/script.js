const sidebar = document.querySelector("#sidebar");
const hide_sidebar = document.querySelector(".hide-sidebar");
const new_chat_button = document.querySelector(".new-chat");

const user_menu = document.querySelector(".user-menu ul");
const show_user_menu = document.querySelector(".user-menu button");
let answers = []


const models = document.querySelectorAll(".model-selector button");

for( const model of models ) {
    model.addEventListener("click", function() {
        document.querySelector(".model-selector button.selected")?.classList.remove("selected");
        model.classList.add("selected");
    });
}

const input_message = document.querySelector("#message");
const output_message = "я поки трішки stupid, тому не можу відповісти на запитання.( можливо, колись мій творець навчить мене бути розумнішим, і тоді я зможу тобі допомогти, а поки що нажаль я можу писати лише одне і те ж повідомлення. сподіваюсь скоро це зміниться, дякую за ваше терпіння!";

input_message.addEventListener("keyup", async function(e) {
    input_message.style.height = "auto";
    let height = input_message.scrollHeight + 2;
    if (height > 200) {
        height = 200;
    }
    input_message.style.height = height + "px";

    if (e.key === "Enter" && e.shiftKey) {
        e.preventDefault(); // щоб не вставлялося \n
        await sendMessage();
    }
});


function show_view( view_selector ) {
    document.querySelectorAll(".view").forEach(view => {
        view.style.display = "none";
    });

    document.querySelector(view_selector).style.display = "flex";
}

document.querySelectorAll(".conversation-button").forEach(button => {
    button.addEventListener("click", function() {
        show_view( ".conversation-view" );
    })
});

const send_button = document.querySelector(".send-button");

send_button.addEventListener("click", sendMessage);

async function simulateTyping(sender, fullText) {
    const conversation = document.querySelector(".conversation-view");

    const messageDiv = document.createElement("div");
    messageDiv.classList.add(sender, "message");

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("content");

    const paragraph = document.createElement("p");
    contentDiv.appendChild(paragraph);

    messageDiv.appendChild(contentDiv);
    conversation.appendChild(messageDiv);
    conversation.scrollTop = conversation.scrollHeight;

    for (let i = 0; i < fullText.length; i++) {
        paragraph.textContent += fullText[i];
        conversation.scrollTop = conversation.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 20)); // швидкість тут
    }
}

async function sendRequest(requestText) {
    resp = "";
    await fetch("https://math-faculty-chat-production.up.railway.app/3-5/question", 
        {method: "POST", body: JSON.stringify({
            text: requestText,
            previousAnswers: answers.join(";")
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }})
    .then((response => resp = response.json()));
    return resp;
}

async function sendMessage() {
    const messageText = input_message.value.trim();
    if (messageText === "") return;

    addMessage("user", messageText);
    input_message.value = "";
    input_message.style.height = "auto";

    let output = await sendRequest(messageText); 

    answers.push(output.message);
    setTimeout(() => {
        simulateTyping("assistant", output.message);
    }, 500);
}

function addMessage(sender, text) {
    const conversation = document.querySelector(".conversation-view");

    const messageDiv = document.createElement("div");
    messageDiv.classList.add(sender, "message");

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("content");

    const paragraph = document.createElement("p");
    paragraph.textContent = text;

    contentDiv.appendChild(paragraph);
    messageDiv.appendChild(contentDiv);

    conversation.appendChild(messageDiv);

    conversation.scrollTop = conversation.scrollHeight;
}
