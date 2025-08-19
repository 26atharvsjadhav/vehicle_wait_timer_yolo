from ultralytics import YOLO
from app.logger import logger

class VehicleDetector:
    def __init__(self, model_path="yolov5s.pt"):
        logger.info("Loading detection model...")
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, verbose=False)
        detections = []
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                if label in ["car", "truck", "bus", "motorbike"]:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    detections.append((x1, y1, x2, y2, label, float(box.conf[0])))
        return detections
