import eel
import os

import pyautogui

from run.browser.audio_recorder import AudioRecorder
from run.browser.browser_logger import BrowserLogger
from src.ai_conversation import AIConversation


PKG_DIR = os.path.dirname(os.path.abspath(__file__))


logger = BrowserLogger(eel)


def start():
    eel.init(os.path.join(PKG_DIR, "web"))
    w, h = pyautogui.size()
    eel.start("index.html", mode="edge", app_mode=True, size=(w * 0.6, h))


@eel.expose
def create_conversation(name):
    return AIConversation.new(name, logger=logger).data


@eel.expose
def delete_conversation(conversation_id):
    return AIConversation.find(conversation_id).delete()


@eel.expose
def load_conversations():
    return [item.data for item in AIConversation.all(logger=logger)]


@eel.expose
def load_conversation(conversation_id):
    conversation = AIConversation.find(conversation_id)
    return [item.data for item in conversation.messages()]


@eel.expose
def messageReceived(conversation_id, message_data):
    print("Message received:", message_data)

    conversation: AIConversation = AIConversation.find(
        conversation_id, logger=BrowserLogger(eel)
    )
    answer = conversation.handle_message(
        message_data["content"], message_data["attachments"]
    )
    return answer.data


@eel.expose
def pick_image():
    import tkinter as tk
    from tkinter import filedialog

    tk.Tk().withdraw()
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg")])
    if path:
        import time
        import shutil

        filename = f"img-{time.strftime('%Y%m%d-%H%M%S')}.{path.split('.')[-1]}"

        shutil.copy(path, os.path.join(PKG_DIR, "web/uploads/", filename))
        return filename


current_recording = None


@eel.expose
def start_recording():
    global current_recording
    if not current_recording:
        current_recording = AudioRecorder(
            lambda filename: eel.stopRecording(filename),
        )
        current_recording.start()

    raise Exception("Already recording")


@eel.expose
def stop_recording():
    global current_recording
    if current_recording:
        current_recording.stop()
        current_recording = None

    raise Exception("Not recording")
