import cv2
import mediapipe as mp
import pyautogui
import time
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# EAR calculation helper
def eye_aspect_ratio(landmarks, eye_indices):
    p1, p2, p3, p4, p5, p6 = [landmarks[i] for i in eye_indices]
    A = ((p2.x - p6.x)**2 + (p2.y - p6.y)**2) ** 0.5
    B = ((p3.x - p5.x)**2 + (p3.y - p5.y)**2) ** 0.5
    C = ((p1.x - p4.x)**2 + (p1.y - p4.y)**2) ** 0.5
    return (A + B) / (2.0 * C)

# Eye indices from Mediapipe FaceMesh
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]

# Thresholds
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 3
LONG_BLINK_FRAMES = 20  # ~1 sec if ~20 FPS
DOUBLE_BLINK_GAP = 0.5  # seconds

frame_counter = 0
blink_count = 0
last_blink_time = 0
action_label = ""   # what to display on screen

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
        right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
        ear = (left_ear + right_ear) / 2.0

        if ear < EAR_THRESHOLD:
            frame_counter += 1
        else:
            if frame_counter >= CONSEC_FRAMES:
                current_time = time.time()

                if frame_counter >= LONG_BLINK_FRAMES:
                    action_label = "Long Blink - Scroll"
                    pyautogui.scroll(-300)
                else:
                    if current_time - last_blink_time <= DOUBLE_BLINK_GAP:
                        action_label = "Double Blink - Right Click"
                        pyautogui.click(button="right")
                        last_blink_time = 0
                    else:
                        action_label = "Single Blink - Left Click"
                        pyautogui.click(button="left")
                        last_blink_time = current_time

                blink_count += 1

            frame_counter = 0

        # Overlay info
        cv2.putText(frame, f"Blinks: {blink_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        if action_label:
            cv2.putText(frame, action_label, (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Eye Blink Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows() 




