window.conversations = {};
window.currentConversation = undefined;

class Conversation {
  id;
  name;
  created_at;

  /**
   * Conversation class
   *
   * @param {number} id
   * @param {string} name
   * @param {Date} created_at
   */
  constructor(id, name, created_at) {
    this.id = id;
    this.name = name;
    this.created_at = created_at;
  }

  /**
   * Creates a Conversation object from a JSON representation.
   * @param {Object} json - The JSON object representing the Conversation.
   * @returns {Conversation} - The created Conversation object.
   */
  static fromJson(json) {
    return new Conversation(json.id, json.name, new Date(json.created_at));
  }

  /**
   * Retrieves all conversations and populates the conversations box.
   *
   * @returns {Promise<void>} A promise that resolves when all conversations are loaded and attached.
   */
  static async all() {
    window.conversations = {};
    $(".conversations-box .list-group").empty();
    window.currentConversation = undefined;

    const conversations = await eel.load_conversations()();
    for (let conversation of conversations) {
      const conversationObj = Conversation.fromJson(conversation);
      window.conversations[conversationObj.id] = conversationObj;
      conversationObj.attach();
    }

    const all = Object.values(window.conversations);
    if (window.currentConversation === undefined && all.length > 0)
      all[all.length - 1].select();
  }

  /**
   * Loads the messages of the conversation.
   * @returns {Promise<void>} A promise that resolves when the messages are loaded.
   */
  async loadMessages() {
    $(".conversation-messages").empty();

    for (let message of await eel.load_conversation(this.id)())
      Message.fromJson(message).attach();

    this.scrollDown();
  }

  /**
   * Sends a message and handles the response.
   * @param {Array} attachments - An array of attachments.
   * @returns {Promise<void>} - A promise that resolves when the message is sent and response is handled.
   */
  async sendMessage(attachments = []) {
    const messageContent = $(".input-group input").val();
    if (messageContent !== "" || attachments.length > 0) {
      $(".input-group input").val("");

      $(".input-group input").attr("disabled", true);
      $(".input-group button").attr("disabled", true);

      const result = await eel.message_received(
        new Message(undefined, "user", messageContent, attachments, new Date())
          .json
      )();

      const message = Message.fromJson(result.message);
      message.attach();

      const answer = Message.fromJson(result.answer);
      answer.attach();

      this.scrollDown();

      speech(answer.content);

      // playAudio(`/storage/conv-${this.id}/answer-${result.answer.id}.mp3`);
    }

    $(".input-group input").attr("disabled", false);
    if (window.streamRecording) {
      $(".input-group .btn-record").html("<i class='fas fa-stop'></i>");
      $(".input-group .btn-record").addClass("btn-danger");
      $(".input-group .btn-record").attr("disabled", true);
    } else {
      $(".input-group .btn-record").html("<i class='fas fa-microphone'></i>");
      $(".input-group .btn-record").removeClass("btn-danger");
      $(".input-group .btn-record").attr("disabled", false);
    }
    $(".input-group .btn-pick-img").attr("disabled", false);
    $("#btn-settings").attr("disabled", false);
  }

  /**
   * Creates a new conversation.
   * @returns {Promise<void>} A promise that resolves when the conversation is created.
   */
  static async create() {
    const conversationName = prompt("Enter the conversation name:");
    if (conversationName !== null) {
      const conversationData = await eel.create_conversation(
        conversationName
      )();
      if (conversationData !== null) {
        const conversation = Conversation.fromJson(conversationData);
        conversation.attach();
        conversation.select();
      }
    }
  }

  /**
   * Deletes a conversation by its ID.
   * @param {number} id - The ID of the conversation to delete.
   * @returns {Promise<void>} - A promise that resolves when the conversation is deleted successfully.
   */
  static async delete(id) {
    if (await eel.delete_conversation(id)()) {
      $(`.conversation-item[conversation-id="${id}"]`).remove();
      console.log(window.currentConversation, id);
      if (window.currentConversation.id == id) {
        $(".conversation-messages").empty();
        $(".input-group input").attr("disabled", true);
        $(".input-group button").attr("disabled", true);
        $("#btn-settings").attr("disabled", true);
      }
    } else alert("Failed to delete the conversation");
  }

  /**
   * Selects the current conversation and performs necessary UI updates.
   * @returns {Promise<void>} A promise that resolves when the conversation is selected.
   */
  async select() {
    window.currentConversation = this;
    $(".input-group input").attr("disabled", true);
    $(".input-group button").attr("disabled", true);
    $("#btn-settings").attr("disabled", true);

    $(".conversation-messages").empty();

    $(`.conversation-item`).removeClass("active");
    $(`.conversation-item`).removeClass("text-white");
    $(`.conversation-item`).addClass("list-group-item-light");

    // $(".conversation-box .header h3").text(this.name);

    await this.loadMessages();

    $(`.conversation-item[conversation-id="${this.id}"]`).addClass("active");
    $(`.conversation-item[conversation-id="${this.id}"]`).addClass(
      "text-white"
    );
    $(`.conversation-item[conversation-id="${this.id}"]`).removeClass(
      "list-group-item-light"
    );

    $(".input-group input").attr("disabled", false);
    if (window.streamRecording) {
      $(".input-group .btn-record").html("<i class='fas fa-stop'></i>");
      $(".input-group .btn-record").addClass("btn-danger");
      $(".input-group .btn-record").attr("disabled", true);
    } else {
      $(".input-group .btn-record").html("<i class='fas fa-microphone'></i>");
      $(".input-group .btn-record").removeClass("btn-danger");
      $(".input-group .btn-record").attr("disabled", false);
    }
    $(".input-group .btn-pick-img").attr("disabled", false);
    $("#btn-settings").attr("disabled", false);
  }

  /**
   * Selects a conversation by its ID.
   *
   * @param {string} conversationId - The ID of the conversation to select.
   */
  static select(conversationId) {
    if (
      window.currentConversation &&
      window.currentConversation.id === conversationId
    )
      return;

    /**
     *  @type {Conversation}
     */
    const conversation = window.conversations[conversationId];

    conversation.select();
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
              ${this.name}
            </h5>
            <small class="date">
              ${this.created_at.toLocaleString()}
            </small>
          </div>
          <!-- menu button -->
          <button class="btn bg-transparent dropright" type="button" id="delete-conversation-${
            self.id
          }" data-toggle="dropdown" aria-haspopup="true">
            <i class="fas fa-ellipsis-v"></i>
            <ul class="dropdown-menu dropdown-menu-bottom" aria-labelledby="delete-conversation-${
              self.id
            }">
              <li class="dropdown-item" onclick="Conversation.delete(${
                this.id
              })">Delete</li>
            </ul>
          </button>
        </div>
      </div>
    `;
  }

  /**
   * Attaches the HTML content of the conversation to the conversations box.
   */
  attach() {
    $(".conversations-box .list-group").append(this.html);
  }

  /**
   * Scrolls down the conversation messages.
   * @async
   * @function scrollDown
   * @returns {Promise<void>}
   */
  async scrollDown() {
    await delay(5);
    const conversationBox = $(".conversation-messages");
    conversationBox.scrollTop(conversationBox.prop("scrollHeight"));
  }
}
