
function $on(target, eventName, callback) {
  $(document).on(eventName, target, callback);
}

$on(".conversations-box .conversation", "click", function() {
  const conversationId = $(this).attr("conversation-id");
  Conversation.select(conversationId);
});

$on("#create-conversation", "click", function(event) {
  Conversation.create();
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