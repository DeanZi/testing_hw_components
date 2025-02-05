# Testing HW Components - Camera Module

## Introduction
This project is an assignment focused on testing hardware components, starting with the camera module. The goal is to build a scalable system that can be extended to test other hardware components in the future.

## High-Level Design
The design follows a modular and extensible structure. The test framework is built using `pytest`, and logging is integrated to track the execution of tests. The camera component tests include availability checks, feature adjustments, image capture, and video recording, with additional robustness tests under system stress and high CPU load.
See [High-Level Design Document](https://github.com/DeanZi/testing_hw_components/blob/main/High-Level%20Design%20Document.pdf).

## Important Files

### `test_camera.py`
- Implements various test cases for the camera component, including:
  - Camera availability
  - Feature settings validation
  - Image capture
  - Video recording
  - Stress tests such as high CPU load and fast switching between multiple cameras
  
### `camera_utils.py`
- Provides camera-related utility functions:
  - Detecting available cameras
  - Checking camera availability
  - Setting camera features
  - Occupying the camera for concurrency tests
  - Capturing images and recording videos
  
### `cpu_utils.py`

- Simulates high CPU load for stress testing:
  - Utilizes multiprocessing to spawn processes running CPU-intensive tasks
  - Each process continuously searches for prime numbers to generate CPU load
  - Runs for a set duration before terminating all spawned processes
  


## Test Framework
- The project uses the `pytest` framework for testing.
- Logging is implemented to track test execution and failures.

## System Requirements
- The test is best run on Ubuntu 20.04 (real machine, not VM) since it attempts to detect a camera. Running in a VM will raise an error: `"No camera detected. Test cannot proceed."`


## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/DeanZi/testing_hw_components.git
cd testing_hw_components
```

### 2. Build the Docker Image
```bash
docker build --network=host -t pytest_camera_project .
```

### 3. Run the Tests
```bash
docker run --rm pytest_camera_project
```

## Future Enhancements
- Extend support for other hardware components (e.g., microphone, sensors, GPU)
- Implement additional stress testing scenarios
- Improve logging and reporting for better debugging and analytics

## Conclusion
This project provides a foundation for testing hardware components, starting with the camera module. The framework is designed to be extensible, allowing future additions of new hardware tests.

