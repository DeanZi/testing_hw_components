from gi import require_version
import time

require_version('Gst', '1.0')  # Specify version before importing
from gi.repository import Gst
import subprocess
import re
import os
import multiprocessing


def is_camera_available():
    """Check if the camera device exists and is accessible."""
    return os.path.exists("/dev/video0")


def set_camera_features(features):
    """Validating inputs first."""
    VALID_FEATURES = {
        "brightness": (0, 100),  # Example range
        "contrast": (0, 100),
        "backlight_compensation": (0, 1),
        "sharness": (0, 100)
    }

    for key, value in features.items():
        if key not in VALID_FEATURES:
            print(f"Error: '{key}' is not a valid camera feature. ")
            False

        valid_range = VALID_FEATURES[key]
        if isinstance(valid_range, tuple):  # Numeric range
            if not isinstance(value, (int, float)) or not (valid_range[0] <= value <= valid_range[1]):
                print(f"Error: Invalid value for {key}: {value}. Should be in range {valid_range}.")
                return False
        elif isinstance(valid_range, list):  # Allowed string values
            if value not in valid_range:
                print(f"Error: Invalid value for {key}: {value}. Allowed values: {valid_range}.")
                return False

    # If all values are valid, apply settings (mocked for now)
    print(f"Camera features set successfully: {features}")
    return True


def capture_image(image_path):
    """Capture an image only if the camera is available."""
    if not is_camera_available():
        print("Error: Camera is not available. Cannot capture image.")
        return False

    result = subprocess.run(
        ["fswebcam", "--no-banner", image_path],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"Error capturing image: {result.stderr}")
        return False

    return os.path.exists(image_path)  # Ensure the file was actually created


def record_video(video_path, duration):
    """Record a video using GStreamer, ensuring the camera is available and duration is valid."""
    if not is_camera_available():
        print("Error: Camera is not available. Cannot record video.")
        return False

    if not isinstance(duration, (int, float)) or duration <= 0:
        print(f"Error: Invalid duration {duration}. Must be a positive number.")
        return False

    # Initialize GStreamer
    Gst.init(None)

    # Define the GStreamer pipeline
    pipeline_str = (
        "v4l2src ! videoconvert ! x264enc bitrate=500 speed-preset=ultrafast ! "
        "mp4mux ! filesink location={}".format(video_path)
    )

    # Create a GStreamer pipeline from the string
    pipeline = Gst.parse_launch(pipeline_str)

    # Start playing the pipeline
    pipeline.set_state(Gst.State.PLAYING)

    # Sleep for the duration of the video recording
    time.sleep(duration)

    # Stop the pipeline after the specified duration
    pipeline.set_state(Gst.State.NULL)

    # Check if the video file was created
    return os.path.exists(video_path)


def cpu_intensive_task():
    while True:
        num = 2
        while True:
            num += 1
            for i in range(2, num):
                if num % i == 0:
                    break
            else:
                pass  # Prime number found


def simulate_high_cpu_load():
    processes = []
    for _ in range(multiprocessing.cpu_count()):  # Spawn one per CPU core
        p = multiprocessing.Process(target=cpu_intensive_task)
        p.start()
        processes.append(p)

    time.sleep(10)  # Simulate high CPU load for 10 seconds

    # Terminate all processes
    for p in processes:
        p.terminate()
