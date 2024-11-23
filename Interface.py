import PyQt5
from Editor import AudioEditor
from Recorder import AudioRecorder
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QStackedWidget, QFileDialog, QSlider, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQtWidgets.RedactTab import RedactTabUi
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
        #self.redact_tab()
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
        redact_tab_widget = QWidget()
        redact_tab_ui = RedactTabUi()
        redact_tab_ui.setupUi(redact_tab_widget)

        #Кнопка для возвращения в меню
        exit_button = QPushButton('Вернуться в меню')
        exit_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        redact_tab_widget.mainLayout.addWidget(exit_button)

        # Добавление виджета для выбора аудио-файла
        self.file_label = QLabel("Выберите аудио-файл:")
        self.file_button = QPushButton("Выбрать файл")
        self.file_button.clicked.connect(self.select_audio_file)
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_button)
        file_group = QWidget()
        file_group.setFixedHeight(100)
        file_group.setFixedWidth(400)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        self.audio_file = None
        self.temp_audio_file = None

        # Добавление ползунка для регулировки громкости
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(-100)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(0)
        self.volume_slider.valueChanged.connect(lambda: self.volume_value_label.setText(f'{self.volume_slider.value()} дБ'))

        self.volume_label = QLabel("Громкость (дБ)")
        self.volume_value_label = QLabel("0 дБ")  # Динамический лейбл для отображения текущего значения
        self.volume_min_label = QLabel("-100 дБ")
        self.volume_max_label = QLabel("+100 дБ")
        self.volume_layout = QHBoxLayout()
        self.volume_layout.addWidget(self.volume_min_label)
        self.volume_layout.addWidget(self.volume_slider)
        self.volume_layout.addWidget(self.volume_max_label)
        self.volume_widget = QWidget()
        self.volume_widget.setLayout(self.volume_layout)

        volume_group_layout = QVBoxLayout()
        volume_group_layout.addWidget(self.volume_label)
        volume_group_layout.addWidget(self.volume_value_label)
        volume_group_layout.addWidget(self.volume_widget)
        volume_group_widget = QWidget()
        volume_group_widget.setLayout(volume_group_layout)
        volume_group_widget.setFixedHeight(100)
        volume_group_widget.setFixedWidth(400)  # Установите желаемую ширину

        layout.addWidget(volume_group_widget)

        # Добавление двойного ползунка для обрезания аудио дорожки
        # Надо добавить

        #Закрепление виджетов и вкладки
        tab_widget.setLayout(layout)
        self.stacked_widget.addWidget(tab_widget)

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