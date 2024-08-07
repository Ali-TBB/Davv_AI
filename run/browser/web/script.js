eel.expose(log)
function log(level, message) {
  console.log(`[${level}] ${message}`)
}

function $on(target, eventName, callback) {
  $(document).on(eventName, target, callback);
}

$on(".conversations-box .conversation-item", "click", function() {
  const conversationId = $(this).attr("conversation-id");
  Conversation.select(conversationId);
});

$on("#create-conversation", "click", function() {
  Conversation.create();
});

$on(".input-group input", "change", function() {
  if ($(this).val()) {
    $(".input-group button").attr("disabled", false);
  }
});

$on(".input-group button", "click", function() {
  window.currentConversation.sendMessage();
});

$(document).ready(function() {
  Conversation.all() 
});

$on(".conversation .expand-btn", "click", function() {
  $(".conversation").toggleClass("expanded");
});