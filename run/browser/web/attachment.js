class Attachment {

  id
  type
  path

  /**
   * Attachment class
   * @param {number} id
   * @param {string} type
   * @param {string} path
   */
  constructor(id, type, path) {
    this.id = id
    this.type = type
    this.path = path
  }

  /**
   * @returns {Attachment} JSON representation of the attachment
   */
  static fromJson(json) {
    return new Attachment(json.id, json.type, json.path)
  }

  static async pickImage() {
    filename = await eel.pick_image()()
    if (filename) {
      const attachment = new Attachment(undefined, "image/*", filename)
      window.currentConversation.sendMessage([attachment])
    }
  }

  static recordVoice() {
    eel.start_recording()()
  }

  static stopRecording() {
    eel.stop_recording()()
  }

}

eel.expose(stopRecording)
function stopRecording(filename) {
  window.currentConversation.sendMessage([new Attachment(undefined, "audio/*", filename)])
}
