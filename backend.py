from pymavlink import mavutil
import threading

class TelemetryReader(threading.Thread):
    def __init__(self):
        super(TelemetryReader, self).__init__()
        self.daemon = True

        # Başlangıç değerleri
        self.altitude = 0.0
        self.battery_voltage = 0.0
        self.yaw = 0.0
        self.groundspeed = 0.0
        self.airspeed = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.satellites_visible = 0     
        self.climb = 0.0                


        # MAVLink bağlantısını kur
        self.master = mavutil.mavlink_connection('COM5', baud=57600)
        self.master.wait_heartbeat()
        print("💡 MAVLink bağlantısı kuruldu!")

        # Veri akışını başlat (saniyede 4 veri mesajı)
        self.master.mav.request_data_stream_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_ALL,
            4,  # saniyedeki mesaj sayısı
            1   # başlat
        )

    def run(self):
        while True:
            msg = self.master.recv_match(blocking=True)
            if not msg:
                continue

            msg_type = msg.get_type()

            if msg_type == "GLOBAL_POSITION_INT":
                self.altitude = msg.relative_alt / 1000.0  # mm -> m
                self.yaw = msg.hdg / 100.0 if msg.hdg != 65535 else 0.0
                self.groundspeed = msg.vx / 100.0  # cm/s -> m/s

            elif msg_type == "VFR_HUD":
                self.airspeed = msg.airspeed

            elif msg_type == "SYS_STATUS":
                self.battery_voltage = msg.voltage_battery / 1000.0  # mV -> V

            elif msg_type == "ATTITUDE":
                self.roll = msg.roll * 57.3     # rad -> derece
                self.pitch = msg.pitch * 57.3
                self.yaw = msg.yaw * 57.3       # alternatif yaw

            if msg_type == "GLOBAL_POSITION_INT":
                self.altitude = msg.relative_alt / 1000.0  # mm -> m
                self.yaw = msg.hdg / 100.0 if msg.hdg != 65535 else 0.0
                self.groundspeed = (msg.vx**2 + msg.vy**2) ** 0.5 / 100.0  # vx ve vy'den net yer hızı

            elif msg_type == "VFR_HUD":
                self.airspeed = msg.airspeed
                self.climb = msg.climb  # dikey hız

            elif msg_type == "GPS_RAW_INT":
                self.satellites_visible = msg.satellites_visible  # uydu sayısı

            elif msg_type == "ATTITUDE":
                self.roll = msg.roll * 57.3
                self.pitch = msg.pitch * 57.3
                # self.yaw = msg.yaw * 57.3  # Alternatif yaw kaynağı, gerekirse yorumdan çıkar
