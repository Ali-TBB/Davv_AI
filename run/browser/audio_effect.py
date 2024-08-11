import os
import wave

import pyaudio

from utils.env import Env


chunk = 1024


def play(filename):
    """
    Play the audio file specified by the filename.

    Args:
        filename (str): The path to the audio file.

    Returns:
        None
    """

    file = wave.open(
        os.path.join(Env.base_path, "run/browser/web/src/media", filename), "rb"
    )
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=audio.get_format_from_width(file.getsampwidth()),
        channels=file.getnchannels(),
        rate=file.getframerate(),
        output=True,
    )
    data = file.readframes(chunk)
    while data:
        stream.write(data)
        data = file.readframes(chunk)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    file.close()
