var running = false;

function send() {
  if (running == true) return;
  var msg = document.getElementById("message").value;
  if (msg == "") return;
  running = true;
  addMsg(msg);


  $.ajax({
    url: '/query',
    method: 'post',
    data: {
      'queryText': msg
    },


    success: async function (result) {
      result = JSON.parse(result);
      
      var simpleMessages=result.simpleMessages
      var suggestionsMessages=result.suggestionsMessages
      var listsMessages=result.listsMessages

      var i, len, text;
      for (i = 0, len = simpleMessages.length, text = ""; i < len; i++) {
        addResponseLoader()
        await new Promise(resolve => setTimeout(resolve, 1000));
        removeResponseLoader()
        addResponseMsg(simpleMessages[i])
      }

      var i, len, text;
      for (i = 0, len = suggestionsMessages.length, text = ""; i < len; i++) {
        addResponseLoader()
        await new Promise(resolve => setTimeout(resolve, 1000));
        removeResponseLoader()
        addSuggestionsMessages(suggestionsMessages[i])
      }
   
      

    }
  })


}
function clickSend(msg) {
  if (running == true) return;
  
  if (msg == "") return;
  running = true;
  addMsg(msg);


  $.ajax({
    url: '/query',
    method: 'post',
    data: {
      'queryText': msg
    },


    success: async function (result) {
      result = JSON.parse(result);
      
      var simpleMessages=result.simpleMessages
      var suggestionsMessages=result.suggestionsMessages

      let i, len, text;

      // console.log(result);

      for (i = 0, len = simpleMessages.length, text = ""; i < len; i++) {
        addResponseLoader()
        await new Promise(resolve => setTimeout(resolve, 1000));
        removeResponseLoader()
        addResponseMsg(simpleMessages[i])
      }


      for (i = 0, len = suggestionsMessages.length, text = ""; i < len; i++) {
        addResponseLoader()
        await new Promise(resolve => setTimeout(resolve, 1000));
        removeResponseLoader()
        addSuggestionsMessages(suggestionsMessages[i])
      }
      var listsMessages=result.listsMessages
      
      if(listsMessages.length>0){
        console.log(result.listsMessages);
        addResponseLoader()
        await new Promise(resolve => setTimeout(resolve, 1000));
        removeResponseLoader()
        addListsMessages(listsMessages)
      }
      

    }
  })


}



function addMsg(msg) {
  var div = document.createElement("div");
  div.innerHTML =
    "<span style='flex-grow:1'></span><div class='chat-message-sent'>" +
    msg +
    "</div>";
  div.className = "chat-message-div";
  document.getElementById("message-box").appendChild(div);
  //SEND MESSAGE TO API
  document.getElementById("message").value = "";
  document.getElementById("message-box").scrollTop = document.getElementById(
    "message-box"
  ).scrollHeight;
}
function addResponseMsg(msg) {
  var div = document.createElement("div");
  div.innerHTML = "<div class='chat-message-received'>" + msg + "</div>";
  div.className = "chat-message-div";
  document.getElementById("message-box").appendChild(div);
  document.getElementById("message-box").scrollTop = document.getElementById(
    "message-box"
  ).scrollHeight;
  running = false;
}


function addSuggestionsMessages(msg) {
  var div = document.createElement("div");
  div.innerHTML = "<div class='chat-message-received' style='cursor:pointer;background-color:#c0dddd;' onclick='clickSend("+'"'+msg+'"'+")'>" + msg + "</div>";
  div.className = "chat-message-div";
  document.getElementById("message-box").appendChild(div);
  document.getElementById("message-box").scrollTop = document.getElementById(
    "message-box"
  ).scrollHeight;
  running = false;
}
function addListsMessages(msgs) {
  var div = document.createElement("div");
  console.log('msgs');
  var i, len, text; 
  myhtml= "<div class='chat-message-received' style='cursor:pointer;background-color:#c0dddd;'><ul style='padding-left: 15px;'>";
  for (i = 0, len = msgs.length, text = ""; i < len; i++) {
    myhtml=myhtml+'<li>'+msgs[i]+'</li>';
    }

    myhtml+='</ul></div>';
  
    div.innerHTML=myhtml;

  div.className = "chat-message-div";
  document.getElementById("message-box").appendChild(div);
  document.getElementById("message-box").scrollTop = document.getElementById(
    "message-box"
  ).scrollHeight;
  running = false;
}


function addResponseLoader() {
  var div = document.createElement("div");
  div.innerHTML = "<div class='chat-message-received' id='loader_active'><div class='loader' ><span></span><span></span><span></span></div></div>";
  div.className = "chat-message-div";
  document.getElementById("message-box").appendChild(div);
  document.getElementById("message-box").scrollTop = document.getElementById(
    "message-box"
  ).scrollHeight;
  running = false;
}


function removeResponseLoader() {

  // document.getElementById("message-box").removeChild('loader_active');

  $("#loader_active").remove()
  
}




document.getElementById("message").addEventListener("keyup", function (event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    send();
  }
});
 document.getElementById("chatbot_toggle").onclick = function () {
    if (document.getElementById("chatbot").classList.contains("collapsed")) {
      document.getElementById("chatbot").classList.remove("collapsed")
      document.getElementById("chatbot_toggle").children[0].style.display = "none"
      document.getElementById("chatbot_toggle").children[1].style.display = ""
      
    }
    else {
      document.getElementById("chatbot").classList.add("collapsed")
      document.getElementById("chatbot_toggle").children[0].style.display = ""
      document.getElementById("chatbot_toggle").children[1].style.display = "none"
    }
  }


















