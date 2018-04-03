import cv2
import sys
# import simpletracker as t

frame = None
pressed = False
released = False
initialized = False
startX, startY = 0, 0
currentX, currentY = 0, 0

#
def draw_rectange(event,x,y,flags,param):
    global pressed
    global startX
    global startY
    global currentX
    global currentY
    global released

    currentX, currentY = x, y

    before = pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        pressed = True
    elif event == cv2.EVENT_LBUTTONUP:
        pressed = False

    if before == True and pressed == False:
        released = True
        #cv2.rectangle(frame, (startX, startY), (x, y), (255, 0, 0), -1)
    elif before == False and pressed == True:
        startX, startY = x, y
    #elif before == pressed == True:
     #   nop
        #cv2.rectangle(frame, (startX, startY), (x, y), (255, 0, 0), -1)


# cap = cv2.VideoCapture("http://192.168.1.3:4444/video")
cap = cv2.VideoCapture(0)

res, frame = cap.read()

cv2.namedWindow('tracking')
cv2.setMouseCallback('tracking',draw_rectange)



while True:
    res, frame = cap.read()

    if pressed == True:
        cv2.rectangle(frame, (startX, startY), (currentX, currentY), (0, 255, 0), -1)

    if released == True:
        tracker = cv2.Tracker_create("KCF")
        # tracker = t.OliObjectTracker(frame, (startX, startY, currentX - startX, currentY -startY))
        ok = tracker.init(frame, (startX, startY, currentX - startX, currentY -startY))
        initialized = ok
        # initialized = True
        print(ok)
    elif initialized == True:
        ok, bbox = tracker.update(frame)
        # bbox = tracker.track(frame)
        # ok = True
        print(ok)
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0,0,255))

    if res == False:
        print("failed to read frame")
        break
    else:
        cv2.imshow("tracking", frame)
        
    released = False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()