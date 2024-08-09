import os
import time
import wave
import pyaudio
import numpy as np

from utils.env import Env


class AudioRecorder:

    # TODO; set to 20
    MAX_RECORDING_TIME = 10  # Max recording time in seconds
    MIN_RECORDING_TIME = 2  # Min recording time in seconds
    MIN_VOICE_THRESHOLD = 500  # Threshold for detecting voice
    HIGH_VOLUME_THRESHOLD = 1000  # RMS threshold for high volume

    def __init__(self, on_recording_finished: callable, stop_on_silence=True):
        self.stop_on_silence = stop_on_silence
        self.on_recording_finished = on_recording_finished
        self.recording = False
        self.thread = None

    def start(self):
        if not self.recording:
            import threading

            self.recording = True
            self.thread = threading.Thread(target=self.__record)
            self.thread.start()

    def stop(self):
        if self.recording:
            self.recording = False
            self.thread.join()

    def __record(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        audio = pyaudio.PyAudio()

        # Start Recording
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
                    )  # Calculate elapsed silence time
                    if elapsed_silence >= 2:
                        print("Silence detected for 4 seconds. Stopping recording.")
                        break

        # Stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        output_file = None

        if start_time - last_voice_time > self.MIN_RECORDING_TIME:
            output_file = f"rec-{time.strftime('%Y%m%d-%H%M%S')}.wav"
            with wave.open(
                os.path.join(Env.base_path, "run/browser/tmp", output_file), "wb"
            ) as wave_file:
                wave_file.setnchannels(CHANNELS)
                wave_file.setsampwidth(audio.get_sample_size(FORMAT))
                wave_file.setframerate(RATE)
                wave_file.writeframes(b"".join(frames))

        self.on_recording_finished(output_file)

    def is_voice_active(
        self,
        data,
    ):
        audio_data = np.frombuffer(data, dtype=np.int16)
        return np.any(np.abs(audio_data) > self.MIN_VOICE_THRESHOLD)
