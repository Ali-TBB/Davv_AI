window.conversations = {}
window.currentConversation = undefined

class Conversation {

  id
  title
  created_at

  /**
   * Conversation class
   * 
   * @param {number} id 
   * @param {string} name 
   * @param {Date} created_at 
   */
  constructor(id, name, created_at) {
    this.id = id
    this.title = name
    this.created_at = created_at
  }

  /**
   * @returns {Object} JSON representation of the conversation
   */
  static fromJson(json) {
    return new Conversation(json.id, json.name, new Date(json.created_at))
  }

  static async all() {
    const conversations = await eel.loadConversations()();
    for (let conversation of conversations) {
      const conversationObj = Conversation.fromJson(conversation);
      window.conversations[conversationObj.id] = conversationObj;
      $(".conversations-box .list-group").append(conversationObj.html);
      if (window.currentConversation === undefined) {
        window.currentConversation = conversationObj;
        conversationObj.select();
      }
    }
  }

  async loadMessages() {
    $(".conversation-box").empty();
    const messages = await eel.loadConversationMessages(this.id)()
    for (let message of messages) {
      const messageObj = Message.fromJson(message);
      $(".conversation-box").append(messageObj.html);
    }
  }

  async sendMessage() {
    const messageContent = $(".input-group input").val();
    if (messageContent === "") return;
    $(".input-group input").val("");
    
    $(".input-group input").attr("disabled", true);
    $(".input-group button").attr("disabled", true);

    const message = new Message(undefined, "user", messageContent, [], new Date());
    $(".conversation-box").append(message.html);

    const answerJson = await eel.messageReceived(this.id, message.json)();

    const answer = Message.fromJson(answerJson);
    $(".conversation-box").append(answer.html);

    $(".input-group input").attr("disabled", false);
    $(".input-group button").attr("disabled", false);
  }

  static async create() {
    const conversationName = prompt("Enter the conversation name:");
    if (conversationName !== null) {
      const conversationData = await eel.createConversation(conversationName)();
      console.log(conversationData);
      if (conversationData !== null) {
        const conversation = Conversation.fromJson(conversationData);
        $(".conversations-box").append(conversation.html);
        conversation.select();
      }
    }
  }

  static async delete(id) {
    $(`.conversation-item[conversation-id="${id}"] .btn-danger`).attr("disabled", true)
    if (await eel.deleteConversation(id)()) {
      $(`.conversation-item[conversation-id="${id}"]`).remove(); 
      $(".conversation-box").empty();
    } else 
      $(`.conversation-item[conversation-id="${id}"] .btn-danger`).attr("disabled", false)
  }

  async select() {
    window.currentConversation = this;
    $(".input-group input").attr("disabled", true);
    $(".input-group button").attr("disabled", true);

    $(".conversation-box").empty();

    $(`.conversation-item`).removeClass("active");
    $(`.conversation-item`).removeClass("text-white");
    $(`.conversation-item`).addClass("list-group-item-light");

    await this.loadMessages();

    $(`.conversation-item[conversation-id="${this.id}"]`).addClass("active");
    $(`.conversation-item[conversation-id="${this.id}"]`).addClass("text-white");
    $(`.conversation-item[conversation-id="${this.id}"]`).removeClass("list-group-item-light");
    
    $(".input-group input").attr("disabled", false);
    $(".input-group button").attr("disabled", false);
  }

  static select(conversationId) {
    if (window.currentConversation && window.currentConversation.id === conversationId) return;

    /**
     *  @type {Conversation
     */
    const conversation = window.conversations[conversationId];

    conversation.select()
  }

  /**
   * @returns {string} HTML representation of the conversation
   */
  get html() {
    return `
      <div conversation-id="${this.id}"
           class="conversation-item list-group-item list-group-item-action list-group-item-light rounded-0 d-flex justify-content-between align-items-center">
        <div class="media px-2">
          <img
            src="https://bootstrapious.com/i/snippets/sn-conversation/avatar.svg"
            alt="user"
            width="50"
            class="rounded-circle"
          />
        </div>
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1">
              ${this.title}
          </h5>
          <small class="date mb-0 px-2 gp-5">
            ${this.created_at.toLocaleString()}
            <button class="btn btn-danger btn-sm btn-circle"
                    onclick="Conversation.delete(${this.id})">
              x
            </button>
          </small>
        </div>
      </div>
    `
  }
}