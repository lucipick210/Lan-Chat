let lastCount = 0;

async function loadMessages(){

    const response =
    await fetch("/messages")

    const messages =
    await response.json()

    const messagesDiv =
    document.getElementById("messages")

    if(messages.length === lastCount){
        return
    }

    const wasNearBottom =
        messagesDiv.scrollHeight -
        messagesDiv.scrollTop -
        messagesDiv.clientHeight < 50

    messagesDiv.innerHTML = ""

    messages.forEach(msg=>{

        messagesDiv.innerHTML += `
        <div class="message">
            <b>${msg.username}</b>

            <span class="time">
                ${msg.time || ""}
            </span>

            <br>

            ${msg.message}
        </div>
        `
    })

    if(wasNearBottom){

        messagesDiv.scrollTop =
        messagesDiv.scrollHeight

    }

    lastCount = messages.length
}

async function sendMessage(){

    const username =
    document.getElementById("username").value

    const message =
    document.getElementById("message").value

    if(message.trim()==""){
        return
    }

    const time =
    new Date().toLocaleTimeString()

    await fetch("/send",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            username,
            message,
            time

        })

    })

    document.getElementById("message").value=""

    loadMessages()
}

document
.getElementById("message")
.addEventListener(
"keypress",

function(event){

    if(event.key==="Enter"){
        sendMessage()
    }

})

if(localStorage.username){

document.getElementById(
"username"
).value =
localStorage.username

}

setInterval(loadMessages,1000)

loadMessages()

document.getElementById(
"userLabel"
).innerText =
localStorage.username


function logout(){

    localStorage.removeItem(
    "username"
    )

    window.location.href=
    "/login.html"

}