# 🚗 Driver Simulator

A hand-gesture-based driving simulator using OpenCV, MediaPipe, and pynput. Control your favorite driving games with just your hands! 🖐️🕹️

---
<p float="left">
  <img src="https://github.com/LuizAlencar17/webcam-game-controller-v2/blob/main/images/1.gif" width="45%" />
  <img src="https://github.com/LuizAlencar17/webcam-game-controller-v2/blob/main/images/2.gif" width="45%" />
</p>

## ✨ Features
- 👐 Detects two hands and simulates steering and acceleration.
- 🏎️ Visual steering wheel overlay for immersive feedback.
- ⌨️ Keyboard control for driving games (W, A, D keys).
- 🎥 Adjustable camera resolution for performance.
- 🖼️ Real-time hand landmark visualization.
- 🛑 Safety: Automatically releases keys if hands are not detected.

## 📦 Requirements
- Python 3.8+
- opencv-python
- mediapipe
- pynput
- numpy

Install all dependencies with:
```powershell
pip install opencv-python mediapipe pynput numpy
```

## 🚀 Usage
1. Make sure your webcam is connected and working.
2. Run the simulator:
   ```powershell
   python main.py
   ```
3. Place both hands in view of the camera. The simulator will detect your hands and simulate driving controls.
4. Press `q` to quit.

## 🛠️ How It Works
- The webcam feed is processed in real-time using MediaPipe to detect hand landmarks.
- The angle between your hands determines the steering direction (left/right/straight).
- The simulator overlays a virtual steering wheel on the video feed.
- Keyboard events are sent to simulate acceleration and steering in driving games.

## 📝 Project Structure
```
driver-simulator/
├── camera_utils.py         # Camera initialization and settings
├── controls.py            # Keyboard control logic
├── hand_detection.py      # Hand detection and drawing
├── main.py                # Main application entry point
├── steering_wheel.py      # Steering wheel drawing and angle calculation
├── tests/                 # Test folder (placeholder)
└── README.md              # This file
```

## ❓ Troubleshooting
- If the camera is not detected, check your webcam connection and permissions.
- For better performance, try lowering the camera resolution in `camera_utils.py`.
- If hand detection is unreliable, ensure good lighting and keep hands visible.

## 🤝 Contributing
Pull requests and suggestions are welcome! Feel free to open an issue or submit a PR.

## 📄 License
MIT License

---

Enjoy your virtual driving experience! 🏁
