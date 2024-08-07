class Message {

  id
  role
  content
  attachments
  created_at

  /**
   *  Message class
   * @param {number} id
   * @param {string} role
   * @param {string} content
   * @param {Attachment[]} attachments
   * @param {Date} created_at 
   */
  constructor(id, role, content, attachments, created_at) {
    this.id = id
    this.role = role
    this.content = content
    this.attachments = attachments
    this.created_at = created_at
  }

  /**
   * @returns {Message} JSON representation of the message
   */
  static fromJson(json) {
    return new Message(json.id, json.role, json.content, json.attachments, new Date(json.created_at))
  }

  get json() {
    return {
      id: this.id,
      role: this.role,
      content: this.content,
      attachments: this.attachments,
      created_at: this.created_at.getMilliseconds()
    }
  }

  /**
   * @returns {string} HTML representation of the message
   */
  get html() {
    return {
      model: `<div class="message-item media mb-3">
              <img
                src="https://bootstrapious.com/i/snippets/sn-conversation/avatar.svg"
                alt="user"
                width="50"
                class="rounded-circle"
              />
              <div class="media-body ml-3">
                <div class="message-content bg-light rounded py-2 px-3 mb-2">
                  <p class="text-small mb-0 text-muted">
                    ${this.content}
                  </p>
                </div>
                <p class="small text-muted">
                  ${this.created_at.toLocaleString()}
                </p>
              </div>
            </div>`,
      user: `<div class="message-item media ml-auto mb-3">
              <div class="media-body">
                <div class="message-content bg-primary rounded py-2 px-3 mb-2 ml-auto">
                  <p class="text-small mb-0 text-white">
                    ${this.content}
                  </p>
                </div>
                <p class="small text-muted">
                  ${this.created_at.toLocaleString()}
                </p>
              </div>
            </div>`
    }[this.role]
  }

  toString() {
    return `${this.role}: ${this.content} - ${this.created_at}`
  }

}