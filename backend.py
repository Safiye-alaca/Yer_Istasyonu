from pymavlink import mavutil

# 1. Seri bağlantıyı başlat
connection = mavutil.mavlink_connection('COM5', baud=57600)  # COM3 yerine senin COM portun

# 2. İlk "heartbeat" mesajını bekle (bağlantı kurulduğuna emin olmak için)
print("Bağlantı bekleniyor...")
connection.wait_heartbeat()
print(f"Bağlantı kuruldu: Sistem ID {connection.target_system}, Component ID {connection.target_component}")

# 3. Sürekli veri oku
while True:
    msg = connection.recv_match(blocking=True)
    if not msg:
        continue
    print(msg)
