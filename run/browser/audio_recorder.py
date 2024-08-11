import os
import time
import wave
import pyaudio
import numpy as np

from utils.env import Env


class AudioRecorder:
    """
    A class for recording audio.

    Attributes:
        MAX_RECORDING_TIME (int): Max recording time in seconds.
        MIN_RECORDING_TIME (int): Min recording time in seconds.
        MIN_VOICE_THRESHOLD (int): Threshold for detecting voice.
        HIGH_VOLUME_THRESHOLD (int): RMS threshold for high volume.

    Methods:
        __init__(self, on_recording_finished: callable, stop_on_silence=True): Initializes the AudioRecorder object.
        start(self): Starts the audio recording.
        stop(self): Stops the audio recording.
        __record(self): Records the audio.
        is_voice_active(self, data): Checks if voice is active in the audio data.
    """

    MAX_RECORDING_TIME = 10  # Max recording time in seconds
    MIN_RECORDING_TIME = 1  # Min recording time in seconds
    MIN_VOICE_THRESHOLD = 500  # Threshold for detecting voice
    HIGH_VOLUME_THRESHOLD = 1000  # RMS threshold for high volume

    def __init__(self, on_recording_finished: callable, stop_on_silence=True):
        """
        Initializes an instance of the AudioRecorder class.

        Args:
            on_recording_finished (callable): A callable object that will be invoked when the recording is finished.
            stop_on_silence (bool, optional): Determines whether the recording should stop automatically when silence is detected. Defaults to True.
        """

        self.stop_on_silence = stop_on_silence
        self.on_recording_finished = on_recording_finished
        self.recording = False
        self.thread = None

    def start(self):
        """
        Starts the audio recording process in a separate thread.

        If the recording is already in progress, this method does nothing.

        """

        if not self.recording:
            import threading

            self.recording = True
            self.thread = threading.Thread(target=self.__record)
            self.thread.start()

    def stop(self):
        """
        Stops the audio recording if it is currently in progress.
        """

        if self.recording:
            self.recording = False
            self.thread.join()

    def __record(self):
        """
        Records audio from the microphone and saves it to a WAV file.

        Returns:
            None

        Raises:
            None
        """

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        audio = pyaudio.PyAudio()

        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        frames = []

        start_time = last_voice_time = time.time()
        while self.recording and (time.time() - start_time) < self.MAX_RECORDING_TIME:
            data = stream.read(CHUNK)
            frames.append(data)

            if self.stop_on_silence:
                if self.is_voice_active(data):
                    last_voice_time = time.time()
                else:
                    elapsed_silence = (
                        time.time() - last_voice_time
                    )
                    if elapsed_silence >= 2:
                        print("Silence detected for 4 seconds. Stopping recording.")
                        break

        stream.stop_stream()
        stream.close()
        audio.terminate()

        output_file = None

        # if start_time - last_voice_time > self.MIN_RECORDING_TIME:
        output_file = f"rec-{time.strftime('%Y%m%d-%H%M%S')}.wav"
        with wave.open(
            os.path.join(Env.base_path, "run/browser/tmp", output_file), "wb"
        ) as wave_file:
            wave_file.setnchannels(CHANNELS)
            wave_file.setsampwidth(audio.get_sample_size(FORMAT))
            wave_file.setframerate(RATE)
            wave_file.writeframes(b"".join(frames))

        self.on_recording_finished(output_file)

    def is_voice_active(self, data):
        """
        Check if there is active voice in the given audio data.

        Args:
            data (bytes): The audio data.

        Returns:
            bool: True if there is active voice, False otherwise.
        """

        audio_data = np.frombuffer(data, dtype=np.int16)
        return np.any(np.abs(audio_data) > self.MIN_VOICE_THRESHOLD)
