import cv2
import time
import simpletracker as st
import window_tracker as wt

def points_from_bbox(bbox):    
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    return p1, p2

# cap = cv2.VideoCapture('data/chaplin.mp4')
# cap = cv2.VideoCapture('http://192.168.1.3:4444/video')
cap = cv2.VideoCapture(0)

res, frame = cap.read()

init_bbox = (287, 23, 86, 320)
init_bbox = (280, 140, 150, 150)
wind_trck = wt.WindowTracker(frame, init_bbox)
simpl_trck = st.SimpleTracker(frame, init_bbox)
#kcf_trck = cv2.Tracker_create('KCF')
#kcf_trck.init(frame, init_bbox) 

# fps measurement
current_frame = 0
capture_frames = 5
start_time = time.time()



while res:
    # measure fps
    current_frame = (current_frame + 1) % capture_frames
    if current_frame == 0:
        end_time = time.time()
        fps = capture_frames // (end_time - start_time)
        print(fps)
        start_time = time.time()

    res, frame = cap.read()

    # simpl_bbox = simpl_trck.track(frame)
    wind_bbox = wind_trck.track(frame)
    # res, kcf_bbox = kcf_trck.update(frame)

    # simpl_p1, simpl_p2 = points_from_bbox(simpl_bbox)
    wind_p1, wind_p2 = points_from_bbox(wind_bbox)
    #kcf_p1, kcf_p2 = points_from_bbox(kcf_bbox)
    
    # cv2.rectangle(frame, simpl_p1, simpl_p2, (0,0,255))
    cv2.rectangle(frame, wind_p1, wind_p2, (0,255, 0))
    # cv2.rectangle(frame, kcf_p1, kcf_p2, (255, 0, 0))

    cv2.imshow("Tracker", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()