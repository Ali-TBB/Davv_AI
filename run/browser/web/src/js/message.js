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
   * @returns {Message} JSON representation of the message
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
      <p class="text-small mb-0 ${
        this.role == "user" ? "text-white" : "text-muted"
      }">
        ${this.content}
      </p>
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

  async attach() {
    const conversationBox = $(".conversation-messages");
    conversationBox.append(this.html);
  }
}
