import cv2
import time
import simpletracker as t
import window_tracker as wt

cap = cv2.VideoCapture('data/chaplin.mp4')
# cap = cv2.VideoCapture('http://192.168.1.3:4444/video')

res, frame = cap.read()

bbox = (287, 23, 86, 320)
# trck = wt.WindowTrakcker(frame, bbox)
trck = t.OliObjectTracker(frame, bbox)

current_frame = 0
start_time = time.time()
capture_frames = 5
while res:
    current_frame = (current_frame + 1) % capture_frames
    if current_frame == 0:
        end_time = time.time()
        fps = capture_frames // (end_time - start_time)
        print(fps)
        start_time = time.time()


    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (0,0,255))

    cv2.imshow("Tracker", frame)

    res, frame = cap.read()
    bbox = trck.track(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()