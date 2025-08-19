# 🚗 Vehicle Wait Timer

This project detects vehicles in a video, tracks them over time, and calculates how long each vehicle stays inside a defined **Region of Interest (ROI)**.  
The output video includes:
- Detection bounding boxes
- ROI rectangle
- Wait time displayed in `MM:SS` format above each vehicle

It uses **OpenCV** for video processing, a simple centroid-based tracker for ID persistence, and **Docker** for easy deployment.

---
🛠 Requirements

Docker installed

Video file input (placed in the project folder)

## 📂 Project Structure
vehicle_wait_timer/
├── app/
│ ├── init.py
│ ├── processor.py # Main video processing logic
│ ├── detector.py # Vehicle detection logic
│ ├── tracker.py # Vehicle tracking & wait time calculation
│ ├── config.py # Configurations (video paths, ROI)
│ ├── logger.py # Logging configuration
├── main.py # Entry point
├── Dockerfile # Docker build file
├── requirements.txt # Python dependencies
└── README.md # This file

## ⚙️ Setup & Run

pip install -r requirements.txt

## ⚙️ Build Docker
docker build -t vehicle-timer .
docker run --rm -v "C:\path\to\vehicle_wait_timer:/app" vehicle-timer (replace path with project directory)

