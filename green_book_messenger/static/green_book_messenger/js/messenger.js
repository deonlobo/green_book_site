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

const messenger_data = document.currentScript.dataset
console.log(messenger_data);
const conversation_list_elements =
  document.querySelectorAll(".messenger__list__element");
for (
  let element = 0; element < conversation_list_elements.length; element++
) {
  conversation_list_elements[element].addEventListener(
    "click",
    function (clickEvent) {
      console.log(clickEvent);
      const conversation_uuid =
        clickEvent.currentTarget.dataset["conversation_uuid"];
      window.location.pathname = "/messenger/" + conversation_uuid + "/";
    }
  );
}

function getUrlPath() {
  return window.location.pathname;
}

const conversation_name = messenger_data['selected_conversation_uuid'];
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

let add_user_btn_toggle = false;

document.querySelector("#add_user_btn").onclick = function () {
  add_user_btn_toggle = !add_user_btn_toggle
  const add_svg = document.querySelector("#add_user_btn_svg");
  if (add_user_btn_toggle) {
    $("#add_user_btn_svg").css({
      transform: "rotate(45deg)",
      transition: "transform 0.2s"
    });
    // $("#messenger_private_conversation_model").animate({
    //   top: "0%"
    // }, 200);
    // add_svg.style.transform = "rotate(45deg)";
  } else {
    $("#add_user_btn_svg").css({
      transform: "rotate(0deg)",
      transition: "transform 0.2s"
    });
    // $("#messenger_private_conversation_model").animate({
    //   top: "100%"
    // }, 200);
    // add_svg.style.transform = "rotate(0deg)";
  }
}

document.querySelector("#private_converstation_close_button").onclick = function () {
  add_user_btn_toggle = !add_user_btn_toggle
  $("#add_user_btn_svg").css({
    transform: "rotate(0deg)",
    transition: "transform 0.2s"
  });
  $("#messenger_private_conversation_model").animate({
    top: "100%"
  }, 200);
  $(".name__badge").html(".........")
  $("#user__name__input").val('');
  $('#search__result__container').empty();


}


function debounce(func, timeout = 500) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      func.apply(this, args);
    }, timeout);
  };
}

function getUsers() {
  let username = $('#user__name__input').val();
  console.log(messenger_data['getusers_ajax']);
  $('#search__result__container').off('click', '.search__list__item');
  $.ajax({
    type: 'GET',
    url: messenger_data["getusers_ajax"],
    data: {
      user_name: username
    },
    success: function (response) {
      console.log(response);
      $('#search__result__container').empty();
      response.forEach(element => {
        console.log(element);
        let listItem = `
                                <div 
                                data-id=${element.id} 
                                data-fName=${element.firstName} 
                                data-lName=${element.lastName}
                                data-uname=${element.username}
                                class = "search__list__item d-flex p-2 border-bottom" >
                                    <div class="mr-2">
                                      <h3>${element.firstName}</h3>
                                    </div>
                                    <div class="">
                                      <h3>${element.lastName}</h3>
                                    </div>
                                </div>`
        $('#search__result__container').append(listItem);
      });
    },
    error: function () {
      // alert('An error occurred.');
    }
  });

  $('#search__result__container').on('click', '.search__list__item', function (e) {
    console.log(this.dataset);
    $('.name__badge').html(this.dataset.fname + " " + this.dataset.lname);
    $('#user__name__input').val(this.dataset.uname);
  });

}

const getUsersDebouce = debounce(() => getUsers());



$('#add_private_conversation_form').on('submit', function (event) {
  event.preventDefault();
  let formData = $(this).serialize();
  console.log(formData);
  $.ajax({
    type: 'POST',
    url: messenger_data['add_private_conversation'],
    data: formData,
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", messenger_data['csrf_token']);
    },
    success: function (response) {
      if (response.status === 'success') {
        window.location.pathname = "/messenger/" + response.conversation_id + "/";
      }
    },
    error: function () {
      // alert('An error occurred.');
    }
  });
});



// $(".conversation_pin").on("click", function(e) {
//   e.stopPropagation();
//   console.log(this);
// })

$('.conversation__pin').click(function (event) {
  event.stopPropagation();
  const uuid = this.dataset.conversation_uuid
  console.log(uuid);
  $.ajax({
    type: 'GET',
    url: messenger_data["toggle_conversation_pin"],
    data: {
      conversation_uuid: uuid
    },
    success: function (response) {
      console.log(response);
      if (response.status === 'success') {
        window.location.pathname = "/messenger/" + uuid + "/";
      }
    },
    error: function () {
      // alert('An error occurred.');
    }
  });


})