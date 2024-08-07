import time
import wave
import pyaudio
import numpy as np

class AudioRecorder:

    MAX_RECORDING_TIME = 30

    def __init__(self, on_recording_finished: callable, stop_on_silence=True):
        self.stop_on_silence = stop_on_silence
        self.output_file = f"rec-{time.strftime('%Y%m%d-%H%M%S')}.wav"
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

        start_time = time.time()
        while self.recording and (time.time() - start_time) < self.MAX_RECORDING_TIME:
            data = stream.read(CHUNK)

            if self.stop_on_silence:
                if self.is_voice_active(data):
                    silence_count = 0
                else:
                    silence_count += 1

            frames.append(data)

        # Stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(self.output_file, "wb") as wave_file:
            wave_file.setnchannels(CHANNELS)
            wave_file.setsampwidth(audio.get_sample_size(FORMAT))
            wave_file.setframerate(RATE)
            wave_file.writeframes(b"".join(frames))

        self.on_recording_finished(self.output_file)

    def is_voice_active(self, data, threshold=500):
        audio_data = np.frombuffer(data, dtype=np.int16)
        return np.any(np.abs(audio_data) > threshold)