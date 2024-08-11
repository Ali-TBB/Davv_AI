eel.expose(log);
function log(level, message) {
  console.log(`[${level}] ${message}`);
}

function $on(target, eventName, callback) {
  $(document).on(eventName, target, callback);
}

$on(".conversations-box .conversation-item", "click", function () {
  const conversationId = $(this).attr("conversation-id");

  if (
    window.currentConversation &&
    window.currentConversation.id == conversationId
  )
    return;

  Conversation.select(conversationId);
});

$on("#create-conversation", "click", function () {
  Conversation.create();
});

$on(".input-group input", "input", function () {
  $(".input-group .btn-send").attr("disabled", !$(this).val());
});

$on(".input-group input", "keypress", function (e) {
  if (e.which == 13) window.currentConversation?.sendMessage();
});

$on(".input-group .btn-send", "click", function () {
  window.currentConversation?.sendMessage();
});

$on(".input-group .btn-record", "mousedown", async function () {
  if (!window.currentConversation || window.streamRecording) return;

  $(".input-group .btn-record").html("<i class='fas fa-stop'></i>");
  $(".input-group .btn-record").addClass("btn-danger");

  await eel.start_recording()();
});

$on(".input-group .btn-record", "mouseup", async function () {
  if (!window.currentConversation || window.streamRecording) return;

  await eel.stop_recording()();

  $(".input-group .btn-record").html("<i class='fas fa-microphone'></i>");
  $(".input-group .btn-record").removeClass("btn-danger");
});

$(document).ready(function () {
  Conversation.all();
});

$on(".conversation .expand-btn", "click", function () {
  $(".conversation").toggleClass("expanded");
});

window.streamRecording = false;
$on(".header .dropdown-menu #stream-recording", "click", async function () {
  window.streamRecording = await eel.streaming_recording()();
  $(this).html(
    window.streamRecording ? "Stop Stream Recording" : "Start Stream Recording"
  );

  if (window.streamRecording) {
    $(".input-group .btn-record").html("<i class='fas fa-stop'></i>");
    $(".input-group .btn-record").addClass("btn-danger");
    $(".input-group .btn-record").attr("disabled", true);
  } else {
    $(".input-group .btn-record").html("<i class='fas fa-microphone'></i>");
    $(".input-group .btn-record").removeClass("btn-danger");
    $(".input-group .btn-record").attr("disabled", false);
  }
});

$on(".message-item .attachment-img img", "click", function () {
  $("#image-preview-modal img").attr("src", $(this).attr("src"));
  $("#image-preview-modal").modal("show");
});

eel.expose(playAudio);
function playAudio(src) {
  console.log("Playing audio", src);
  // const audio = new Audio(src);
  // audio.play();

  const audio = document.createElement("audio");
  audio.src = src;
  return audio.play();
}

function delay(ms) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve();
    }, ms);
  });
}

function getVoice(name) {
  return window.speechSynthesis
    .getVoices()
    .find((voice) => voice.name === name);
}

const synth = window.speechSynthesis;
function speech(text) {
  if (synth.speaking) {
    console.error("speechSynthesis.speaking");
    return;
  }
  if (text !== "") {
    const utterThis = new SpeechSynthesisUtterance(text);
    // utterThis.lang = "en-US";
    // utterThis.rate = 1;
    // utterThis.pitch = 1;
    utterThis.voice = getVoice("Google US English");
    // utterThis.voice = getVoice(
    //   "Microsoft AndrewMultilingual Online (Natural) - English (United States)"
    // );
    utterThis.onstart = function (event) {
      console.log("SpeechSynthesisUtterance.onstart");
    };
    utterThis.onend = function (event) {
      console.log("SpeechSynthesisUtterance.onend");
    };
    utterThis.onerror = function (event) {
      console.error("SpeechSynthesisUtterance.onerror");
    };
    synth.speak(utterThis);
  }
}
