import cv2

# Sistemde hangi kamera portlarının aktif olduğunu otomatik denemek.
# Kamerayı bağladığında hangi portta olduğunu bilmek içindir.
for i in range(5):
    # Bu satır, sıradaki i portundan bir kamera bağlantısı açmaya çalışır.
    cap = cv2.VideoCapture(i) 
    # kameradan bir kare okumaya çalışır.
    if cap.read()[0]:
        print(f"✅ Kamera {i} aktif.")
        cap.release()
    else:
        print(f"❌ Kamera {i} çalışmıyor.")
