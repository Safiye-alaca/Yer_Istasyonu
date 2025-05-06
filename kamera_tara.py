import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.read()[0]:
        print(f"✅ Kamera {i} aktif.")
        cap.release()
    else:
        print(f"❌ Kamera {i} çalışmıyor.")
