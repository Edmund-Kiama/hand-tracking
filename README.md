# 🖐️ Hand Tracking Volume Control

A computer vision project built with Python, OpenCV, and MediaPipe that uses real-time hand landmark detection to track finger positions — with the end goal of controlling system volume through hand gestures.

✅ **Complete** — Full gesture-based volume control using thumb-index distance on Linux (PulseAudio/pactl).

---

## 📌 Problem Statement

Traditional input devices (keyboard, mouse) require physical contact to control system functions. This project explores a **touchless, gesture-based interface** — specifically using the distance between the thumb and index finger as a natural, intuitive gesture to control audio volume.

The project addresses:

- How to reliably detect and track hand landmarks in real time from a webcam feed
- How to extract specific finger positions (thumb tip, index fingertip) from the landmark data
- How to map the distance between two fingers to a meaningful system output (volume)

---

## 🏗️ Project Architecture

The project is split into three files with clear separation of concerns:

```
hand-tracking-volume-control/
├── hand_prototype.py       # 📜 Original prototype (deprecated)
├── handTrackingModule.py    # ✅ Reusable HandDetector class (module)
├── volControl.py            # ⚠️  Volume control app — WIP
└── README.md
```

| File                    | Role                                                                             | Status        |
| ----------------------- | -------------------------------------------------------------------------------- | ------------- |
| `hand_prototype.py`     | Original prototype — raw MediaPipe hand tracking with FPS display                | 📜 Deprecated |
| `handTrackingModule.py` | Refactored, reusable `HandDetector` class with draw and position methods         | ✅ Complete   |
| `volControl.py`         | Complete gesture volume control with FPS, distance mapping, visual bar, `q` exit | ✅ Complete   |

---

## 🔬 How It Works

### Step 1 — Hand Detection (`hand.py` → `handTrackingModule.py`)

MediaPipe's `Hands` solution processes each webcam frame and returns **21 hand landmarks** per detected hand. Each landmark has normalized `x`, `y` coordinates that are scaled to pixel positions using the frame dimensions.

```
Landmark 0  = Wrist
Landmark 4  = Thumb tip
Landmark 8  = Index fingertip
...
```

### Step 2 — Landmark Extraction (`find_position`)

The `HandDetector.find_position()` method returns a list of `[id, cx, cy]` for every landmark, making it easy to query specific finger positions:

```python
lm_list = detector.find_position(frame)
thumb = lm_list[4]   # Thumb tip
finger = lm_list[8]  # Index fingertip
```

### Step 3 — Gesture Mapping (`volControl.py` — WIP)

The current implementation draws a line between the thumb tip (landmark 4) and index fingertip (landmark 8). The next step — mapping that line's length to system volume — is not yet implemented.

**Planned mapping:**

```
Short distance (fingers pinched) → Low volume
Long distance (fingers spread)   → High volume
```

---

## 🖥️ Prerequisites

- **Python 3.7+**
- **OpenCV**
- **MediaPipe**

Install dependencies:

```bash
pipenv install
```

**Linux (PulseAudio):** pactl command available (usually pre-installed).

**Note:** No additional deps needed; uses subprocess for volume control.

### Hardware

- A working **webcam** (built-in or external)
- Adequate lighting for reliable hand detection

---

## 🚀 How to Run

### Run the prototype (deprecated)

```bash
pipenv shell && python hand_prototype.py
```

### Run the volume control app

```bash
pipenv shell && python volControl.py
```

> Pinch thumb/index close for low volume, spread for high. Visual bar + FPS/VOL display. Press `q` to exit.

---

## ✨ Features

- **Real-time hand landmark detection** using MediaPipe (21 landmarks per hand)
- **Multi-hand support** — detects up to 2 hands simultaneously
- **FPS counter** displayed on screen
- **Reusable module design** — `HandDetector` class is importable by any application
- **Landmark position list** — easy access to any fingertip coordinate by index
- **Visual overlays** — draws landmarks, connections, and fingertip circles on the frame
- **Thumb-to-index line** drawn in `volControl.py` as a visual gesture indicator

---

## ⚙️ Configuration

Tunable parameters in `HandDetector`:

| Parameter        | Default | Description                                           |
| ---------------- | ------- | ----------------------------------------------------- |
| `mode`           | `False` | Static image mode (`True`) vs. video stream (`False`) |
| `max_hands`      | `2`     | Maximum number of hands to detect                     |
| `detection_conf` | `0.5`   | Minimum detection confidence threshold                |
| `track_conf`     | `0.5`   | Minimum tracking confidence threshold                 |

---

## 🔭 Assumptions

- A **webcam** is available and accessible at device index `0`.
- The environment has **sufficient lighting** for MediaPipe to detect hands reliably.
- `find_position()` is always called **after** `find_hands()` — the method relies on `self.results` being set by `find_hands()` first.
- Landmark indices follow MediaPipe's standard hand landmark map (thumb tip = `4`, index tip = `8`).

---

## 🎉 All Features Complete!

**Linux-specific:** Uses `pactl` for PulseAudio volume control. Install PulseAudio if needed (`sudo apt install pulseaudio-utils`).

---

## 📚 References

- [MediaPipe Hands — Google](https://mediapipe.readthedocs.io/en/latest/solutions/hands.html)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Hand Landmark Model — MediaPipe](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
