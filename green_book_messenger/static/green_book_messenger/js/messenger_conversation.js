const messenger_template_data = document.currentScript.dataset
const conversation_name = messenger_template_data["selected_conversation_uuid"]
const conversation_message_container = $("#messenger__conversation__container")
const emojiContainer = $("#emoji__container")

const emojis = [
  "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇",
  "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚",
  "😋", "😛", "😜", "🤪", "😝", "🤑", "🤗", "🤭", "🤫", "🤔",
  "🤐", "🤨", "😐", "😑", "😶", "😏", "😒", "🙄", "😬", "🤥",
  "😌", "😔", "😪", "🤤", "😴", "😷", "🤒", "🤕", "🤢", "🤮",
  "🤧", "😵", "🤯", "🤠", "🥳", "😎", "🤓", "🧐", "😕", "😟",
  "🙁", "☹️", "😮", "😯", "😲", "😳", "🥺", "😦", "😧", "😨",
  "😰", "😥", "😢", "😭", "😱", "😖", "😣", "😞", "😓", "😩",
  "😫", "😤", "😡", "😠", "🤬", "😈", "👿", "💀", "☠️", "💩",
  "🤡", "👹", "👺", "👻", "👽", "👾", "🤖", "😺", "😸", "😹",
  "😻", "😼", "😽", "🙀", "😿", "😾",
]



function adjust_message_container_height() {
  // Select the navbar and the target div
  const navbar = document.querySelector("#greenbook--navbar"); // Adjust the selector as needed
  const messenger_container = document.querySelector("#messenger--container"); // Adjust the selector as needed

  // Get the height of the navbar
  const navbarHeight = navbar.offsetHeight;

  // Get the height of the viewport
  const viewportHeight = window.innerHeight;

  // Calculate the height for the target div
  const targetHeight = viewportHeight - navbarHeight;

  // Set the height to the target div
  messenger_container.style.height = `${targetHeight}px`;
}


function formatDate(date) {
  // Format the date
  const formattedDate = date.toLocaleString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  });

  // Format the time part with a.m./p.m.
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const ampm = hours >= 12 ? "p.m." : "a.m.";
  const formattedTime = `${hours % 12 || 12}:${minutes
        .toString()
        .padStart(2, "0")} ${ampm}`;

  // Combine formatted date and time
  const formattedTimestamp = `${formattedDate}, ${formattedTime}`;

  return formattedTimestamp
}


function generate_message_blob(message, timestamp, isLoggedInUser, peerName) {
  let docElement = "";
  if (isLoggedInUser) {
    docElement = `<div class="d-flex flex-column mb-4 mr-3">
                    <span class="messenger_conversation__bubble bubble__right p-3 ml-3">${message}</span>
                    <span
                      class="messenger_conversation__timestamp badge rounded-pill align-self-end">${timestamp}</span>
                  </div>`
  } else {
    docElement = `<div class="d-flex flex-column mb-4 ml-3">
                    <span class="rounded-circle overflow-hidden align-self-start mb-1">
                      <img width="30" height="30"
                        src = "https://api.dicebear.com/9.x/initials/svg?seed=${peerName}"
                        alt = "" / >
                    </span>
                    <span class="messenger_conversation__bubble bubble__left br-0 p-3">${message}</span>
                    <span
                      class="messenger_conversation__timestamp badge rounded-pill align-self-start">${timestamp}</span>
                  </div>`
  }

  return docElement;

}

function redirectToMessengerHome() {
  window.location.href = messenger_template_data["messenger_list_url"];
}



if (conversation_name != "None") {
  const chatSocket = new WebSocket(
    "ws://" +
    window.location.host +
    "/ws/messenger/" +
    conversation_name +
    "/"
  );

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    // Parse the timestamp to a Date object
    const date = new Date(data.timestamp);
    console.log(data);

    const docElement = generate_message_blob(data.message, formatDate(date),
      messenger_template_data['user_id'] == data.user_id,
      data.user_name);

    const newMessageElement = document.createElement("div");
    newMessageElement.innerHTML = docElement;
    if ($('#messenger__conversation__container #start_conversation_message').length > 0) {
      $('#messenger__conversation__container #start_conversation_message').remove();
    }
    conversation_message_container.prepend(newMessageElement);
  };

  chatSocket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };

  $("#messenger__chat__input").focus();
  $('#messenger__chat__input').keyup(function (e) {
    if (e.keyCode === 13) {
      // enter, return
      $("#messenger__chat__submit").click();
    }
  });

  $("#messenger__chat__submit").click(function (e) {
    const messageInputDom = $("#messenger__chat__input");
    const message = messageInputDom.val();
    if (message == "" || message == undefined || message.trim().length == 0) return;

    const timestamp = new Date().toISOString();

    chatSocket.send(
      JSON.stringify({
        message_content: message,
        timestamp: timestamp,
        user_id: messenger_template_data['user_id'],
      })
    );
    messageInputDom.val('');
  })
}


// Select the node that will be observed for mutations
let targetNode = document.getElementById(
  "messenger__conversation__container"
);

// Options for the observer (which mutations to observe)
let config = {
  childList: true
};

// Callback function to execute when mutations are observed
let callback = function (mutationsList, observer) {
  // Use traditional 'for loops' for IE 11
  console.log("mutation");
  let lastChildListMutation = null
  for (let mutation of mutationsList) {
    if (mutation.type === "childList") {
      lastChildListMutation = mutation
    }
  }

  if (lastChildListMutation != null) {
    $("#messenger__conversation__container").animate({
        scrollTop: $("#messenger__conversation__container")[0].scrollHeight,
      },
      500
    );
  }

};

// Create an observer instance linked to the callback function
let observer = new MutationObserver(callback);

// Start observing the target node for configured mutations
observer.observe(targetNode, config);

function get_messages_by_conversation(conversation_id) {
  $.ajax({
    type: 'GET',
    url: messenger_template_data["messages_by_conversation_url"],
    data: {
      "filter": "",
      "conversation_id": conversation_id
    },
    success: function (response) {
      const messages = JSON.parse(response["messages"])
      // conversation_message_container.empty();
      if (messages.length == 0) {
        const empty_message_node = ` <h1 id="start_conversation_message" class="text-center my-auto">Start Conversation</h1>`
        conversation_message_container.append(empty_message_node)

      } else {
        messages.forEach(conversation => {
          const data = conversation["fields"]
          console.log(data);
          const date = new Date(data.timestamp);
          const message_node = generate_message_blob(data.content, formatDate(date),
            messenger_template_data['user_id'] == data.sender,
            data.username);
          const newMessageElement = document.createElement("div");
          newMessageElement.innerHTML = message_node;
          conversation_message_container.prepend(newMessageElement)
        });
      }

    },
    error: function () {

    }
  });
}

function set_emoji(emoji) {
  const messageInputDom = $("#messenger__chat__input");
  const message = messageInputDom.val() + emoji;

  messageInputDom.val(message)

}

emojis.forEach(emoji => {
  emojiContainer.append(`<h3 onclick='set_emoji("${emoji}")' class="emoji__item">${emoji}</h3>`)
})

adjust_message_container_height();
get_messages_by_conversation(conversation_name);