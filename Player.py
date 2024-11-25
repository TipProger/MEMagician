import wave
import pyaudio
from PyQt5.QtCore import QThread, pyqtSignal

class AudioPlayer(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.audio_format = pyaudio.paInt16
        self.channels = 2
        self.rate = 48000
        self.chunk = 1024
        self.frames = []
        self.player = pyaudio.PyAudio()
        self.is_playing = False
        self.is_paused = False

    def run(self):
        self.start_playing()

    def start_playing(self):
        self.is_playing = True
        stream = self.player.open(format=self.audio_format,
                                     channels=self.channels,
                                     rate=self.rate,
                                     frames_per_buffer=self.chunk,
                                     input=True)
        self.update_signal.emit("Запись начата...")

        while self.is_playing:
            if not self.is_paused:
                data = stream.read(self.chunk)
                self.frames.append(data)

        stream.stop_stream()
        stream.close()
        self.player.terminate()
        self.update_signal.emit("Запись завершена.")

    def stop_playing(self):
        self.is_playing = False

    def pause_playing(self):
        self.is_paused = True
        self.update_signal.emit("Запись приостановлена.")

    def resume_playing(self):
        self.is_paused = False
        self.update_signal.emit("Запись возобновлена.")


