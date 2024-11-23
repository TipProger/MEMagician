import pydub
import wave
import pyaudio
from PyQt5.QtCore import QThread, pyqtSignal

class AudioEditor(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.audio_format = pyaudio.paInt16
        self.channels = 2
        self.rate = 48000
        self.chunk = 1024
        self.segment = None
        self.filename = None
        self.temp_filename = 'temp.wav'

    def save_current_recording(self):
        with wave.open('recording.wav', 'wb') as wf:
            wf.setnchannels(self.col_channels)
            wf.setsampwidth(self.recorder.get_sample_size(self.audio_format))
            wf.setframerate(self.chastota)
            wf.writeframes(b''.join(self.frames))

    def sound_changing(self):
        file = 'recording.wav'
        volume = 1000
        self.segment = pydub.AudioSegment.from_file(file) # названия файлов и параметры для редактирования будут передаваться из виджетов Interface
        self.segment += volume
        self.segment.export(file, format='wav')

    def audio_trimming(self):
        finish_miliseconds = 2 * 1000
        start_miliseconds = 1 * 1000
        self.segment = self.segment[start_miliseconds:len(self.segment) - finish_miliseconds]
        segment.export(file, format='wav')

    def audio_overlay(self):
        file1 = 'recording.wav' # файл будет выбираться с компа
        file2 = 'recording.wav'
        segment = file1 + file2
        segment.export(file1, format='wav')