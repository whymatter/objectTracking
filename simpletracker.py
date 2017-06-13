import cv2
import numpy as np
import time


class OliObjectTracker:
    def __init__(self, frame, bbox):
        self.bbox = bbox
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.expected = gray[bbox[1]:bbox[1] +
                             bbox[3], bbox[0]:bbox[0] + bbox[2]]
        self.time1 = 0
        self.time2 = 0

    def track(self, frame):
        bbox = self.bbox
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        best_error_value = -1
        best_error_location = (0, 0)
        r = 10

        for x in range(-r, r + 1):
            for y in range(-r, r + 1):
                s = time.time()

                current_window = frame_gray[
                    bbox[1] + y:bbox[1] + bbox[3] + y,
                    bbox[0] + x:bbox[0] + bbox[2] + x]
                if np.size(current_window) != bbox[3] * bbox[2]: continue
                current_window = current_window.astype(float, copy=True)

                self.time1 += time.time() - s

                s = time.time()

                # full_errors = (current_window - self.expected)
                full_errors = np.subtract(current_window, self.expected)
                full_errors = full_errors.reshape(1, np.size(current_window))
                error = np.sum(full_errors)
                
                self.time2 += time.time() - s

                if best_error_value == -1 or best_error_value > error:
                    best_error_value = error
                    best_error_location = (x, y)

        # print("time1 " + repr(self.time1))
        # print("time2 " + repr(self.time2))

        self.bbox = (
            self.bbox[0] + best_error_location[0],
            self.bbox[1] + best_error_location[1],
            self.bbox[2],
            self.bbox[3]
        )

        self.expected = frame_gray[bbox[1]:bbox[1] + bbox[3],
                             bbox[0]:bbox[0] + bbox[2]]

        return self.bbox
