import os

# Video paths
INPUT_VIDEO = os.getenv("INPUT_VIDEO", "input.mp4")
OUTPUT_VIDEO = os.getenv("OUTPUT_VIDEO", "output.mp4")

# ROI coordinates (x1, y1, x2, y2)
ROI = (200, 300, 800, 600)  # Example rectangle

# Detection model (YOLOv5 pretrained small model for speed)
MODEL_PATH = os.getenv("MODEL_PATH", "yolov5s.pt")

# Tracker settings
MAX_DISAPPEAR_FRAMES = 30  # frames allowed missing before vehicle considered gone
