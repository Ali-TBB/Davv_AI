import base64
import time
import eel
import os
import shutil

from gtts import gTTS
import pyautogui

from models.attachment import Attachment
from run.browser import audio_effect
from run.browser.audio_recorder import AudioRecorder
from run.browser.browser_logger import BrowserLogger
from run.browser.streaming_record import StreamingRecord
from src.ai_conversation import AIConversation
from utils.env import Env


logger = BrowserLogger(eel)


def start():
    eel.init(os.path.join(Env.base_path, "run/browser/web"))
    w, h = pyautogui.size()
    eel.start("index.html", app_mode=True, size=(w * 0.6, h), close_callback=on_close)


def on_close(page, sockets):
    print("Closing page", page, sockets)

    if streaming_record:
        streaming_record.stop()

    if current_recording:
        current_recording.stop()

    exit()


current_conversation: AIConversation = None


@eel.expose
def create_conversation(name):
    global current_conversation

    current_conversation = AIConversation.new(name, logger=logger)
    current_conversation.init()
    return current_conversation.__dict__()


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
    return [
        item.__dict__() for item in AIConversation.all(logger=logger, order_type="DESC")
    ]


@eel.expose
def load_conversation(conversation_id):
    global current_conversation

    current_conversation = AIConversation.find(conversation_id, logger=logger)
    if current_conversation:
        current_conversation.init()
        return [item.__dict__() for item in current_conversation.messages()]
    return []


@eel.expose
def message_received(message_data: dict):
    print("Message received:", message_data)
    if not current_conversation:
        return None

    attachments: list[Attachment] = []
    for attachment in message_data.get("attachments", []):
        path = os.path.join(Env.base_path, "run/browser/tmp", attachment["filename"])
        shutil.move(path, current_conversation.directory.path)
        attachments.append(
            Attachment.create(
                None,
                attachment["mime_type"],
                os.path.join(
                    current_conversation.directory.name, attachment["filename"]
                ),
            )
        )

    message, answer = current_conversation.handle_message(
        message_data["content"], attachments
    )

    gTTS(answer.content, lang="en").save(
        os.path.join(current_conversation.directory.path, f"answer-{answer.id}.mp3")
    )

    if streaming_record:
        streaming_record.start()

    return {"message": message.__dict__(), "answer": answer.__dict__()}


@eel.expose
def upload_file(file_content):
    filename = f"tmp-{time.strftime('%Y%m%d-%H%M%S')}"
    path = os.path.join(Env.base_path, "run/browser/tmp", filename)
    header, encoded = file_content.split(",", 1)
    data = base64.b64decode(encoded)
    with open(path, "wb") as f:
        f.write(data)
    return filename


current_recording = None


@eel.expose
def start_recording():
    global current_recording

    if not current_recording and current_conversation:
        if streaming_record:
            audio_effect.play("start-stream-recording.wav")
        audio_effect.play("start-recording.wav")

        print("Starting recording...")

        current_recording = AudioRecorder(
            on_recording_finished,
            stop_on_silence=streaming_record is not None,
        )
        current_recording.start()


@eel.expose
def stop_recording():
    global current_recording

    if current_recording:
        current_recording.stop()
        current_recording = None


def on_recording_finished(filename):
    global current_recording

    eel.stopRecording(filename)
    current_recording = None
    audio_effect.play("end-recording.wav")


streaming_record = None


@eel.expose
def streaming_recording():
    global streaming_record

    if not current_conversation:
        return False

    if streaming_record:
        streaming_record.stop()
        streaming_record = None
    else:
        streaming_record = StreamingRecord(start_recording)
        streaming_record.start()

    return streaming_record is not None
