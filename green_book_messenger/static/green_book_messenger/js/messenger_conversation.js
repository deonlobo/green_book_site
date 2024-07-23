const messenger_template_data = document.currentScript.dataset

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

adjust_message_container_height();

const conversation_name = messenger_template_data["selected_conversation_uuid"]
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
    const conversation_list_elements = document.getElementById(
      "messenger__conversation__container"
    );

    let docElement = "";

    // Parse the timestamp to a Date object
    const date = new Date(data.timestamp);

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
    formattedTimestamp = `${formattedDate}, ${formattedTime}`;

    if (messenger_data['user_id'] == data.user_id) {
      docElement = `<div class="d-flex flex-column mb-4 mr-3">
            <span class="messenger_conversation__bubble bubble__right p-3">${data.message}</span>
            <span
              class="messenger_conversation__timestamp badge rounded-pill align-self-end">${formattedTimestamp}
            </span>
          </div>`;
    } else {
      docElement = `<div class="d-flex flex-column mb-4 ml-3">
            <span class="rounded-circle overflow-hidden align-self-start mb-1">
              <img width="30" height="30" src="https://api.dicebear.com/9.x/pixel-art-neutral/svg" alt="" />
            </span>
            <span class="messenger_conversation__bubble bubble__left br-0 p-3">${data.message}</span>
            <span
              class="messenger_conversation__timestamp badge rounded-pill align-self-start">${formattedTimestamp}</span>
          </div>
      `;
    }

    const newMessageElement = document.createElement("div");
    newMessageElement.innerHTML = docElement;
    conversation_list_elements.insertBefore(
      newMessageElement,
      conversation_list_elements.firstChild
    );


  };

  chatSocket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };

  document.querySelector("#messenger__chat__input").focus();
  document.querySelector("#messenger__chat__input").onkeyup = function (e) {
    if (e.keyCode === 13) {
      // enter, return
      document.querySelector("#messenger__chat__submit").click();
    }
  };

  document.querySelector("#messenger__chat__submit").onclick = function (e) {
    const messageInputDom = document.querySelector("#messenger__chat__input");
    const message = messageInputDom.value;
    const timestamp = new Date().toISOString();
    chatSocket.send(
      JSON.stringify({
        message_content: message,
        timestamp: timestamp,
        user_id: messenger_data['user_id'],
      })
    );
    messageInputDom.value = "";
  };
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
  console.log("Here");
  // Use traditional 'for loops' for IE 11
  for (let mutation of mutationsList) {
    if (mutation.type === "childList") {
      $("#messenger__conversation__container").animate({
          scrollTop: $("#messenger__conversation__container")[0].scrollHeight,
        },
        500
      );
    }
  }
};

// Create an observer instance linked to the callback function
let observer = new MutationObserver(callback);

// Start observing the target node for configured mutations
observer.observe(targetNode, config);
