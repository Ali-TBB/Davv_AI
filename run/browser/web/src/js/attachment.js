class Attachment {
  id;
  mime_type;
  filename;

  /**
   * Attachment class
   * @param {number} id - The attachment ID.
   * @param {string} mime_type - The attachment mime type.
   * @param {string} filename - The attachment filename.
   */
  constructor(id, mime_type, filename) {
    this.id = id;
    this.mime_type = mime_type;
    this.filename = filename;
  }

  /**
   * @returns {Attachment} JSON representation of the attachment
   */
  static fromJson(json) {
    return new Attachment(json.id, json.mime_type, json.path);
  }

  /**
   * Returns the attachment data as a JSON object.
   *
   * @returns {Object} The attachment data as a JSON object.
   */
  get json() {
    return {
      id: this.id,
      mime_type: this.mime_type,
      filename: this.filename,
    };
  }

  /**
   * Returns the HTML representation of the attachment.
   * @returns {string} The HTML code representing the attachment.
   */
  get html() {
    if (this.mime_type.startsWith("image/")) {
      return `<div class="attachment-img bg-primary"><img src="/storage/${this.filename}" alt="image"/></div>`;
    } else if (this.mime_type.startsWith("audio/")) {
      return `<audio controls>
                <source src="/storage/${this.filename}" type="${this.mime_type}">
              </audio>`;
    } else {
      return `<a href="/storage/${this.filename}" class="ml-2">${this.filename}</a>`;
    }
  }

  /**
   * Picks an image file from the user's device and uploads it to the server.
   * @returns {Promise<void>} A promise that resolves when the image is successfully uploaded.
   */
  static pickImage() {
    return new Promise((resolve, reject) => {
      const input = document.createElement("input");
      input.type = "file";
      input.accept = "image/*";
      input.onchange = (event) => {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = async (event) => {
            const base64Data = event.target.result.split(",")[1];
            const attachment = new Attachment(
              undefined,
              file.type,
              await eel.upload_file(base64Data, file.type)()
            );
            window.currentConversation.sendMessage([attachment]);
            resolve();
          };
          reader.readAsDataURL(file);
        }
      };
      input.click();
    });
  }

  /**
   * Records audio using the device's microphone.
   * @returns {Promise<MediaRecorder>} A promise that resolves to the MediaRecorder object.
   */
  static async recordAudio() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    if (!stream) return;

    const mediaRecorder = new MediaRecorder(stream);
    const chunks = [];
    mediaRecorder.ondataavailable = (event) => chunks.push(event.data);
    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunks, { type: mediaRecorder.mimeType });
      if (blob) {
        const render = new FileReader();
        render.onload = async (event) => {
          const base64Data = event.target.result.split(",")[1];
          const attachment = new Attachment(
            undefined,
            mediaRecorder.mimeType,
            await eel.upload_file(base64Data, mediaRecorder.mimeType)()
          );
          window.currentConversation.sendMessage([attachment]);
        };
        render.readAsDataURL(blob);
      }
    };

    return mediaRecorder;
  }
}

eel.expose(stopRecording);
/**
 * Stops the recording and sends the recorded audio file as an attachment in the current conversation.
 * @param {string} filename - The name of the audio file.
 */
function stopRecording(filename) {
  if (window.currentConversation)
    window.currentConversation.sendMessage(
      filename ? [new Attachment(undefined, "audio/wav", filename)] : []
    );
}
