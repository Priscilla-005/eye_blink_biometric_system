# eye_blink_biometric_system
Eye Blink Biometric Communication System

A computer-vision based assistive communication system that uses **real-time eye blink detection** to let non-verbal or mobility-limited users communicate without a keyboard, mouse, or speech. Built for accessibility use cases such as patients with ALS, paralysis, or post-surgical recovery.

The system tracks facial landmarks via a webcam, computes the **Eye Aspect Ratio (EAR)** in real time, and classifies blinks as **single** or **double (long)** to drive an on-screen AAC (augmentative and alternative communication) interface.
## Features
### Blink Communication System (`blink_communication.py`)
A GUI-based AAC tool for non-verbal users.
- Cycles through a list of preset phrases ("Yes", "No", "I need water", "Call doctor", "I am in pain", "Thank you")
- **Single blink** → move to the next message
- **Double (long) blink** → speak the currently selected message aloud (text-to-speech)
- Custom messages can be added live through the GUI input field
- Tkinter interface displays the active message in large, high-contrast text
- Voice output powered by `pyttsx3` (offline TTS, no internet required)

---

## How It Works

1. **Face landmark detection** — [MediaPipe Face Mesh](https://google.github.io/mediapipe/solutions/face_mesh.html) detects 468 facial landmarks per frame, including refined iris/eye landmarks.
2. **Eye Aspect Ratio (EAR)** — For each eye, EAR is computed from six landmark points:

   ```
   EAR = (‖p2 - p6‖ + ‖p3 - p5‖) / (2 × ‖p1 - p4‖)
   ```

   EAR stays roughly constant when the eye is open and drops sharply when it closes.
3. **Blink classification** — EAR is compared against a threshold (`0.25`) across consecutive frames (`CONSEC_FRAMES = 3`) to filter out noise. A blink that closes and reopens within the `DOUBLE_BLINK_GAP` window of the previous blink is classified as a **double blink**; otherwise it's a **single blink**.
4. **Action dispatch** — Single blink advances the message list; double blink speaks the current message aloud via text-to-speech.

---

## Tech Stack

| Component | Purpose |
|---|---|
| OpenCV (`cv2`) | Webcam capture and frame processing |
| MediaPipe | Facial landmark detection (Face Mesh) |
| NumPy | EAR vector math |
| Tkinter | GUI for the communication assistant |
| pyttsx3 | Offline text-to-speech |

---

## Installation

```bash
pip install opencv-python mediapipe numpy pyttsx3
```

> **Note:** A working webcam is required. On Windows, `pyttsx3` uses SAPI5; on macOS it uses NSSpeechSynthesizer; on Linux, ensure `espeak` is installed (`sudo apt install espeak`).

---

##  Usage

```bash
python blink_communication.py
```
- Blink once to cycle through phrases.
- Blink twice (a longer/double blink) to have the current phrase spoken aloud.
- Type a custom phrase into the input box and click **Add Message** to extend the phrase list.
- Press **ESC** (with the camera window focused) to exit.

---

##  Project Structure

```
.
├── blink_communication.py     # AAC tool: message cycling + text-to-speech
└── README.md
```

---

##  Use Cases

- Assistive communication for non-verbal or speech-impaired individuals
- Bedside/ICU communication for patients who cannot speak or gesture
- Rehabilitation and accessibility research prototypes
- Low-cost, camera-only alternative to specialized eye-tracking hardware

---

##  Limitations

- Accuracy depends on lighting conditions and camera quality.
- A single fixed EAR threshold (`0.25`) may not generalize well across users — per-user calibration is recommended for production use.
- No blink-vs-wink or intentional-vs-involuntary blink discrimination yet, which could cause false triggers.
- Real-time performance depends on hardware; low-end devices may see reduced frame rate.

##  Future Improvements

- Per-user EAR calibration step at startup
- Configurable blink thresholds via a settings panel
- Support for additional gestures (e.g., eyebrow raise, head tilt) as extra control channels
- Logging/analytics for clinical or accessibility research use
- Packaging as a standalone executable for non-technical end users

---

## 📄 License

Specify your preferred license here (e.g., MIT).
