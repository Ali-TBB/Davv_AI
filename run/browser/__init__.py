import os
import eel

import pyautogui

from run.browser.browser_logger import BrowserLogger
from src.ai_conversation import AIConversation


PKG_DIR = os.path.dirname(os.path.abspath(__file__))


logger = BrowserLogger(eel)


def start():
    eel.init(os.path.join(PKG_DIR, "web"))
    w, h = pyautogui.size()
    eel.start("index.html", mode="edge", app_mode=True, size=(w * 0.6, h))


@eel.expose
def createConversation(name):
    return AIConversation.new(name, logger=logger).data


@eel.expose
def deleteConversation(conversationId):
    return AIConversation.find(conversationId).delete()


@eel.expose
def loadConversations():
    return [item.data for item in AIConversation.all(logger=logger)]


@eel.expose
def loadConversationMessages(conversationId):
    conversation = AIConversation.find(conversationId)
    return [item.data for item in conversation.messages()]


@eel.expose
def messageReceived(conversationId, messageData):
    print("Message received:", messageData)

    conversation: AIConversation = AIConversation.find(
        BrowserLogger(eel), conversationId
    )
    answer = conversation.handle_message(
        messageData["content"], messageData["attachments"]
    )
    return answer.data
