import os
import sys


from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from data.geocoder import reverse_geocode
import requests
class MAPAPI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.screen = [600, 600]
        self.cords = "37.530966,55.703258"
        self.scale = 0.002
        self.setGeometry(100, 100, *self.screen)
        self.setWindowTitle('MapApi')
        self.image_maker(self.cords, self.scale)
        self.pixmap = QPixmap('map.png')
        self.image = QLabel(self)
        self.image.resize(600, 600)
        self.image.setPixmap(self.pixmap)

    def image_maker(self, coords, scale):
        toponym = reverse_geocode(coords, scale)
        toponym_coodrinates = toponym["Point"]["pos"]
        # Долгота и широта:
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        print(toponym_lattitude, toponym_longitude)
        server_address = 'https://static-maps.yandex.ru/v1?'
        ll_spn = f"ll={','.join([toponym_longitude, toponym_lattitude])}&spn={str(scale),str(scale)}"
        map_request = f"{server_address}{ll_spn}&apikey={apikey}"
        response = requests.get(map_request)
        self.map_file = f"map.png"
        with open(self.map_file, "wb") as out_f:
            out_f.write(response.content)
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