# yer_istasyonu_main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from yer_istasyonu import Ui_Form
from backend import TelemetryReader

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.telemetry = TelemetryReader()
        self.telemetry.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(1000)  # 1 saniyede bir verileri güncelle

    def update_labels(self):
        self.ui.label_2_irtifa.setText(f"{self.telemetry.altitude:.2f} m")
        self.ui.label_3_batarya.setText(f"{self.telemetry.battery_voltage:.2f} V")
        self.ui.label_11_donusAcisi.setText(f"{self.telemetry.yaw:.2f}°")
        self.ui.label_6.setText(f"{self.telemetry.groundspeed:.2f} m/s")  # yer hızı
        self.ui.label.setText(f"{self.telemetry.airspeed:.2f} m/s")       # hava hızı
        self.ui.label_8.setText(f"{self.telemetry.roll:.2f}°")            # roll
        self.ui.label_9.setText(f"{self.telemetry.pitch:.2f}°")           # pitch

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
