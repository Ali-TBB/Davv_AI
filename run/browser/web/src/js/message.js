class Message {
  id;
  role;
  content;
  attachments;
  created_at;

  /**
   *  Message class
   * @param {number} id
   * @param {string} role
   * @param {string} content
   * @param {Attachment[]} attachments
   * @param {Date} created_at
   */
  constructor(id, role, content, attachments, created_at) {
    this.id = id;
    this.role = role;
    this.content = content;
    this.attachments = attachments;
    this.created_at = created_at;
  }

  /**
   * Creates a new Message object from a JSON representation.
   * @param {Object} json - The JSON object representing the Message.
   * @returns {Message} - The created Message object.
   */
  static fromJson(json) {
    return new Message(
      json.id,
      json.role,
      json.content,
      json.attachments.map((attachment) => Attachment.fromJson(attachment)),
      new Date(json.created_at)
    );
  }

  /**
   * Returns the JSON representation of the message.
   * @returns {Object} The JSON representation of the message.
   */
  get json() {
    return {
      id: this.id,
      role: this.role,
      content: this.content,
      attachments: this.attachments.map((attachment) => attachment.json),
      created_at: this.created_at.getMilliseconds(),
    };
  }

  /**
   * @returns {string} HTML representation of the message
   */
  get html() {
    const contentHtml = this.content
      ? `
    <div class="message-content rounded py-2 px-3 mb-2 ${
      this.role == "user" ? "bg-primary ml-auto" : "bg-light"
    }">
      <div class="text-small mb-0 ${
        this.role == "user" ? "text-white" : "text-muted"
      }">
          ${marked.parse(this.content)}
      </div>
    </div>`
      : "";
    const attachmentsHtml = this.attachments
      .map((attachment) => attachment.html)
      .join("");
    return {
      model: `<div class="message-item media mb-3">
              <img
                src="https://ui-avatars.com/api/?name=AI&background=ddd&color=007bff&bold=true&rounded=true"
                alt="user"
                width="50"
                class="rounded-circle"
              />
              <div class="media-body ml-3">
                ${contentHtml}
                ${attachmentsHtml}
                <p class="small text-muted">
                  ${this.created_at.toLocaleString()}
                </p>
              </div>
            </div>`,
      user: `<div class="message-item media ml-auto mb-3">
              <div class="media-body">
                ${contentHtml}
                ${attachmentsHtml}
                <p class="small text-muted">
                  ${this.created_at.toLocaleString()}
                </p>
              </div>
            </div>`,
    }[this.role];
  }

  /**
   * Attaches the HTML content of the message to the conversation box.
   * @returns {Promise<void>} A promise that resolves when the HTML content is attached.
   */
  async attach() {
    const conversationBox = $(".conversation-messages");
    conversationBox.append(this.html);
  }
}
