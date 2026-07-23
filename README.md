# ✋ Real-Time Hand Tracking & Gesture Control

A real-time computer vision project built with** ** **Python** ,** ** **OpenCV** , and** ** **MediaPipe** .

The project uses a webcam to track human hands, extract their** ** **21 hand landmarks** , recognize hand gestures, and interact with different visualization modes in real time.

The current implementation allows the user to switch between visualization modes by** ** **closing and reopening their hand** . A closed fist acts as a gesture-based control input.

---

## ✨ Features

* 🎥 Real-time webcam input
* ✋ Real-time hand tracking
* 🖐️ Detection of up to two hands
* 📍 Extraction of 21 landmarks for each hand
* 🎯 Conversion of normalized MediaPipe coordinates into pixel coordinates
* 🟢 Real-time landmark visualization
* 🔴 Custom connections between hand landmarks
* 🤖 Gesture recognition using MediaPipe Gesture Recognizer
* ✊ Closed-fist gesture used to switch visualization modes
* 🔄 Real-time mode switching
* 🖥️ Live gesture visualization on the webcam feed

---

## 🧠 How It Works

The project uses two separate MediaPipe systems that process the same camera frame:

```text
                    Webcam
                       │
                       ▼
                  OpenCV Frame
                       │
                       ▼
                  BGR → RGB
                       │
                       ▼
                MediaPipe Image
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       Hand Landmarker     Gesture Recognizer
             │                   │
             ▼                   ▼
       21 Hand Landmarks    Gesture Category
             │                   │
             │                   ▼
             │              "Closed_Fist"
             │                   │
             │                   ▼
             │              Mode Switch
             │                   │
             └─────────┬─────────┘
                       ▼
                  Visualization
                       │
                       ▼
                  Webcam Output
```

### Hand Landmarker

The** ****Hand Landmarker** is responsible for detecting the hand and returning its 21 landmarks.

These landmarks are used to:

* Draw points on the hand
* Calculate pixel coordinates
* Identify specific fingers
* Connect landmarks
* Create geometric structures
* Build future 2D and 3D visualizations

The project currently tracks up to two hands.

### Gesture Recognizer

The** ****Gesture Recognizer** is used exclusively for gesture detection.

It recognizes predefined hand gestures such as:

```text
Closed_Fist
Open_Palm
Victory
Thumb_Up
Thumb_Down
Pointing_Up
ILoveYou
```

The recognized gesture is displayed directly on the webcam feed.

---

## 📍 Hand Landmarks

Each detected hand contains 21 predefined landmarks.

```text
0       Wrist

1–4     Thumb
5–8     Index Finger
9–12    Middle Finger
13–16   Ring Finger
17–20   Pinky
```

Some important landmarks used in the current project are:

```text
4  → Thumb Tip
8  → Index Finger Tip
```

These points are used to create custom connections between the two tracked hands.

---

## 🎮 Gesture-Based Mode Switching

The project uses the** **`Closed_Fist` gesture as a control input.

When the user closes their hand, the program switches to the next visualization mode.

The program does not continuously switch modes while the fist remains closed.

Instead, the gesture must follow this sequence:

```text
🖐️ Open Hand
      │
      ▼
✊ Close Hand
      │
      ▼
Mode Changes
      │
      ▼
✊ Keep Hand Closed
      │
      ▼
No Additional Change
      │
      ▼
🖐️ Open Hand
      │
      ▼
✊ Close Hand Again
      │
      ▼
Next Mode
```

This behavior is controlled by the** **`fist_triggered` variable.

The variable prevents the same closed fist from triggering multiple mode changes while the hand remains closed.

---

## 🔄 Visualization Modes

The project currently uses a mode-based visualization system.

### Mode 1 — Finger Connections

When two hands are detected, the program connects:

* Left thumb → Right thumb
* Left index → Right index
* Left thumb → Left index
* Right thumb → Right index

The result is a custom geometric structure between the two hands.

```text
        Thumb ───────── Thumb
           │               │
           │               │
        Index ────────── Index
```

### Mode 2 — 3D Visualization

The second mode is currently reserved for future development.

The goal is to use the hand landmarks and their depth information to create a three-dimensional geometric structure.

---

## 📐 Coordinate Conversion

MediaPipe returns normalized landmark coordinates.

The** **`x` and** **`y` values range approximately from:

```text
0.0 → 1.0
```

These coordinates are converted into pixel coordinates using the dimensions of the camera frame:

```python
x = int(landmark.x * width)
y = int(landmark.y * height)
```

This allows the landmarks to be drawn directly on the OpenCV frame.

---

## 🛠️ Technologies

* **Python**
* **OpenCV**
* **MediaPipe Tasks API**

MediaPipe components used:

* `HandLandmarker`
* `GestureRecognizer`

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Enter the project directory:

```bash
cd YOUR_REPOSITORY
```

Install the required dependencies:

```bash
pip install opencv-python mediapipe
```

---

## 📁 Project Structure

The project expects the following structure:

```text
project/
│
├── main.py
│
├── models/
│   ├── hand_landmarker.task
│   └── gesture_recognizer.task
│
└── README.md
```

The two** **`.task` files are the MediaPipe models required by the project.

---

## ▶️ Running the Project

Run the program with:

```bash
python main.py
```

The webcam window will open and display:

* Detected hand landmarks
* Custom hand connections
* Recognized gesture

The recognized gesture is displayed at the top of the webcam feed.

Press:

```text
Q
```

to exit the program.

---

## ⚙️ Camera Configuration

The camera is initialized using:

```python
cap = cv2.VideoCapture(1)
```

The number** **`1` identifies the camera device being used.

Depending on your system, you may need to change it:

```python
cap = cv2.VideoCapture(0)
```

Commonly:

```text
0 → Default / built-in camera
1 → Secondary camera
2 → Another connected camera
```

---

## ⏱️ Video Processing

The project uses MediaPipe's** **`VIDEO` running mode.

Each processed frame receives an increasing timestamp:

```python
timestamp += 33
```

A value of approximately** **`33 ms` between frames corresponds to roughly:

```text
1000 / 33 ≈ 30 FPS
```

The timestamp is required by MediaPipe to ensure that frames are processed in chronological order.

---

## 🚀 Future Development

The project is currently being developed as a foundation for real-time hand-based interaction and 3D computer vision.

Possible future improvements include:

* [ ] Implement 2D rectangle visualization
* [ ] Implement 3D rectangle visualization
* [ ] Use the** **`z` coordinate for depth information
* [ ] Create 3D geometric structures from hand landmarks
* [ ] Add temporal landmark smoothing
* [ ] Improve tracking stability
* [ ] Add more gesture-based controls
* [ ] Use different gestures for different actions
* [ ] Add gesture-based object manipulation
* [ ] Add interactive 3D graphics
* [ ] Improve camera and model configuration
* [ ] Add a graphical user interface

---

## 🎯 Project Goal

The main goal of this project is to explore the use of** ****real-time hand tracking and gesture recognition** to create interactive visual systems.

The project combines:

```text
Hand Tracking
      +
Gesture Recognition
      +
Computer Vision
      +
Geometric Visualization
```

The long-term goal is to transform hand movements and gestures into meaningful** ** **2D and 3D interactive structures** .

---

## 📄 License

This project is currently intended for educational and experimental purposes.
