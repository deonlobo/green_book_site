const messenger_template_data = document.currentScript.dataset

let pinned_conversations = [];
let private_conversations = [];
let group_conversations = [];

const pinned_node = $("#pinned__list")
const private_node = $("#private__list")
const group_node = $("#group__list")
const filter_conversations_debounce = debounce(() => get_conversations_by_filter());
const get_users_debounce = debounce(() => get_users());
let add_button_toggle_state = false;
let toggle_private_conv_modal_state = false;


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

function get_pinned_conversations(input_filter) {
  $.ajax({
    type: 'GET',
    url: messenger_template_data["pinned_conversations_url"],
    data: {
      "filter": input_filter
    },
    success: function (response) {
      pinned_conversations = JSON.parse(response["pinned_conversations"])
      console.log(pinned_conversations);
      pinned_node.off('click', '.btn__pin');
      pinned_node.off("click", ".messenger__list__element")
      pinned_node.empty();
      if (pinned_conversations.length > 0) {
        const title_node = `<p class="text-muted px-4 m-0"><b>Pinned</b></p>`
        pinned_node.append(title_node)

      }
      pinned_conversations.forEach(conversation => {
        const list_node = generate_conversation_list_item(conversation['fields'].conversation_uuid,
          conversation['fields'].conversation_name, true)
        pinned_node.append(list_node)

        $(`#pin-btn-${conversation['fields'].conversation_uuid}`).on('click', function (event) {
          event.stopPropagation()
          toggle_pin(conversation['fields'].conversation_uuid)
        });

        const pinned_element = pinned_node.children().last();
        console.log(pinned_element);
        pinned_element.on("click", function (clickEvent) {
          console.log(clickEvent);
          const conversation_uuid =
            this.dataset["conversation_uuid"];
          window.location.pathname = "/messenger/" + conversation_uuid + "/";
        })


      });
    },
    error: function () {

    }
  });




}


function get_private_conversations(input_filter) {
  $.ajax({
    type: 'GET',
    url: messenger_template_data["private_conversations_url"],
    data: {
      "filter": input_filter
    },
    success: function (response) {
      private_conversations = JSON.parse(response["private_conversations"])
      console.log(private_conversations);
      private_node.off('click', '.btn__pin');
      private_node.empty();
      if (private_conversations.length > 0) {
        const title_node = `<p class="text-muted px-4 m-0"><b>Private</b></p>`
        private_node.append(title_node)

      }
      private_conversations.forEach(conversation => {
        console.log("here");
        const list_node = generate_conversation_list_item(conversation['fields'].conversation_uuid,
          conversation['fields'].conversation_name, false)
        // list_node.click(toggle_pin)
        private_node.append(list_node)
        $(`#pin-btn-${conversation['fields'].conversation_uuid}`).on('click', function (event) {
          event.stopPropagation()
          toggle_pin(conversation['fields'].conversation_uuid)
        });

      });
    },
    error: function () {

    }
  });
}

function generate_conversation_list_item(conversation_uuid, conversation_name, pinned) {
  return (`
    <div data-conversation_uuid=${conversation_uuid}
            class="position-relative messenger__list__element d-flex p-2 px-4 border-bottom">
            <span class=" rounded-circle overflow-hidden">
              <img width="50" height="50"
                src="https://api.dicebear.com/9.x/initials/svg?seed=${conversation_name}" alt="" />
            </span>
            <span class="d-flex align-items-center ml-2"><b>${conversation_name}</b></span>
            <span data-conversation_uuid="{{conversation.conversation_uuid}}"
              class="conversation__pin position-absolute">
              <button class="btn btn__pin" id="pin-btn-${conversation_uuid}">
              ${pinned?`
              
              <svg width="25" height="25" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M17.1218 1.87023C15.7573 0.505682 13.4779 0.76575 12.4558 2.40261L9.75191 6.73289L11.1969 8.17793C11.2355 8.1273 11.2723 8.07415 11.3071 8.01845L14.1523 3.46191C14.493 2.91629 15.2528 2.8296 15.7076 3.28445L20.6359 8.21274C21.0907 8.66759 21.0041 9.42737 20.4584 9.76806L15.9019 12.6133C15.8462 12.6481 15.793 12.6848 15.7424 12.7234L17.1874 14.1684L21.5177 11.4645C23.1546 10.4424 23.4147 8.16307 22.0501 6.79852L17.1218 1.87023Z"
                  fill="#f8f5f1" />
                <path
                  d="M3.56525 8.85242C3.6015 8.26612 3.84962 7.68582 4.32883 7.27422L5.77735 8.72274C5.75784 8.72967 5.73835 8.7368 5.71886 8.74414C5.64516 8.7719 5.61855 8.80285 5.60548 8.82181C5.58877 8.84604 5.56651 8.8937 5.56144 8.97583C5.55046 9.15333 5.62872 9.40686 5.82846 9.6066L14.3137 18.0919C14.5135 18.2916 14.767 18.3699 14.9445 18.3589C15.0266 18.3538 15.0743 18.3316 15.0985 18.3149C15.1175 18.3018 15.1484 18.2752 15.1762 18.2015C15.1835 18.182 15.1907 18.1625 15.1976 18.143L16.6461 19.5915C16.2345 20.0707 15.6542 20.3188 15.0679 20.3551C14.2853 20.4035 13.4808 20.0874 12.8995 19.5061L9.36397 15.9705L2.68394 22.6506C2.29342 23.0411 1.66025 23.0411 1.26973 22.6506C0.879206 22.26 0.879206 21.6269 1.26973 21.2363L7.94975 14.5563L4.41425 11.0208C3.83293 10.4395 3.51687 9.63502 3.56525 8.85242Z"
                  fill="#f8f5f1" />
                <path
                  d="M2.00789 2.00786C1.61736 2.39838 1.61736 3.03155 2.00789 3.42207L20.5862 22.0004C20.9767 22.3909 21.6099 22.3909 22.0004 22.0004C22.391 21.6099 22.391 20.9767 22.0004 20.5862L3.4221 2.00786C3.03158 1.61733 2.39841 1.61733 2.00789 2.00786Z"
                  fill="#f8f5f1" />
              </svg>`:`
              <svg width="25" height="25" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd"
                  d="M17.1218 1.87023C15.7573 0.505682 13.4779 0.76575 12.4558 2.40261L9.61062 6.95916C9.61033 6.95965 9.60913 6.96167 9.6038 6.96549C9.59728 6.97016 9.58336 6.97822 9.56001 6.9848C9.50899 6.99916 9.44234 6.99805 9.38281 6.97599C8.41173 6.61599 6.74483 6.22052 5.01389 6.87251C4.08132 7.22378 3.61596 8.03222 3.56525 8.85243C3.51687 9.63502 3.83293 10.4395 4.41425 11.0208L7.94975 14.5563L1.26973 21.2363C0.879206 21.6269 0.879206 22.26 1.26973 22.6506C1.66025 23.0411 2.29342 23.0411 2.68394 22.6506L9.36397 15.9705L12.8995 19.5061C13.4808 20.0874 14.2853 20.4035 15.0679 20.3551C15.8881 20.3044 16.6966 19.839 17.0478 18.9065C17.6998 17.1755 17.3043 15.5086 16.9444 14.5375C16.9223 14.478 16.9212 14.4114 16.9355 14.3603C16.9421 14.337 16.9502 14.3231 16.9549 14.3165C16.9587 14.3112 16.9606 14.31 16.9611 14.3098L21.5177 11.4645C23.1546 10.4424 23.4147 8.16307 22.0501 6.79853L17.1218 1.87023ZM14.1523 3.46191C14.493 2.91629 15.2528 2.8296 15.7076 3.28445L20.6359 8.21274C21.0907 8.66759 21.0041 9.42737 20.4584 9.76806L15.9019 12.6133C14.9572 13.2032 14.7469 14.3637 15.0691 15.2327C15.3549 16.0037 15.5829 17.1217 15.1762 18.2015C15.1484 18.2752 15.1175 18.3018 15.0985 18.3149C15.0743 18.3316 15.0266 18.3538 14.9445 18.3589C14.767 18.3699 14.5135 18.2916 14.3137 18.0919L5.82846 9.6066C5.62872 9.40686 5.55046 9.15333 5.56144 8.97583C5.56651 8.8937 5.58877 8.84605 5.60548 8.82181C5.61855 8.80285 5.64516 8.7719 5.71886 8.74414C6.79869 8.33741 7.91661 8.56545 8.68762 8.85128C9.55668 9.17345 10.7171 8.96318 11.3071 8.01845L14.1523 3.46191Z"
                  fill="#f8f5f1" />
              </svg>
              
              `}
              </button>
            </span>
      </div>

    `)
}


function toggle_loader(isVisible) {
  const list_loader = $("#list__loader")

  if (isVisible) {
    list_loader.show()
  } else {
    list_loader.hide()
  }
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

function get_conversations_by_filter() {
  const input_filter = $("#messenger__search__input").val()
  toggle_loader(true)
  get_pinned_conversations(input_filter)
  get_private_conversations(input_filter)
  toggle_loader(false)

}

function toggle_pin(conversation_uuid) {
  $.ajax({
    type: 'GET',
    url: messenger_template_data["toggle_conversation_pin_url"],
    data: {
      conversation_uuid: conversation_uuid
    },
    success: function (response) {
      toggle_loader(true)
      get_conversations_by_filter()
      toggle_loader(false)
    },
    error: function () {}
  });
}


function add_button_toggle() {
  add_button_toggle_state = !add_button_toggle_state
  if (add_button_toggle_state) {
    $("#add_conversation_btn").css({
      transform: "rotate(45deg)",
      transition: "transform 0.2s"
    });
    $("#add__button__modal").animate({
        height: '3rem',
      },
      200
    );
  } else {
    $("#add_conversation_btn").css({
      transform: "rotate(0deg)",
      transition: "transform 0.2s"
    });
    $("#add__button__modal").animate({
        height: 0,
      },
      200
    );
  }
}

function open_private_conversation_modal() {
  add_button_toggle()
  toggle_private_conv_modal_state = !toggle_private_conv_modal_state
  if (toggle_private_conv_modal_state) {
    $("#messenger_private_conversation_model").animate({
      top: "0%"
    }, 200);
  } else {
    $("#messenger_private_conversation_model").animate({
      top: "100%"
    }, 200);
  }
}

function close_private_conversation_modal() {
  toggle_private_conv_modal_state = !toggle_private_conv_modal_state
  $("#messenger_private_conversation_model").animate({
    top: "100%"
  }, 200);
  $(".name__badge").html(".........")
  $("#user__name__input").val('');
  $('#search__result__container').empty();
}

function get_users() {
  let username = $('#user__name__input').val();
  $('#search__result__container').off('click', '.search__list__item');
  $.ajax({
    type: 'GET',
    url: messenger_template_data["get_users_url"],
    data: {
      user_name: username
    },
    success: function (response) {
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
    error: function () {}
  });

  $('#search__result__container').on('click', '.search__list__item', function (e) {
    $('.name__badge').html(this.dataset.fname + " " + this.dataset.lname);
    $('#user__name__input').val(this.dataset.uname);
  });

}

$('#add_private_conversation_form').on('submit', function (event) {
  event.preventDefault();
  let formData = $(this).serialize();
  $.ajax({
    type: 'POST',
    url: messenger_template_data['add_private_conversation_url'],
    data: formData,
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", messenger_template_data['csrf_token']);
    },
    success: function (response) {
      if (response.status === 'success') {
        window.location.pathname = "/messenger/" + response.conversation_id + "/";
      }
    },
    error: function () {}
  });
});

adjust_message_container_height();
toggle_loader(true)
get_pinned_conversations("")
get_private_conversations("")
toggle_loader(false)