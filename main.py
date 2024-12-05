import logging
import random
import string
import sys
import requests
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QLabel, QWidget, QLineEdit
from PySide6.QtGui import QMovie
from PySide6.QtCore import QBuffer, QByteArray, Qt, QIODevice

import RequestError

API_KEY = "AIzaSyASK7yVNJo89KkhzAhEQBZgGDdcQ_sC5Co"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def generate_random_query():
    length = random.randint(3, 15)
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def get_random_gif_url(q=""):
    url = "https://tenor.googleapis.com/v2/search"
    while True:
        if q == "":
            query = generate_random_query()
        else:
            query = q
        random_offset = random.randint(0, 1000)
        params = {
            "q": query,
            "key": API_KEY,
            "limit": 30,
            "pos": random_offset,
        }
        logging.info(f"Отправка запроса к API с параметрами: {params}")

        response = requests.get(url, params=params)

        if response.status_code == 200:
            logging.info("Запрос успешно выполнен, получен ответ 200")

            data = response.json()
            gif = random.choice(data["results"])
            gif_url = gif["media_formats"]["gif"]["url"]
            logging.info(f"Получен URL GIF: {gif_url}")
            return gif_url
        else:
            RequestError.ApiRequestError(response.status_code)


class GifViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор мемов")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.gif_label = QLabel("Нажмите кнопку для загрузки GIF")
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText("Введите тег для поиска (или оставьте пустым)")

        self.button = QPushButton("Показать случайную GIF")
        self.button.clicked.connect(self.show_random_gif)

        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(QApplication.quit)

        self.layout.addWidget(self.gif_label)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout)

    def show_random_gif(self):
        text = self.textbox.text().strip()
        if text == "":
            gif_url = get_random_gif_url()
        else:
            logging.info(f"Пользователь ввел запрос: '{text}'")

            gif_url = get_random_gif_url(text)
        if gif_url:
            response = requests.get(gif_url)
            gif_data = response.content

            gif_movie = QMovie()
            gif_buffer = QBuffer()
            gif_buffer.setData(QByteArray(gif_data))
            gif_buffer.open(QIODevice.OpenModeFlag.ReadOnly)
            gif_movie.setDevice(gif_buffer)

            self.gif_label.setMovie(gif_movie)
            gif_movie.start()
        else:
            logging.error("Ошибка запроса к API")
            self.gif_label.setText("Ошибка запроса к API")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = GifViewer()
    viewer.show()
    sys.exit(app.exec())
