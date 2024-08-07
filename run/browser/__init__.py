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
    link_storage()
    eel.init(os.path.join(Env.base_path, "run/browser/web"))
    w, h = pyautogui.size()
    eel.start("index.html", app_mode=True, size=(w * 0.6, h))


def link_storage():
    source = os.path.join(Env.base_path, "storage")
    link_name = os.path.join(Env.base_path, "run/browser/storage")
    # Check if the symlink already exists
    if os.path.islink(link_name) or os.path.exists(link_name):
        try:
            os.remove(link_name)
            print(f"Existing symlink or file removed: {link_name}")
        except OSError as e:
            print(f"Error removing existing symlink or file: {e}")

    # Create the new symlink
    try:
        os.symlink(source, link_name)
        print(f"Symlink created: {link_name} -> {source}")
    except OSError as e:
        print(f"Error creating symlink: {e}")


current_conversation: AIConversation = None


@eel.expose
def create_conversation(name):
    global current_conversation

    current_conversation = AIConversation.new(name, logger=logger)
    current_conversation.init()
    return current_conversation.data


@eel.expose
def delete_conversation(conversation_id):
    global current_conversation

    if current_conversation and current_conversation.id == conversation_id:

        if current_conversation.delete():
            current_conversation = None
            return True
        return False
    else:
        return AIConversation.find(conversation_id).delete()


@eel.expose
def load_conversations():
    return [item.data for item in AIConversation.all(logger=logger)]


@eel.expose
def load_conversation(conversation_id):
    global current_conversation

    current_conversation = AIConversation.find(conversation_id, logger=logger)
    if current_conversation:
        current_conversation.init()
        return [item.data for item in current_conversation.messages()]
    return []


@eel.expose
def message_received(message_data: dict):
    print("Message received:", message_data)

    attachments: list[Attachment] = []
    for attachment in message_data.get("attachments", []):
        path = os.path.join(
            Env.base_path, "run/browser/uploads", attachment["filename"]
        )
        shutil.move(path, current_conversation.directory.path)
        attachments.append(
            Attachment.create(
                None,
                attachment["meme_type"],
                os.path.join(
                    current_conversation.directory.name, attachment["filename"]
                ),
            )
        )

    answer = current_conversation.handle_message(message_data["content"], attachments)
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
