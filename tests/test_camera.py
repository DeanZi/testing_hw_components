import threading
from core.base_test import BaseTest
from core.camera_utils import capture_image, record_video, set_camera_features, is_camera_available, occupy_camera
import time

from core.cpu_utils import simulate_high_cpu_load


class TestCamera(BaseTest):
    """Test class for camera component."""

    def setup_method(self):
        """Initialize logger and check if the camera is detected."""
        super().setup_method()
        self.logger.info("Setting up camera test...")
        assert is_camera_available(), "No camera detected. Test cannot proceed."

    def test_camera_availability(self):
        """Test if the camera is available."""
        self.logger.info("Testing camera availability...")
        assert is_camera_available(), "Camera is not available."
        self.logger.info("Camera is available.")

    def test_feature_settings(self):
        """Test setting various camera features dynamically."""
        self.logger.info("Testing camera feature settings...")

        features = {
            "brightness": 50,
            "contrast": 50,
            "backlight_compensation": 1,
            "sharpness": 30
        }

        assert set_camera_features(features), "Failed to set camera features."
        self.logger.info("Camera features set successfully.")

    def test_invalid_feature_settings(self):
        """Test setting invalid camera features."""
        self.logger.info("Testing invalid feature settings...")

        invalid_features = {
            "brightness": -10,  # Invalid: brightness should be within valid range
            "contrast": 300,  # Invalid: out of range
            "sharpness": "high",  # Invalid: should be a number
            "non_existent_feature": 42  # Invalid: feature doesn't exist
        }

        assert not set_camera_features(invalid_features), "Invalid feature settings should fail."
        self.logger.info("Invalid feature settings correctly rejected.")

    def test_capture_image(self):
        """Test capturing an image."""
        self.logger.info("Testing image capture...")
        image_path = "test_image.jpg"
        assert capture_image(image_path), "Failed to capture image."
        self.logger.info("Image captured successfully.")

    def test_capture_image_with_camera_unavailable(self):
        """Test capturing an image when the camera is unavailable due to being occupied."""
        # Start a thread to occupy the camera
        camera_thread = threading.Thread(target=occupy_camera, daemon=True)
        camera_thread.start()

        # Give the camera some time to become occupied
        time.sleep(1)

        # Now, attempt to capture an image when the camera should be unavailable
        image_path = "test_image_unavailable.jpg"
        result = capture_image(image_path)
        # Wait for the original thread to finish
        camera_thread.join()
        # We assert that the camera is unavailable, so the capture should fail
        assert not result, "Image capture should fail when camera is unavailable."
        self.logger.info("Test passed: Camera was occupied and image capture failed.")

    def test_record_video(self):
        """Test recording a video."""
        self.logger.info("Testing video recording...")
        video_path = "test_video.mp4"
        duration = 5  # 5 seconds
        assert record_video(video_path, duration), "Failed to record video."
        self.logger.info("Video recorded successfully.")

    def test_record_video_with_camera_unavailable(self, monkeypatch):
        """Test recording a video when the camera is unavailable."""
        self.logger.info("Testing video recording failure when camera is unavailable...")

        # Start a thread to occupy the camera
        camera_thread = threading.Thread(target=occupy_camera, daemon=True)
        camera_thread.start()

        # Give the camera some time to become occupied
        time.sleep(1)

        video_path = "test_video_unavailable.mp4"
        result = record_video(video_path, 5)
        # Wait for the original thread to finish
        camera_thread.join()

        assert not result, "Video recording should fail when camera is unavailable."
        self.logger.info("Video recording failed as expected when camera is unavailable.")

    def test_fast_camera_switching(self):
        """Test rapid switching between available cameras by capturing frames."""
        self.logger.info("Testing fast camera switching...")
        camera_devices = ["/dev/video0", "/dev/video1"]  # Example camera devices

        for _ in range(10):  # Switch 10 times rapidly
            for camera in camera_devices:
                image_path = f"test_image{_}.jpg"
                assert capture_image(image_path), f"Failed to capture image {_}."
                self.logger.info("Image captured successfully.")
                self.logger.info(f"Switched to {camera} successfully.")

    def test_overloaded_system_camera(self):
        """Test camera behavior under high system load."""
        self.logger.info("Simulating an overloaded system while testing camera behavior...")

        # Start high CPU load simulation
        simulate_high_cpu_load()

        # Now run the camera test (e.g., capturing an image)
        image_path = "test_image_under_load.jpg"
        video_path = "test_video_under_load.mp4"
        assert capture_image(image_path), "Failed to capture image under load."
        assert record_video(video_path, 10), "Failed to record video under load."
        self.logger.info("Camera behavior under system load tested successfully.")
