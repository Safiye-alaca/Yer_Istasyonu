import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from yer_istasyonu import Ui_Form
# from backend import TelemetryReader  # ← Telemetri geçici olarak kaldırıldı
from PyQt5 import QtWidgets
import cv2
from PyQt5.QtGui import QImage, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Telemetri verilerini başlat
        # self.telemetry = TelemetryReader()
        # self.telemetry.start()

        # Telemetri verilerini GUI'ye yazdırmak için zamanlayıcı kur
        self.timer_telemetry = QTimer()
        self.timer_telemetry.timeout.connect(self.update_labels)
        self.timer_telemetry.start(1000)

        # -------------------------------
        # Analog görüntü (USB kamera) için hazırlık
        # -------------------------------
        self.camera = cv2.VideoCapture(1)

        self.timer_camera = QTimer()
        self.timer_camera.timeout.connect(self.update_frame)
        self.timer_camera.start(30)

    def update_labels(self):
        print("Veri güncelleniyor...")
        # print(f"Altitude: {self.telemetry.altitude}")
        # print(f"Voltage: {self.telemetry.battery_voltage}")
        # print(f"Yaw: {self.telemetry.yaw}")

        # self.ui.label_2_irtifa.setText(f"{self.telemetry.altitude:.2f} m")
        # self.ui.label_3_batarya.setText(f"{self.telemetry.battery_voltage:.2f} V")
        # self.ui.label_11_donusAcisi.setText(f"{self.telemetry.yaw:.2f}°")
        # self.ui.label_6.setText(f"{self.telemetry.groundspeed:.2f} m/s")
        # self.ui.label_9.setText(f"{self.telemetry.pitch:.2f}°")
        # self.ui.label_10_wpyeMesafe.setText(f"{self.telemetry.satellites_visible} uydu")
        # self.ui.label_12_dikeyHiz.setText(f"{self.telemetry.climb:.2f} m/s")
        # self.ui.label_8_yerdenHiz.setText(f"{self.telemetry.groundspeed:.2f} m/s")

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.ui.label_5_analog.setPixmap(pixmap)

    def closeEvent(self, event):
        self.camera.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
