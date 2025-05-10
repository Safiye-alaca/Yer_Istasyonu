import sys
import cv2
import numpy as np
import requests
from io import BytesIO
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from yer_istasyonu import Ui_Form


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Analog (USB) kamera başlat
        self.camera = cv2.VideoCapture(1)
        self.timer_camera = QTimer()
        self.timer_camera.timeout.connect(self.update_frame)
        self.timer_camera.start(30)  # 30ms'de bir analog görüntü

        # Dijital yayın URL (Cloudflare üzerinden gelen)
        self.stream_url = "https://offensive-dip-vat-voltage.trycloudflare.com/video_feed"
        self.stream_response = None
        self.bytes_buffer = b''
        self.session = requests.Session()  # Oturum ile yeniden bağlanmayı kolaylaştırır
        self.timer_digital = QTimer()
        self.timer_digital.timeout.connect(self.update_digital_frame)
        self.timer_digital.start(100)  # 100ms'de bir dijital görüntü

        # (İsteğe bağlı) Telemetri simülasyonu
        self.timer_telemetry = QTimer()
        self.timer_telemetry.timeout.connect(self.update_labels)
        self.timer_telemetry.start(1000)

    def update_labels(self):
        print("Veri güncelleniyor...")  # Gerekirse telemetry entegrasyonu yapılabilir

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            qt_image = QImage(
                frame.data, frame.shape[1], frame.shape[0],
                frame.shape[1] * 3, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qt_image)
            self.ui.label_5_analog.setPixmap(pixmap)

    def update_digital_frame(self):
        if not hasattr(self, 'digital_cap'):
            self.digital_cap = cv2.VideoCapture(self.stream_url)

        if not self.digital_cap.isOpened():
            print("Dijital stream bağlantısı başarısız.")
            return

        ret, frame = self.digital_cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            qt_image = QImage(
                frame.data, frame.shape[1], frame.shape[0],
                frame.shape[1] * 3, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qt_image)
            self.ui.label_4_dijital.setPixmap(pixmap)
        else:
            print("Dijital görüntü alınamadı.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
