eel.expose(log)
function log(level, message) {
  console.log(`[${level}] ${message}`)
}

function $on(target, eventName, callback) {
  $(document).on(eventName, target, callback);
}

$on(".conversations-box .conversation-item", "click", function() {
  const conversationId = $(this).attr("conversation-id");
  
  if (window.currentConversation && window.currentConversation.id == conversationId) return;
  
  Conversation.select(conversationId);
});

$on("#create-conversation", "click", function() {
  Conversation.create();
});

$on(".input-group input", "input", function() {
  $(".input-group .btn-send").attr("disabled", !$(this).val());
});

$on(".input-group .btn-send", "click", function() {
  window.currentConversation?.sendMessage();
});

$on(".input-group .btn-record", "mousedown", function() {
  if (!window.currentConversation) return;
  eel.start_recording()()
});

$on(".input-group .btn-record", "mouseup", function() {
  if (!window.currentConversation) return;
  eel.stop_recording()()
});

$(document).ready(function() {
  Conversation.all() 
});

$on(".conversation .expand-btn", "click", function() {
  $(".conversation").toggleClass("expanded");
});