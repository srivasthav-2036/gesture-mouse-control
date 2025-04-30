# Gesture Mouse Control 

A computer vision-based virtual mouse system that allows you to control your mouse pointer using **Hand Gestures** via your webcam. Built with OpenCV, MediaPipe, and PyAutoGUI.


## Features

- 🖱️ Cursor movement using index finger
- 👆 Left click gesture
- 👉 Right click gesture
- ✌️ Double click gesture
- 🤏 Screenshot gesture
- 🧠 AI-powered hand tracking using MediaPipe
- 🔲 On-screen gesture box to guide hand position

  
##  Preview

![Gesture Mouse Control](path_to_your_screenshot_or_demo_video)


## Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- PyAutoGUI
- pynput
- Webcam
  

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/srivasthav-2036/gesture-mouse-control.git
    ```
3. Navigate to the project directory:
   ```bash
   cd gesture-mouse-control
   ```
5. Installing required libraries:
   ```bash
   pip install opencv-python mediapipe numpy pyautogui
    ```

## Usage

1. Connect your webcam and run the program:
   python main.py

2. Follow the on-screen instructions to control your mouse with hand gestures!:
   ### Mouse Movement:
   Condition: Index finger angle >50°, thumb-index distance <50 units, also the index finger must be within the box
   ### Left Click:
   👈 Close thumb + bend index = Left Click
   <br>
   **Condition**: Index and thumb angles <50°, index and middle finger angle >50°, thumb-index distance >50 units.
   ### Right Click:
   👉 Close thumb + bend middle = Right Click
   <br>
   **Condition**: Thumb-index angle <50°, index-middle angle >90°, thumb-index distance >50 units.
   ### Double Click:
   ✌️ Bend both index and middle = Double Click
   <br>
   **Condition**: Index-thumb angle <50°, index-middle angle <50°, thumb-index distance >50 units.
   ### Screenshot:
   ✊ Close all fingers = Screenshot
   <br>
   **Condition**: Index-thumb angle <50°, index-middle angle <50°, thumb-index distance <50 units.

4. Make sure your hand stays inside the blue box for accurate tracking and gesture detection.



   
