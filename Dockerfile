FROM python:3.9-slim

WORKDIR /app

# Install OpenCV + video dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files & YOLO model
COPY . .

ENV INPUT_VIDEO=input.mp4
ENV OUTPUT_VIDEO=output.mp4

CMD ["python", "main.py"]
