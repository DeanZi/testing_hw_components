from gi import require_version
require_version('Gst', '1.0')  # Specify version before importing
from gi.repository import Gst
import subprocess
import re
import os
import time


def is_camera_available():
    """Check if the camera device exists and is accessible."""
    return os.path.exists("/dev/video0")


def get_camera_controls():
    """Retrieve available camera controls."""
    command = "v4l2-ctl --list-ctrls"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    controls = {}
    if result.returncode == 0:
        for line in result.stdout.split("\n"):
            match = re.match(r"\s*(\S+) \((\w+)\).*", line)
            if match:
                controls[match.group(1)] = match.group(2)  # e.g., {'brightness': 'int', 'contrast': 'int'}
    return controls


def set_camera_features(features):
    """Set only the features that are supported by the camera."""
    available_controls = get_camera_controls()  # Fetch controls once inside the function
    commands = []

    feature_map = {
        "brightness": "brightness",
        "contrast": "contrast",
        "white_balance": "white_balance_temperature_auto",
        "frame_rate": "frame_rate"
    }

    for key, value in features.items():
        actual_control = feature_map.get(key)
        if actual_control and actual_control in available_controls:
            if key == "white_balance":
                value = 1 if value == "auto" else 0
            commands.append(f"v4l2-ctl --set-ctrl={actual_control}={value}")

    for command in commands:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to apply setting: {command}")
            return False

    return True


def capture_image(image_path):
    """Capture an image using fswebcam."""
    result = subprocess.run(["fswebcam", image_path], capture_output=True, text=True)
    return result.returncode == 0 and os.path.exists(image_path)


def record_video(video_path, duration):
    """Record a video using GStreamer for the specified duration without subprocess."""
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
