import PyQt5
from Editor import AudioEditor
from Recorder import AudioRecorder
from Player import AudioPlayer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QStackedWidget, QFileDialog, QSlider, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQtWidgets.RedactTab import Ui_RedactTabWidget
from PyQtWidgets.DoubleSlider import RangeSlider
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MEMagician')
        self.setWindowState(PyQt5.QtCore.Qt.WindowMaximized)
        self.editor = AudioEditor()
        self.stacked_widget = QStackedWidget(self)
        self.init_menu()
        self.record_tab()
        self.redact_tab()
        self.setCentralWidget(self.stacked_widget)

    def init_menu(self):
        menu_widget = QWidget()
        layout = QVBoxLayout()
        record_button = QPushButton('Запись')
        record_button.clicked.connect(lambda:self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(record_button)
        record_button = QPushButton('Редактор')
        record_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(record_button)
        menu_widget.setLayout(layout)
        self.stacked_widget.addWidget(menu_widget)

    def record_tab(self):
        rec_tab_widget = QWidget()
        layout = QVBoxLayout()
        exit_button = QPushButton('Вернуться в меню')
        exit_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(exit_button)

        self.record_button = QPushButton('Начать запись')
        self.record_button.clicked.connect(self.toggle_recording)
        layout.addWidget(self.record_button)

        self.pause_button = QPushButton('Пауза')
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setEnabled(False)  # Отключаем кнопку паузы в начале
        layout.addWidget(self.pause_button)

        rec_tab_widget.setLayout(layout)
        self.stacked_widget.addWidget(rec_tab_widget)

        self.recorder_thread = None

    def toggle_recording(self):
        if self.recorder_thread is None or not self.recorder_thread.is_recording:
            self.recorder_thread = AudioRecorder()
            self.recorder_thread.update_signal.connect(self.update_label)
            self.recorder_thread.start()  # Запуск потока записи
            self.record_button.setText("Остановить запись")
            self.pause_button.setEnabled(True)  # Включаем кнопку паузы
        else:
            self.recorder_thread.stop_recording()  # Остановка записи
            self.recorder_thread.wait()  # Ждем завершения потока

            # Сохранение файла
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить запись", "", "WAV Files (*.wav)")
            if file_path:
                self.recorder_thread.save_recording(file_path)

            self.recorder_thread = None
            self.record_button.setText("Начать запись")
            self.pause_button.setEnabled(False)  # Отключаем кнопку паузы

    def toggle_pause(self):
        if self.recorder_thread.is_paused:
            self.recorder_thread.resume_recording()
            self.pause_button.setText("Пауза")
        else:
            self.recorder_thread.pause_recording()
            self.pause_button.setText("Возобновить")

    def update_label(self, message):
        print(message)  # Выводим сообщение в консоль (можно заменить на обновление метки)

    def redact_tab(self):
        #Создаем основной виджет вкладки и экземпляр UI
        redact_tab_widget = QWidget()
        redact_tab_widget_ui = Ui_RedactTabWidget()
        # Установка UI на виджет
        redact_tab_widget_ui.setupUi(redact_tab_widget)

        #Дополняем дизайн вкладки и устанавливаем функционал
        #Кнопка для возвращения в меню
        exit_button = QPushButton('Вернуться в меню')
        exit_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        redact_tab_widget_ui.mainLayout.addWidget(exit_button)

        # Функция виджета для выбора аудио-файла
        redact_tab_widget_ui.SelecFileButton.clicked.connect(self.select_audio_file)

        # Добавление ползунка для регулировки громкости
        redact_tab_widget_ui.horizontalSlider.valueChanged.connect(lambda: redact_tab_widget_ui.SliderVolumeChange.setText(f'{redact_tab_widget_ui.horizontalSlider.value()} дБ'))

        # Добавление двойного ползунка для обрезания аудио дорожки
        range_slider = RangeSlider()
        range_slider.setRange(0, 0)

        #Закрепление виджетов и вкладки
        self.stacked_widget.addWidget(redact_tab_widget)

    def select_audio_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Audio files (*.wav *.mp3 *.ogg)")
        if file_dialog.exec_():
            self.audio_file = file_dialog.selectedFiles()[0]
            self.file_label.setText(f"Выбран файл: {os.path.basename(self.audio_file)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# как делать переключение между вкладками
