class Attachment {

  id
  meme_type
  filename

  /**
   * Attachment class
   * @param {number} id
   * @param {string} meme_type
   * @param {string} filename
   */
  constructor(id, meme_type, filename) {
    this.id = id
    this.meme_type = meme_type
    this.filename = filename
  }

  /**
   * @returns {Attachment} JSON representation of the attachment
   */
  static fromJson(json) {
    return new Attachment(json.id, json.meme_type, json.filename)
  }

  get json() {
    return {
      id: this.id,
      meme_type: this.meme_type,
      filename: this.filename
    }
  }

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
            const attachment = new Attachment(undefined, file.type, await eel.upload_file(event.target.result)())
            window.currentConversation.sendMessage([attachment])
            resolve()
          }
          reader.readAsDataURL(file);
        }
      }
      input.click();
    });
  }

}

eel.expose(stopRecording)
function stopRecording(filename) {
  window.currentConversation.sendMessage([new Attachment(undefined, "audio/wav", filename)])
}
