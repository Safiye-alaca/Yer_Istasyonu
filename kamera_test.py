import cv2

for index in range(5):
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        print(f"Kamera bulundu: {index}")
        cap.release()
