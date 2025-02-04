import logging


class BaseTest:
    """Base class for all hardware tests, ensuring reusability."""

    def setup_method(self):
        """Set up the hardware test environment (override if needed)."""
        self.logger = logging.getLogger(self.__class__.__name__)  # Create a logger instance
        self.logger.setLevel(logging.INFO)  # Ensure log level is set

        handler = logging.FileHandler("test_logs.log")  # File handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        if not self.logger.hasHandlers():  # Prevent duplicate handlers
            self.logger.addHandler(handler)

    def run_test(self):
        """Execute test logic (override in child classes)."""
        raise NotImplementedError("run_test method must be implemented.")

    def teardown(self):
        """Cleanup after test execution."""
        self.logger.info(f"{self.__class__.__name__} test completed.")
