import os
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
import requests
from math import log2
from PyQt6.QtCore import Qt


class MAPAPI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def image_maker(self, coords, scale):
        server_address = 'http://static-maps.yandex.ru/1.x/?'
        ll_spn = f'll={coords}&z={scale}'
        # Готовим запрос.

        map_request = f"{server_address}{ll_spn}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.screen = [600, 600]
        self.cords = "37.588902,55.768677"
        self.scale = 17
        self.setGeometry(100, 100, *self.screen)
        self.setWindowTitle('MapApi')
        self.image_maker(self.cords, self.scale)
        self.pixmap = QPixmap('map.png')
        self.image = QLabel(self)
        self.image.resize(600, 600)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp and self.scale < 21:
            self.scale += 1
        elif event.key() == Qt.Key.Key_PageDown and self.scale > 0:
            self.scale -= 1

        elif event.key() == Qt.Key.Key_Up:
            cords = self.cords.split(',')
            step = 10 / (log2(self.scale) * self.scale ** 2.5)
            cords[1] = str(float(cords[1]) + abs(step))
            if abs(float(cords[1])) >= 90:
                return
            self.cords = ','.join(cords)

        elif event.key() == Qt.Key.Key_Down:
            cords = self.cords.split(',')
            step = 10 / (log2(self.scale) * self.scale ** 2.5)
            cords[1] = str(float(cords[1]) - abs(step))
            if abs(float(cords[1])) >= 90:
                return
            self.cords = ','.join(cords)

        elif event.key() == Qt.Key.Key_Right:
            cords = self.cords.split(',')
            step = 10 / (log2(self.scale) * self.scale ** 2.5)
            cords[0] = str(float(cords[0]) + abs(step))
            if abs(float(cords[0])) >= 90:
                return
            self.cords = ','.join(cords)

        elif event.key() == Qt.Key.Key_Left:
            cords = self.cords.split(',')
            step = 10 / (log2(self.scale) * self.scale ** 2.5)
            cords[0] = str(float(cords[0]) - abs(step))
            if abs(float(cords[0])) >= 90:
                return
            self.cords = ','.join(cords)

        self.image_maker(self.cords, self.scale)
        self.image.setPixmap(QPixmap('map.png'))

    def closeEvent(self, event):
        os.remove("map.png")


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MAPAPI()
    ex.show()
    sys.exit(app.exec())
