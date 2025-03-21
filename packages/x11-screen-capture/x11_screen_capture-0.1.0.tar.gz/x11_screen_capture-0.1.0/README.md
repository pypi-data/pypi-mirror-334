# screen_capture

[![PyPI version](https://badge.fury.io/py/screen-capture.svg)](https://badge.fury.io/py/screen-capture)
[![License: gpl-3.0](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

**A Python module for efficient screen capture and stripe-based JPEG encoding, designed for performance and flexibility.**

This module provides a Python interface to a high-performance screen capture library. It captures screen regions and encodes them into JPEG stripes, delivering them via a callback mechanism. This stripe-based approach can be beneficial for streaming or processing screen capture data efficiently.

## Installation

Due to its reliance on a native module, installation is slightly different from typical Python packages.

1. **Prerequisites:** Ensure you have CMake, x11 dev files, xxhash dev files, libext dev files, and libjpeg-turbo dev files installed on your system.
2. **Install via pip:**

   ```bash
   sudo apt-get update && \
   sudo apt-get install -y \
     cmake \
     g++ \
     gcc \
     libjpeg62-turbo-dev \
     libx11-dev \
     libxext-dev \
     libxxhash-dev \
     make \
     python3-dev
   ```

   ```bash
   pip install screen_capture
   ```

   This command will:
   - Build the native `screen_capture_module.so` library using CMake during the installation process.
   - Install the Python wrapper and the compiled shared library.

**Note:** This package is currently designed and tested for **Linux** environments as indicated in the `setup.py` classifiers.

## Usage

### Basic Capture

Here's a basic example of how to use the `screen_capture` module to start capturing the screen and process the encoded JPEG stripes.

```python
import ctypes
from screen_capture import CaptureSettings, ScreenCapture

def my_stripe_callback(result_ptr, user_data):
    """Callback function to process encoded JPEG stripes."""
    result = result_ptr.contents
    if result.data:
        data_bytes = ctypes.cast(
            result.data, ctypes.POINTER(ctypes.c_ubyte * result.size)
        ).contents
        jpeg_stripe_data = bytes(data_bytes)
        # Process the jpeg_stripe_data here (e.g., save to file, stream, etc.)
        print(f"Received JPEG stripe: y_start={result.stripe_y_start}, height={result.stripe_height}, size={result.size} bytes")
    else:
        print("Callback received empty stripe data.")

# Configure capture settings
capture_settings = CaptureSettings()
capture_settings.capture_width = 1920  # Example: Capture width
capture_settings.capture_height = 1080 # Example: Capture height
capture_settings.capture_x = 0        # Capture from top-left corner
capture_settings.capture_y = 0
capture_settings.target_fps = 30.0
capture_settings.jpeg_quality = 75

# Instantiate the ScreenCapture module
module = ScreenCapture()

try:
    module.start_capture(capture_settings, my_stripe_callback)
    input("Press Enter to stop capture...") # Keep capture running until Enter is pressed
finally:
    module.stop_capture()
    print("Capture stopped.")
```

### Capture Settings

The `CaptureSettings` class allows you to configure various parameters for screen capture:

```python
class CaptureSettings(ctypes.Structure):
    _fields_ = [
        ("capture_width", ctypes.c_int),          # Width of the capture region
        ("capture_height", ctypes.c_int),         # Height of the capture region
        ("capture_x", ctypes.c_int),              # X coordinate of the top-left corner of the capture region
        ("capture_y", ctypes.c_int),              # Y coordinate of the top-left corner of the capture region
        ("target_fps", ctypes.c_double),          # Target frames per second
        ("jpeg_quality", ctypes.c_int),           # JPEG quality for standard encoding (0-100)
        ("paint_over_jpeg_quality", ctypes.c_int), # JPEG quality when "paint-over" detection triggers (0-100)
        ("use_paint_over_quality", ctypes.c_bool), # Enable/disable paint-over quality adjustment
        ("paint_over_trigger_frames", ctypes.c_int),# Number of frames to trigger paint-over quality
        ("damage_block_threshold", ctypes.c_int),   # Threshold for damage detection (motion detection)
        ("damage_block_duration", ctypes.c_int),    # Duration to consider damage blocks for paint-over
    ]
```

Adjust these settings to fine-tune capture performance and quality based on your needs.

### Stripe Callback

The `start_capture` function requires a callback function of type `StripeCallback`. This callback is invoked by the native module whenever a JPEG encoded stripe is ready.

```python
StripeCallback = ctypes.CFUNCTYPE(
    None, ctypes.POINTER(StripeEncodeResult), ctypes.c_void_p
)
```

Your Python callback function should accept two arguments:

- `result_ptr`: A ctypes pointer to a `StripeEncodeResult` structure containing the encoded JPEG stripe data and metadata.
- `user_data`:  Currently unused in the `start_capture` signature (set to `None` in the example).

Inside the callback, you are responsible for processing the `StripeEncodeResult` data. **Crucially, you do not need to manually free the memory of `result.data` as the Python wrapper handles this by calling `free_stripe_encode_result_data` after your callback returns.**

## Features

* **Efficient Screen Capture:** Leverages a native module for optimized screen capture performance.
* **Stripe-Based JPEG Encoding:** Encodes captured frames into horizontal stripes based on system core count. The end result being minimal system load at high framerates.
* **Configurable Capture Region:** Specify the exact region of the screen to capture.
* **Adjustable FPS and JPEG Quality:** Control the capture frame rate and JPEG compression level.
* **Paint-Over Detection and Quality Adjustment:** Dynamically adjusts JPEG quality based on screen content changes for optimized bandwidth usage.
* **Direct Callback Mechanism:**  Provides captured data directly to your Python code via a callback function for real-time processing.

## Example

For a more complete example of using `screen_capture` for streaming over WebSockets, please refer to the `examples` directory. This example demonstrates:

* Setting up a WebSocket server.
* Using the `screen_capture` module to capture screen and encode JPEG stripes.
* Sending the JPEG stripes to connected WebSocket clients for real-time streaming.
* Serving a basic HTML page to view the stream.

Once the module is installed it can be run with:

```
cd example
python3 screen_to_browser.py
```

Then land on http://localhost:9001

## License

This project is licensed under the **MIT License**.
