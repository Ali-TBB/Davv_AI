import os
import threading
import time
import wave
import numpy as np
import pyaudio
import speech_recognition as sr

from utils.env import Env

# Parameters
CHUNK = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Number of audio channels
RATE = 44100  # Sample rate
THRESHOLD = 500  # Threshold for detecting speech
SILENCE_LIMIT = 2  # Silence limit in seconds
PRE_SPEECH_DURATION = 1  # Duration in seconds for pre-speech buffer
PRE_SPEECH_FRAMES = int(
    RATE * PRE_SPEECH_DURATION / CHUNK
)  # Number of frames to capture before speech starts


class StreamingRecord:
    """
    Class for streaming audio recording and speech detection.

    Args:
        on_detect (callable): A callback function to be called when speech is detected.

    Attributes:
        audio: The PyAudio object for audio input.
        stream: The audio stream for recording.
        thread: The thread for running the speech detection process.
        detecting (bool): Flag indicating if speech detection is currently active.

    Methods:
        start(): Start the audio recording and speech detection process.
        stop(): Stop the audio recording and speech detection process.

    Private Methods:
        __detect(): Method for detecting speech in the audio stream.
        __on_stop(): Method to be called when the speech detection process is stopped.
        __is_silent(data): Check if the audio data is below the silent threshold.
        __convert_to_text(frames): Convert the audio frames to text using Google Speech Recognition.

    """

    def __init__(self, on_detect: callable):
        """
        Initializes the StreamingRecord object.

        Args:
            on_detect (callable): A callable object that will be called when detection occurs.
        """

        self.on_detect = on_detect
        self.audio = None
        self.stream = None
        self.thread = None
        self.detecting = False

    def start(self):
        """
        Start the audio recording and speech detection process.
        """

        if self.detecting:
            return
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        self.detecting = True
        self.thread = threading.Thread(target=self.__detect)
        self.thread.start()

    def __detect(self):
        """
        Method for detecting speech in the audio stream.
        """

        print("Listening for speech...")

        frames = []
        speech_frames = []
        in_speech = False
        last_spoke = time.time()

        while self.detecting:
            frame = self.stream.read(CHUNK)
            frames.append(frame)

            if not self.__is_silent(frame):
                if not in_speech:
                    print("Start of speech")

                    in_speech = True
                    # speech_frames = list(frames)  # Start with pre-speech frames
                    speech_frames = frames[-min(PRE_SPEECH_FRAMES, len(frames)) :]
                else:
                    speech_frames.append(frame)

                last_spoke = time.time()
            else:
                if in_speech:
                    speech_frames.append(frame)
                    if time.time() - last_spoke > SILENCE_LIMIT:
                        print("End of speech")

                        if self.__convert_to_text(speech_frames):
                            self.detecting = False

                        in_speech = False
                        speech_frames = []

        self.__on_stop()

    def __on_stop(self):
        """
        Method to be called when the speech detection process is stopped.
        """

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def stop(self):
        """
        Stop the audio recording and speech detection process.
        """

        if not self.detecting:
            return
        self.detecting = False
        self.thread.join()

    def __is_silent(self, data):
        """
        Check if the audio data is below the silent threshold.

        Args:
            data: The audio data to be checked.

        Returns:
            bool: True if the audio data is below the silent threshold, False otherwise.
        """

        return np.max(np.frombuffer(data, np.int16)) < THRESHOLD

    def __convert_to_text(self, frames):
        """
        Convert the audio frames to text using Google Speech Recognition.

        Args:
            frames: The audio frames to be converted.

        Returns:
            bool: True if speech is detected and the callback function is called, False otherwise.
        """

        path = os.path.join(
            Env.base_path,
            "run/browser/tmp",
            f"tmp-{time.strftime('%Y%m%d-%H%M%S')}.wav",
        )
        wf = wave.open(path, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        wf.close()

        recognizer = sr.Recognizer()
        with sr.AudioFile(path) as source:
            audio = recognizer.record(source)

        detected = False
        try:
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            if "hi google" in text.lower() or "hey google" in text.lower():
                self.on_detect()
                detected = True
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}"
            )

        os.remove(path)

        return detected


if __name__ == "__main__":
    recorder = StreamingRecord(lambda: print("Detected the word!"))
    recorder.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        recorder.stop()
