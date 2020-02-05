document.addEventListener("DOMContentLoaded", () => {
  
  // get username
  if (document.querySelector("#display_name_is")) {
    localStorage.setItem("display_name", document.querySelector("#display_name_is").innerHTML);
  }

  // get active channel
  document.querySelectorAll("#ch_item").forEach(item => {
    item.onclick = () => {
      if (localStorage.getItem("display_name")) {
        localStorage.setItem("act_ch", item.dataset.ch);
      }
    };
  });

  // init. the socketIO
  var socket = io();

  if (document.querySelector("#send_txt")) {
    document.querySelector("#send_txt").focus();
    // scroll page down when user reaches the page
    window.scrollBy(0, document.documentElement.scrollHeight - window.innerHeight)
  }
  
  // SOCKETIO: When connected, send user's old messages and see if there is other messeges on server
  socket.on("connect", () => {
    // make sure channel in the url is same as stored active channel
    if (window.location.pathname.substring(9,) !== localStorage['act_ch']) {
      localStorage.setItem("act_ch", window.location.pathname.substring(9,));
    }
    socket.emit("all_msgs", { ch_name: localStorage.getItem("act_ch") });
  });

  // SOCKETIO: receive older messages
  socket.on("all_msgs", data => {
    data.forEach(item => {
      add_msg(item);
    });
  });

  // SOCKETIO: receive new msg
  socket.on("new_msg", data => {
    add_msg(data);
  });

  // SOCKETIO: receive delete message
  socket.on("delete_msg", data => {
    const del_id = data.del_id;
    if (document.querySelector(`div#${del_id}`)) {
      document.querySelector(`div#${del_id}`).remove();
    }
    // also add changes to messeges count of this channel
    document.querySelector(
      `a[data-ch=${localStorage.getItem("act_ch")}]~span`
    ).innerText = data.chat_count;
    // scroll page down
    window.scrollBy(0, document.documentElement.scrollHeight - window.innerHeight);
  });

  // submit new messages to server
  document.querySelector("#send").onsubmit = () => {
    const text = document.querySelector("#send_txt").value;
    socket.emit("submit_msg", {
      u_msg: text,
      ch_name: `${localStorage.getItem("act_ch")}`
    });
    document.querySelector("#send_txt").value = "";
    return false;
  };

  // function to add msg to html
  function add_msg(msg) {
    if (localStorage.getItem("display_name") === msg.user_id) {
      var class1 = "right";
    } else {
      var class1 = "left";
    }
    // create div container
    const new_msg = document.createElement("div");
    new_msg.classList = `chat_container ${class1}` ;
    new_msg.id = `${msg.id}`;
    // create h5 tag for user name
    const h5_name = document.createElement("h5");
    h5_name.className = class1;
    h5_name.innerHTML = msg.user_id;
    new_msg.append(h5_name);
    // create image tag for user image
    const img_img = document.createElement("img");
    img_img.className = class1;
    img_img.src = msg.user_img;
    new_msg.append(img_img);
    // create p tag for user chat message
    const p_msg = document.createElement("p");
    p_msg.className = class1;
    p_msg.innerHTML = msg.messege;
    new_msg.append(p_msg);
    // create delete link for a chat message
    const del_a = document.createElement("a");
    del_a.className = class1;
    del_a.id = `${msg.id}`;
    const link = document.createTextNode("Delete");
    del_a.appendChild(link);
    del_a.href = "#";
    del_a.title = "delete message";
    new_msg.append(del_a);
    // create span tag for time of user chat message
    const span_time = document.createElement("span");
    span_time.className = "time";
    span_time.innerHTML = msg.timestamp;
    new_msg.append(span_time);
    // When delete button is clicked, remove message.
    del_a.onclick = function() {
      if (localStorage.getItem("display_name") === msg.user_id) {
        del_id = this.id;
        this.parentElement.remove();
        socket.emit("delete_msg", {u_msg: msg.messege, ch_name: localStorage.getItem("act_ch"), del_id: del_id});
        // scroll page down
        window.scrollBy(0, document.documentElement.scrollHeight - window.innerHeight);
      } else {
        alert("you can't delete a message of other users");
        // scroll page down
        window.scrollBy(0, document.documentElement.scrollHeight - window.innerHeight);
      }
    };
    // finally add this content to DOM
    document.querySelector("#msgs_list").append(new_msg);
    // scroll page down
    window.scrollBy(0, document.documentElement.scrollHeight - window.innerHeight)
    // also add changes to messeges count of this channel
    if (msg.chat_count) {
      document.querySelector(
        `a[data-ch=${localStorage.getItem("act_ch")}]~span`
      ).innerText = msg.chat_count;
    }
  }
});
