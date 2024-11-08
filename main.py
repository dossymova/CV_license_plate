from ultralytics import YOLO
import cv2

from sort.sort import *
from util import get_car, read_license_plate

from db import Database

mot_tracker = Sort()

coco_model = YOLO("yolov8n.pt").cuda()
license_plate_model = YOLO("license_plate_detector.pt").cuda()

# cap = cv2.VideoCapture("./videos/test.mp4")
cap = cv2.VideoCapture("./images/ewq.png")

vehicles = [2, 5, 7]

db = Database('database.db')

window_width, window_height = 800, 600
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video', window_width, window_height)

frame_num = 0

ret = True
while ret:
    ret, frame = cap.read()
    if ret:
        if frame_num%10 == 0:
            detections = coco_model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection

                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])

            track_ids = mot_tracker.update(np.asarray(detections_))

            license_plates = license_plate_model(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate
                
                xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

                if car_id != -1:
                    license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_threshold  = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                    license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_threshold)
                    print(license_plate_text)

                    # cv2.imshow('license_plate_crop', license_plate_crop)
                    # cv2.imshow('license_plate_crop_threshold', license_plate_crop_threshold)
            
            frame_num = 0

        cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Video', window_width, window_height)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) == ord('q'):
            break
            
        frame_num += 1
    else:
        break

cap.release()
cv2.destroyAllWindows()