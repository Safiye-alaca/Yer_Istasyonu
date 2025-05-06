import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer

class CameraTest(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analog Kamera Testi")
        self.setGeometry(100, 100, 640, 480)

        self.label = QLabel(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.camera = cv2.VideoCapture(1)  # 0: ön kamera, 1: arka kamera (gerekirse değiştir)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.camera.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraTest()
    window.show()
    sys.exit(app.exec_())
