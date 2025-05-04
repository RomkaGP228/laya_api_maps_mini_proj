import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
import requests
from math import log2
from PyQt6.QtCore import Qt


class MAPAPI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        uic.loadUi('data/main.ui', self)  # Ensure 'data/main.ui' exists
        self.theme_button.clicked.connect(self.theme_method)
        self.finder_button.clicked.connect(self.finder)

    def initUI(self):
        self.cords = "37.588902,55.768677"
        self.scale = 17
        self.theme_color = 'light'
        self.image_maker(self.cords, self.scale, theme_color=self.theme_color)
        self.pixmap = QPixmap('map.png')
        self.image = QLabel(self)
        self.image.resize(600, 600)
        self.image.setPixmap(self.pixmap)
        # Ensure the main window has focus to capture key events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def image_maker(self, coords, scale, theme_color, pt=None):
        server_address = "https://static-maps.yandex.ru/v1?"
        self.params = {'ll': coords,
                       'z': scale,
                       'l': 'map',
                       'apikey': "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
                       'theme': theme_color,
                       'pt': pt}
        response = requests.get(server_address, self.params)

        if not response:
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def theme_method(self):
        if self.theme_button.text() == 'Темная тема':
            self.theme_color = 'dark'
            self.theme_button.setText('Светлая тема')
        else:
            self.theme_color = 'light'
            self.theme_button.setText('Темная тема')
        print('goaal')
        self.image_maker(self.cords, self.scale, self.theme_color)
        self.image.setPixmap(QPixmap('map.png'))

    def finder(self):
        geocoder_address = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "geocode": self.finder_line.text(),
            "format": "json"}
        response = requests.get(geocoder_address, geocoder_params)
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        self.cords = ','.join(list(map(str, toponym["Point"]["pos"].split(" "))))
        self.image_maker(self.cords, self.scale, self.theme_color, pt=self.cords)
        self.image.setPixmap(QPixmap('map.png'))

    def keyPressEvent(self, event):
        cords = self.cords.split(',')
        step = 10 / (log2(self.scale) * self.scale ** 2.5)  # Fixed typo in formula

        if event.key() == Qt.Key.Key_Up:
            cords[1] = str(float(cords[1]) + abs(step))  # Move latitude up
            if abs(float(cords[1])) >= 90:
                return
            self.cords = ','.join(cords)

        elif event.key() == Qt.Key.Key_Down:
            cords[1] = str(float(cords[1]) - abs(step))  # Move latitude down
            if abs(float(cords[1])) >= 90:
                return
            self.cords = ','.join(cords)

        elif event.key() == Qt.Key.Key_Right:
            cords[0] = str(float(cords[0]) + abs(step))  # Move longitude right
            if abs(float(cords[0])) >= 180:
                return
            self.cords = ','.join(cords)

        elif event.key() == Qt.Key.Key_Left:
            cords[0] = str(float(cords[0]) - abs(step))  # Move longitude left
            if abs(float(cords[0])) >= 180:
                return
            self.cords = ','.join(cords)

        elif event.key() == Qt.Key.Key_PageUp and self.scale < 21:
            self.scale += 1  # Zoom in

        elif event.key() == Qt.Key.Key_PageDown and self.scale > 0:
            self.scale -= 1  # Zoom out

        # Update the map after any key press
        self.image_maker(self.cords, self.scale, self.theme_color)
        self.image.setPixmap(QPixmap('map.png'))

    def closeEvent(self, event):
        if os.path.exists("map.png"):
            os.remove("map.png")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MAPAPI()
    ex.show()
    sys.exit(app.exec())
