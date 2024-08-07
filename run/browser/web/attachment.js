class Attachment {

  id
  mime_type
  filename

  /**
   * Attachment class
   * @param {number} id
   * @param {string} mime_type
   * @param {string} filename
   */
  constructor(id, mime_type, filename) {
    this.id = id
    this.mime_type = mime_type
    this.filename = filename
  }

  /**
   * @returns {Attachment} JSON representation of the attachment
   */
  static fromJson(json) {
    console.log(json);
    return new Attachment(json.id, json.mime_type, json.path)
  }

  get json() {
    return {
      id: this.id,
      mime_type: this.mime_type,
      filename: this.filename
    }
  }

  get html() {
    console.log(this.mime_type);
    if (this.mime_type.startsWith("image/")) {
      return `<img src="storage/${this.filename}" alt="image" class="img-fluid rounded ml-2" width="100" />`
    } else if (this.mime_type.startsWith("audio/")) {
      return `<audio controls class="ml-2">
                <source src="storage/${this.filename}" type="${this.mime_type}">
              </audio>`
    } else {
      return `<a href="storage/${this.filename}" class="ml-2">${this.filename}</a>`
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
