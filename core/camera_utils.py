from gi import require_version
require_version('Gst', '1.0')  # Specify version before importing
from gi.repository import Gst
import subprocess
import os
import time
import cv2


def is_camera_available(camera_index=0):
    """Check if the camera is available by trying to open it."""
    cap = cv2.VideoCapture(camera_index)
    available = cap.isOpened()
    cap.release()  # Always release the capture object
    return available


def set_camera_features(features):
    """Validating inputs first."""
    VALID_FEATURES = {
        "brightness": (0, 100),  # Example range
        "contrast": (0, 100),
        "backlight_compensation": (0, 1),
        "sharpness": (0, 100)
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

    # If all values are valid, apply settings (mocked for now)
    print(f"Camera features set successfully: {features}")
    return True


def occupy_camera():
    """Function to occupy the camera for a while (simulating another process)."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera is unavailable.")
        return
    print("Camera is now occupied.")
    time.sleep(5)  # Keep the camera occupied for 5 seconds
    cap.release()
    print("Camera released.")


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
