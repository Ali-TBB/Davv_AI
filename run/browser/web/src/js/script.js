eel.expose(log);
/**
 * Logs a message to the console.
 *
 * @param {string} level
 * @param {string} message
 */
function log(level, message) {
  console.log(`[${level}] ${message}`);
}

/**
 * Attaches an event listener to the specified target element(s).
 *
 * @param {string} target - The target element(s) to attach the event listener to.
 * @param {string} eventName - The name of the event to listen for.
 * @param {function} callback - The callback function to execute when the event is triggered.
 */
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

window.currentRecorder = null;
$on(".input-group .btn-record", "mousedown", async function () {
  if (
    !window.currentConversation ||
    window.streamRecording
    // ||window.currentRecorder
  )
    return;

  await eel.start_recording()();
  // window.currentRecorder = await Attachment.recordAudio();

  // if (!window.currentRecorder) return;
  // playAudio("/src/media/start-recording.wav");
  // window.currentRecorder.start();

  $(".input-group .btn-record").html("<i class='fas fa-stop'></i>");
  $(".input-group .btn-record").addClass("btn-danger");
});

$on(".input-group .btn-record", "mouseup", async function () {
  if (
    !window.currentConversation ||
    window.streamRecording
    // || !window.currentRecorder
  )
    return;

  await eel.stop_recording()();
  // playAudio("/src/media/end-recording.wav");
  // window.currentRecorder.stop();
  // window.currentRecorder = null;

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

// eel.expose(playAudio);
/**
 * Plays an audio file.
 *
 * @param {string} src
 * @returns {Promise<void>}
 */
function playAudio(src) {
  console.log("Playing audio", src);
  // const audio = new Audio(src);
  // audio.play();

  const audio = document.createElement("audio");
  audio.src = src;
  return audio.play();
}

/**
 * Delays the execution for a specified amount of time.
 * @param {number} ms - The delay time in milliseconds.
 * @returns {Promise} - A promise that resolves after the delay.
 */
function delay(ms) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve();
    }, ms);
  });
}

/**
 * Retrieves a specific voice from the available voices.
 * @param {string} name - The name of the voice to retrieve.
 * @returns {SpeechSynthesisVoice|undefined} The voice object matching the specified name, or undefined if not found.
 */
function getVoice(name) {
  return window.speechSynthesis
    .getVoices()
    .find((voice) => voice.name === name);
}

/**
 * Speaks the given text using the SpeechSynthesis API.
 * @param {string} text - The text to be spoken.
 */
function speech(text) {
  const synth = window.speechSynthesis;
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
