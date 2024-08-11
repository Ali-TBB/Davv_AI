import base64
import eel
import time
import os
import shutil

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
    """
    Initializes the browser module, sets up the web directory path, and starts the browser window.

    Parameters:
        None

    Returns:
        None
    """

    eel.init(os.path.join(Env.base_path, "run/browser/web"))
    w, h = pyautogui.size()
    eel.start("index.html", app_mode=True, size=(w * 0.6, h), close_callback=on_close)


def on_close(page, sockets):
    """
    Perform necessary actions when the browser page is closed.

    Args:
        page: The browser page that is being closed.
        sockets: The sockets associated with the page.

    Returns:
        None
    """

    if streaming_record:
        streaming_record.stop()

    if current_recording:
        current_recording.stop()

    exit()


current_conversation: AIConversation = None


@eel.expose
def create_conversation(name):
    """
    Create a new conversation with the given name.

    Args:
        name (str): The name of the conversation.

    Returns:
        dict: A dictionary representation of the created conversation.
    """

    global current_conversation

    current_conversation = AIConversation.new(name, logger=logger)
    current_conversation.init()
    return current_conversation.__dict__()


@eel.expose
def delete_conversation(conversation_id):
    """
    Deletes a conversation based on the given conversation_id.

    Args:
        conversation_id (int): The ID of the conversation to be deleted.

    Returns:
        bool: True if the conversation is successfully deleted, False otherwise.
    """

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
    """
    Load conversations from AIConversation.all() in descending order.

    Returns:
        list: A list of dictionaries representing the conversations.
    """

    return [
        item.__dict__() for item in AIConversation.all(logger=logger, order_type="DESC")
    ]


@eel.expose
def load_conversation(conversation_id):
    """
    Load a conversation by its ID.

    Args:
        conversation_id (str): The ID of the conversation to load.

    Returns:
        list: A list of dictionaries representing the messages in the loaded conversation.
              Each dictionary contains the attributes of a message.

    """

    global current_conversation

    current_conversation = AIConversation.find(conversation_id, logger=logger)
    if current_conversation:
        current_conversation.init()
        return [item.__dict__() for item in current_conversation.messages()]
    return []


@eel.expose
def message_received(message_data: dict):
    """
    Process a received message and handle attachments.

    Args:
        message_data (dict): The data of the received message.

    Returns:
        dict: A dictionary containing the processed message and answer.

    """

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

    if streaming_record:
        streaming_record.start()

    return {"message": message.__dict__(), "answer": answer.__dict__()}


@eel.expose
def upload_file(base64_data, mime_type):
    """
    Uploads a file with the given base64 data and mime type.

    Args:
        base64_data (str): The base64 encoded data of the file.
        mime_type (str): The mime type of the file.

    Returns:
        str: The filename of the uploaded file.
    """

    filename = f"tmp-{time.strftime('%Y%m%d-%H%M%S')}.${mime_type.split('/')[1]}"
    path = os.path.join(Env.base_path, "run/browser/tmp", filename)
    data = base64.b64decode(base64_data)
    with open(path, "wb") as f:
        f.write(data)
    return filename


current_recording = None


@eel.expose
def start_recording():
    """
    Starts the recording process.

    This function initializes the recording process and starts recording audio.
    It checks if there is an ongoing conversation and if the recording is not already in progress.
    If streaming_record is enabled, it plays the "start-stream-recording.wav" audio effect.
    Otherwise, it plays the "start-recording.wav" audio effect.
    The recording process is handled by the AudioRecorder class.
    The recording will stop automatically if streaming_record is not None and silence is detected.

    Parameters:
        None

    Returns:
        None
    """

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
    """
    Stops the current recording.

    This function stops the current recording if there is one in progress.
    """

    global current_recording

    if current_recording:
        current_recording.stop()
        current_recording = None


def on_recording_finished(filename):
    """
    Callback function called when a recording is finished.

    Args:
        filename (str): The filename of the recorded audio.

    Returns:
        None
    """

    global current_recording

    eel.stopRecording(filename)
    current_recording = None
    audio_effect.play("end-recording.wav")


streaming_record = None


@eel.expose
def streaming_recording():
    """
    Start or stop the streaming recording.

    Returns:
        bool: True if the streaming recording is started, False otherwise.
    """

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
