import cv2
import numpy as np


class WindowTracker:
    RADIUS = 20

    def __init__(self, frame, bbox):
        frame_gray = self.norm(frame)

        self.current_bbox = bbox
        self.expected = frame_gray[bbox[1]:bbox[1] + bbox[3],
                                   bbox[0]:bbox[0] + bbox[2]]

    def norm(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) / 255

    def track(self, frame):
        frame_gray = self.norm(frame)

        bbox = self.current_bbox

        best_error_value = -1
        best_error_location = (0, 0)

        # extend window by r pixel
        # current_window = frame_gray[
        #     bbox[1] - WindowTracker.RADIUS:bbox[1] + WindowTracker.RADIUS + bbox[3],
        #     bbox[0] - WindowTracker.RADIUS:bbox[0] + WindowTracker.RADIUS + bbox[2]]

        r = WindowTracker.RADIUS
        for x in range(-r, r + 1):
            for y in range(-r, r + 1):
                current_window = frame_gray[
                    bbox[1] + y:bbox[1] + bbox[3] + y,
                    bbox[0] + x:bbox[0] + bbox[2] + x]
                if np.size(current_window) != bbox[3] * bbox[2]:
                    continue
                # current_window = current_window.astype(float, copy=True)

                full_errors = cv2.subtract(current_window, self.expected)
                full_errors = full_errors.reshape(1, np.size(current_window))
                error = np.sum(full_errors)

                if best_error_value == -1 or best_error_value > error:
                    best_error_value = error
                    best_error_location = (x, y)

        self.current_bbox = (
            self.current_bbox[0] + best_error_location[0],
            self.current_bbox[1] + best_error_location[1],
            self.current_bbox[2],
            self.current_bbox[3]
        )

        self.expected = frame_gray[bbox[1]:bbox[1] + bbox[3],
                                   bbox[0]:bbox[0] + bbox[2]]

        return self.current_bbox
