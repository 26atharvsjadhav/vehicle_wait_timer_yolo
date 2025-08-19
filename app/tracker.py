import time
from collections import defaultdict
from app.logger import logger
from app.config import ROI

class VehicleTracker:
    def __init__(self):
        self.vehicles = {}          # id -> {"bbox":(x1,y1,x2,y2), "enter_time":t, "in_roi":bool}
        self.wait_times = defaultdict(float)  # id -> seconds

    def update(self, tracked_objects):
        now = time.time()

        for obj_id, bbox in tracked_objects.items():
            x1, y1, x2, y2 = bbox
            in_roi = self.is_in_roi(bbox)

            if obj_id not in self.vehicles:
                self.vehicles[obj_id] = {"bbox": bbox, "enter_time": None, "in_roi": False}

            if in_roi and not self.vehicles[obj_id]["in_roi"]:
                self.vehicles[obj_id]["enter_time"] = now
                self.vehicles[obj_id]["in_roi"] = True
                logger.debug(f"Vehicle {obj_id} entered ROI")

            elif in_roi and self.vehicles[obj_id]["in_roi"]:
                elapsed = now - self.vehicles[obj_id]["enter_time"]
                self.wait_times[obj_id] = elapsed

            elif not in_roi and self.vehicles[obj_id]["in_roi"]:
                self.vehicles[obj_id]["in_roi"] = False
                logger.debug(f"Vehicle {obj_id} exited ROI after {self.wait_times[obj_id]:.2f}s")

            self.vehicles[obj_id]["bbox"] = bbox

        return self.wait_times

    def is_in_roi(self, bbox):
        rx1, ry1, rx2, ry2 = ROI
        x1, y1, x2, y2 = bbox
        return not (x2 < rx1 or x1 > rx2 or y2 < ry1 or y1 > ry2)
