import base64
import time
import eel
import os
import shutil

import pyautogui

from models.attachment import Attachment
from run.browser.audio_recorder import AudioRecorder
from run.browser.browser_logger import BrowserLogger
from src.ai_conversation import AIConversation
from utils.env import Env


logger = BrowserLogger(eel)


def start():
    eel.init(os.path.join(Env.base_path, "run/browser/web"))
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
def message_received(conversation_id, message_data: dict):
    print("Message received:", message_data)

    conversation: AIConversation = AIConversation.find(
        conversation_id, logger=BrowserLogger(eel)
    )
    attachments: list[Attachment] = []
    for attachment in message_data.get("attachments", []):
        path = os.path.join(
            Env.base_path, "run/browser/uploads", attachment["filename"]
        )
        shutil.move(path, conversation.directory.path)
        attachments.append(
            Attachment.create(
                None,
                attachment["meme_type"],
                os.path.join(conversation.directory.name, attachment["filename"]),
            )
        )

    answer = conversation.handle_message(message_data["content"], attachments)
    return answer.data


@eel.expose
def upload_file(file_content):
    filename = f"tmp-{time.strftime('%Y%m%d-%H%M%S')}"
    path = os.path.join(Env.base_path, "run/browser/uploads", filename)
    header, encoded = file_content.split(",", 1)
    data = base64.b64decode(encoded)
    with open(path, "wb") as f:
        f.write(data)
    return filename


current_recording = None


@eel.expose
def start_recording():
    global current_recording
    if not current_recording:
        current_recording = AudioRecorder(
            lambda filename: eel.stopRecording(filename), False
        )
        current_recording.start()


@eel.expose
def stop_recording():
    global current_recording
    if current_recording:
        current_recording.stop()
        current_recording = None
