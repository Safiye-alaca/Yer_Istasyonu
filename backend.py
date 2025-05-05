"""
# backend.py
from pymavlink import mavutil
import threading

class TelemetryReader:
    def __init__(self):
        self.master = mavutil.mavlink_connection('COM5', baud=57600)
        self.altitude = 0.0
        self.battery_voltage = 0.0
        self.yaw = 0.0
        self.airspeed = 0.0
        self.groundspeed = 0.0
        self.roll = 0.0
        self.pitch = 0.0

    def start(self):
        thread = threading.Thread(target=self.read_loop, daemon=True)
        thread.start()

    def read_loop(self):
        self.master.wait_heartbeat()
        print("Bağlantı kuruldu!")

        while True:
            msg = self.master.recv_match(blocking=True)
            if not msg:
                continue

            msg_type = msg.get_type()

            if msg_type == "GLOBAL_POSITION_INT":
                self.altitude = msg.relative_alt / 1000.0
                self.yaw = msg.hdg / 100.0

            elif msg_type == "BATTERY_STATUS":
                voltages = msg.voltages
                if voltages[0] != 0xFFFF:
                    self.battery_voltage = voltages[0] / 1000.0

            elif msg_type == "VFR_HUD":
                self.groundspeed = msg.groundspeed
                self.airspeed = msg.airspeed

            elif msg_type == "ATTITUDE":
                self.roll = msg.roll * 57.2958
                self.pitch = msg.pitch * 57.2958
"""

from pymavlink import mavutil
import threading

class TelemetryReader:
    def __init__(self):
        # MAVLink bağlantısı başlatılıyor (COM portunu gerektiği gibi değiştir)
        self.master = mavutil.mavlink_connection('COM5', baud=57600)

        # Telemetri verileri
        self.altitude = 0.0
        self.battery_voltage = 0.0
        self.yaw = 0.0

    def start(self):
        # Arka planda çalışan thread başlatılıyor
        thread = threading.Thread(target=self.read_loop, daemon=True)
        thread.start()

    def read_loop(self):
        self.master.wait_heartbeat()
        print("✅ Bağlantı kuruldu!")

        # Telemetri veri akışı isteği gönderiliyor
        self.master.mav.request_data_stream_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_ALL,
            4,  # saniyede 4 mesaj
            1   # başlat (1), durdur (0)
        )

        while True:
            msg = self.master.recv_match(blocking=True)
            if not msg:
                continue

            # Gerekirse debug için yazdır
            print(f"📡 {msg.get_type()}: {msg}")

            if msg.get_type() == "GLOBAL_POSITION_INT":
                self.altitude = msg.relative_alt / 1000.0  # mm → m
                self.yaw = msg.hdg / 100.0  # centidegree → degree

            elif msg.get_type() == "BATTERY_STATUS":
                voltages = msg.voltages
                if voltages[0] != 0xFFFF:
                    self.battery_voltage = voltages[0] / 1000.0  # mV → V

