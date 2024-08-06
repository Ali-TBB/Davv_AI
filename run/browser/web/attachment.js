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

}