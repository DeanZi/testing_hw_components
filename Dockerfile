# Use debian based image
FROM debian:bullseye-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    fswebcam \
    gstreamer-1.0 \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    libgirepository1.0-dev \
    pkg-config \
    libcairo2-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# PyObject Install
RUN pip install PyGObject

# Copy the rest of the project files
COPY . .

# Default command to run only the test_camera.py script
CMD ["pytest", "tests/test_camera.py", "-v"]
