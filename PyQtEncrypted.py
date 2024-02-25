from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QSplitter
from PyQt5.QtGui import QPixmap, QIcon

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Шифрование и дешифрование")
        self.setGeometry(400, 400, 600, 300)
        self.resize(850, 450)
        self.setWindowIcon(QIcon("icon.png"))
        self.set_background_image("bg.png")

        splitter = QSplitter()
        splitter.setOrientation(Qt.Horizontal)

        encrypt_groupbox = self.create_groupbox("Шифрование", self.encrypt_text)
        decrypt_groupbox = self.create_groupbox("Дешифрование", self.decrypt_text)

        splitter.addWidget(encrypt_groupbox)
        splitter.addWidget(decrypt_groupbox)

        self.setCentralWidget(splitter)

    def set_background_image(self, image_path):
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap(image_path))
        self.background_label.setScaledContents(True)
        self.update_background_geometry()

    def update_background_geometry(self):
        self.background_label.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        self.update_background_geometry()
        event.accept()

    def create_groupbox(self, title, button_callback):
        groupbox = QWidget()
        layout = QVBoxLayout(groupbox)

        label_input = QLabel("Введите текст:")
        layout.addWidget(label_input)

        input_field = QTextEdit()
        layout.addWidget(input_field)

        label_key = QLabel("Введите ключ:")
        layout.addWidget(label_key)

        key_field = QLineEdit()
        layout.addWidget(key_field)

        button = QPushButton(title)
        button.clicked.connect(lambda: button_callback(input_field.toPlainText(), key_field.text(), output_field))
        layout.addWidget(button)

        output_field = QTextEdit()
        output_field.setReadOnly(True)
        layout.addWidget(output_field)

        self.adjust_height(output_field)

        return groupbox

    def adjust_height(self, field):
        content_height = field.document().size().height()
        field.setMinimumHeight(int(content_height) + 10)
        field.setMaximumHeight(int(content_height) + 10)

    def encrypt_text(self, text, key, output_field):
        if not key.isdigit():
            QMessageBox.warning(self, "Ошибка", "Некорректный ключ")
            return
        encrypted_text = ""
        for char in text:
            encrypted_char = ord(char) ^ int(key)
            encrypted_text += chr(encrypted_char)
        output_field.setText(encrypted_text)
        self.adjust_height(output_field)

    def decrypt_text(self, text, key, output_field):
        if not key.isdigit():
            QMessageBox.warning(self, "Ошибка", "Некорректный ключ")
            return
        decrypted_text = ""
        for char in text:
            decrypted_char = ord(char) ^ int(key)
            decrypted_text += chr(decrypted_char)
        output_field.setText(decrypted_text)
        self.adjust_height(output_field)

        QApplication.clipboard().setText(decrypted_text)


app = QApplication([])
main_window = MyMainWindow()
main_window.show()
app.exec_()
