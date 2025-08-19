import cv2
import math
from app.detector import VehicleDetector
from app.tracker import VehicleTracker
from app.config import INPUT_VIDEO, OUTPUT_VIDEO, ROI
from app.logger import logger


class SimpleCentroidTracker:
    def __init__(self, max_distance=50):
        self.next_id = 0
        self.objects = {}  # id -> centroid
        self.max_distance = max_distance

    def update(self, detections):
        """
        detections: list of tuples (x1, y1, x2, y2, label, conf)
        """
        updated_objects = {}
        centroids = [((x1 + x2) // 2, (y1 + y2) // 2) for x1, y1, x2, y2, *_ in detections]

        for c in centroids:
            matched_id = None
            for obj_id, prev_c in self.objects.items():
                dist = math.hypot(c[0] - prev_c[0], c[1] - prev_c[1])
                if dist < self.max_distance:
                    matched_id = obj_id
                    break

            if matched_id is None:
                matched_id = self.next_id
                self.next_id += 1

            updated_objects[matched_id] = c

        # Update stored centroids
        self.objects = updated_objects
        return updated_objects


class VideoProcessor:
    def __init__(self):
        self.detector = VehicleDetector()
        self.tracker = VehicleTracker()
        self.centroid_tracker = SimpleCentroidTracker()

    def run(self):
        cap = cv2.VideoCapture(INPUT_VIDEO)
        if not cap.isOpened():
            logger.error("Error opening video file")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(
            OUTPUT_VIDEO, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
        )

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            detections = self.detector.detect(frame)

            # Use centroid tracker for stable IDs
            object_ids = self.centroid_tracker.update(detections)
            tracked_objects = {}
            for obj_id, centroid in object_ids.items():
                for x1, y1, x2, y2, *_ in detections:
                    c = ((x1 + x2) // 2, (y1 + y2) // 2)
                    if c == centroid:
                        tracked_objects[obj_id] = (x1, y1, x2, y2)
                        break

            wait_times = self.tracker.update(tracked_objects)

            # Draw ROI
            cv2.rectangle(frame, (ROI[0], ROI[1]), (ROI[2], ROI[3]), (0, 255, 0), 2)

            # Draw vehicles + wait time
            for obj_id, bbox in tracked_objects.items():
                x1, y1, x2, y2 = bbox
                wt = wait_times.get(obj_id, 0)
                mm, ss = divmod(int(wt), 60)
                label = f"ID {obj_id} - {mm:02}:{ss:02}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            out.write(frame)

        cap.release()
        out.release()
        logger.info(f"Processing complete. Saved to {OUTPUT_VIDEO}")
