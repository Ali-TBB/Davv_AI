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
    window.conversations = {}
    $(".conversations-box .list-group").empty();
    window.currentConversation = undefined;

    const conversations = await eel.load_conversations()();
    for (let conversation of conversations) {
      const conversationObj = Conversation.fromJson(conversation);
      window.conversations[conversationObj.id] = conversationObj;
      conversationObj.attach();
    }

    if (window.currentConversation === undefined) {
      Object.values(window.conversations)[0]?.select();
    }
  }

  async loadMessages() {
    $(".conversation-box").empty();
    const messages = await eel.load_conversation(this.id)()
    for (let message of messages) {
      const messageObj = Message.fromJson(message);
      messageObj.attach();
    }
  }

  async sendMessage(attachments = []) {
    const messageContent = $(".input-group input").val();
    if (messageContent === "" && attachments.length === 0) return;
    $(".input-group input").val("");
    
    $(".input-group input").attr("disabled", true);
    $(".input-group button").attr("disabled", true);

    const message = new Message(undefined, "user", messageContent, attachments, new Date());
    message.attach();

    const answerJson = await eel.message_received(message.json)();
    console.log(answerJson);

    const answer = Message.fromJson(answerJson);
    answer.attach();

    $(".input-group input").attr("disabled", false);
    $(".input-group button").attr("disabled", false);
  }

  static async create() {
    const conversationName = prompt("Enter the conversation name:");
    if (conversationName !== null) {
      const conversationData = await eel.create_conversation(conversationName)();
      console.log(conversationData);
      if (conversationData !== null) {
        const conversation = Conversation.fromJson(conversationData);
        conversation.attach();
        conversation.select();
      }
    }
  }

  static async delete(id) {
    if (await eel.delete_conversation(id)()) {
      $(`.conversation-item[conversation-id="${id}"]`).remove(); 
      $(".conversation-box").empty();
    } else
      alert("Failed to delete the conversation");
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
    $(".input-group .btn-record").attr("disabled", false);
    $(".input-group .btn-pick-img").attr("disabled", false);
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
           class="conversation-item rounded-0 d-flex justify-content-between align-items-center px-3 py-2 border-bottom">
        <img
          src="https://ui-avatars.com/api/?name=AI&background=ddd&color=007bff&bold=true&rounded=true"
          alt="user"
          width="40"
          class="rounded-circle"
        />
        <div class="d-flex w-100 justify-content-between align-items-center">
          <div class="d-flex flex-column px-2 justify-content-center">
            <h5>
              ${this.title}
            </h5>
            <small class="date">
              ${this.created_at.toLocaleString()}
            </small>
          </div>
          <!-- menu button -->
          <button class="btn dropright" type="button" id="delete-conversation-${self.id}" data-toggle="dropdown" aria-haspopup="true">
            <i class="fas fa-ellipsis-v"></i>
            <ul class="dropdown-menu dropdown-menu-bottom" aria-labelledby="delete-conversation-${self.id}">
              <li class="dropdown-item" onclick="Conversation.delete(${this.id})">Delete</li>
            </ul>
          </button>
        </div>
      </div>
    `
  }

  attach() {
    $(".conversations-box .list-group").append(this.html);
  }
}