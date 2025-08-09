import numpy as np
import cv2 as cv
import time
from ultralytics import YOLO
import supervision as sv

TARGET_VIDEO_PATH = './data/video1_result.mp4'
SOURCE_VIDEO_PATH = './data/video1.mp4'

#-------- LOAD MODEL--------------------------------------------
model = YOLO('./models/yolo11n.pt')
tracker = sv.ByteTrack()

frames_generator = sv.get_video_frames_generator(SOURCE_VIDEO_PATH)

# -------VIRTUAL LINE------------------------------------------
START = sv.Point(250, 800)
END = sv.Point(1500, 800)
line_zone = sv.LineZone(start=START, end=END)

cv.namedWindow("frame", cv.WINDOW_NORMAL)  # Create a resizable window
cv.resizeWindow("frame", 800, 600)         # Resize window to 800x600 pixels

# ----- LOOP FRAMES ---------------------------------------------
for frame in frames_generator:

    # detection------------------------------------------------
    results = model(frame, classes=[2,5,7])[0]


    # tracking--------------------------------------------------
    detections = sv.Detections.from_ultralytics(results)
    detections = tracker.update_with_detections(detections)
    crossed_in, crossed_out = line_zone.trigger(detections)


    # plot boxes and id -----------------------------------------
    for i in range(len(detections)):
        x,y,x2,y2 = detections[i].xyxy[0]
        id = detections[i].tracker_id[0]
        cv.rectangle(frame, [int(x), int(y)],  [int(x2), int(y2)], (0, 255, 0), 2)
        cv.putText(frame, str(id), (int(x), int(y)), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),4)


    # plot line and counting per frame ---------------------------
    cv.line(frame, (250, 800), (1500, 800), (255, 0, 0), 2)
    cv.putText(frame, "in" + str(line_zone.in_count), (int(850), int(850)), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),4)
    cv.putText(frame, "out" + str(line_zone.out_count), (int(850), int(750)), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),4)


    cv.imshow('frame', frame)    
    if cv.waitKey(1) == ord('q'):
        break
    
cv.destroyAllWindows()