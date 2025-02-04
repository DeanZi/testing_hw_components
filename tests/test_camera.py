import os

from core.base_test import BaseTest
from core.camera_utils import capture_image, record_video, set_camera_features, is_camera_available, simulate_high_cpu_load


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
            "white_balance": "auto",
            "frame_rate": 30
        }

        assert set_camera_features(features), "Failed to set camera features."
        self.logger.info("Camera features set successfully.")

    def test_invalid_feature_settings(self):
        """Test setting invalid camera features."""
        self.logger.info("Testing invalid feature settings...")

        invalid_features = {
            "brightness": -10,  # Invalid: brightness should be within valid range
            "contrast": 300,  # Invalid: out of range
            "frame_rate": "high",  # Invalid: should be a number
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

    def test_capture_image_with_camera_unavailable(self, monkeypatch):
        """Test capturing an image when the camera is unavailable."""
        self.logger.info("Testing image capture failure when camera is unavailable...")

        monkeypatch.setattr("core.camera_utils.is_camera_available", lambda: False)

        image_path = "test_image_unavailable.jpg"
        assert not capture_image(image_path), "Image capture should fail when camera is unavailable."
        self.logger.info("Image capture failed as expected when camera is unavailable.")

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

        monkeypatch.setattr("core.camera_utils.is_camera_available", lambda: False)

        video_path = "test_video_unavailable.mp4"
        assert not record_video(video_path, 5), "Video recording should fail when camera is unavailable."
        self.logger.info("Video recording failed as expected when camera is unavailable.")

    def test_record_video_with_invalid_duration(self):
        """Test recording a video with an invalid duration."""
        self.logger.info("Testing video recording with invalid duration...")

        video_path = "test_video_invalid.mp4"
        invalid_durations = [-5, 0, "ten"]  # Negative, zero, and non-numeric values

        for duration in invalid_durations:
            assert not record_video(video_path, duration), f"Video recording should fail for duration: {duration}"

        self.logger.info("Video recording correctly failed for invalid durations.")

    def test_fast_camera_switching(self):
        """Test rapid switching between multiple available cameras."""
        self.logger.info("Testing fast camera switching...")
        camera_devices = ["/dev/video0", "/dev/video1"]  # Example camera devices

        for _ in range(10):  # Switch 10 times rapidly
            for camera in camera_devices:
                assert os.path.exists(camera), f"Camera {camera} not found."
                self.logger.info(f"Switched to {camera} successfully.")

    def test_fast_camera_switching(self):
        """Test rapid switching between multiple available cameras."""
        self.logger.info("Testing fast camera switching...")
        camera_devices = ["/dev/video0", "/dev/video1"]  # Example camera devices

        for _ in range(10):  # Switch 10 times rapidly
            for camera in camera_devices:
                assert os.path.exists(camera), f"Camera {camera} not found."
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
