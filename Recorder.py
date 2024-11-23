import wave
import pyaudio
from PyQt5.QtCore import QThread, pyqtSignal

class AudioRecorder(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.audio_format = pyaudio.paInt16
        self.channels = 2
        self.rate = 48000
        self.chunk = 1024
        self.frames = []
        self.recorder = pyaudio.PyAudio()
        self.is_recording = False
        self.is_paused = False

    def run(self):
        self.start_recording()

    def start_recording(self):
        self.is_recording = True
        stream = self.recorder.open(format=self.audio_format,
                                     channels=self.channels,
                                     rate=self.rate,
                                     frames_per_buffer=self.chunk,
                                     input=True)
        self.update_signal.emit("Запись начата...")

        while self.is_recording:
            if not self.is_paused:
                data = stream.read(self.chunk)
                self.frames.append(data)

        stream.stop_stream()
        stream.close()
        self.recorder.terminate()
        self.update_signal.emit("Запись завершена.")

    def stop_recording(self):
        self.is_recording = False

    def pause_recording(self):
        self.is_paused = True
        self.update_signal.emit("Запись приостановлена.")

    def resume_recording(self):
        self.is_paused = False
        self.update_signal.emit("Запись возобновлена.")

    def save_recording(self, file_path):
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.recorder.get_sample_size(self.audio_format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        self.update_signal.emit(f"Запись сохранена: {file_path}")

