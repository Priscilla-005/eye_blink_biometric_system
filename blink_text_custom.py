import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import messagebox
import pyttsx3
import time

# ---------------- SETUP ---------------- #
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
engine = pyttsx3.init()

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]

EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 3
DOUBLE_BLINK_GAP = 0.6

frame_counter = 0
last_blink_time = 0

# ---------------- DEFAULT MESSAGES ---------------- #
messages = ["Yes", "No", "I need water", "Call doctor", "I am in pain", "Thank you"]
index = 0

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title("Blink Communication System")
root.geometry("550x400")
root.configure(bg="#101820")

label_title = tk.Label(root, text="Blink Communication System", font=("Arial", 18, "bold"), fg="#FEE715", bg="#101820")
label_title.pack(pady=10)

label_msg = tk.Label(root, text="", font=("Arial", 22), fg="white", bg="#101820")
label_msg.pack(pady=40)

label_info = tk.Label(root, text="Blink once → Next | Blink twice → Speak | ESC to Exit", font=("Arial", 12),
                      fg="#FEE715", bg="#101820")
label_info.pack(side="bottom", pady=10)

# ---------------- ADD CUSTOM MESSAGE ---------------- #
def add_message():
    new_msg = entry_msg.get().strip()
    if new_msg:
        messages.append(new_msg)
        entry_msg.delete(0, tk.END)
        messagebox.showinfo("Added", f"Message '{new_msg}' added successfully!")
    else:
        messagebox.showwarning("Error", "Please enter a valid message.")

frame_add = tk.Frame(root, bg="#101820")
frame_add.pack(pady=5)
entry_msg = tk.Entry(frame_add, width=25, font=("Arial", 12))
entry_msg.grid(row=0, column=0, padx=5)
btn_add = tk.Button(frame_add, text="Add Message", font=("Arial", 10, "bold"), command=add_message, bg="#FEE715")
btn_add.grid(row=0, column=1)

# ---------------- FUNCTION ---------------- #+
def update_gui(selected_msg):
    label_msg.config(text=selected_msg)
    root.update()

def eye_aspect_ratio(landmarks, eye_indices):
    p = np.array([(landmarks[i].x, landmarks[i].y) for i in eye_indices])
    A = np.linalg.norm(p[1] - p[5])
    B = np.linalg.norm(p[2] - p[4])
    C = np.linalg.norm(p[0] - p[3])
    return (A + B) / (2.0 * C)

# ---------------- CAMERA ---------------- #
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not found!")
    exit()

print("Blink Communication System started...")
engine.say("Blink Communication System started")
engine.runAndWait()

current_message = messages[index]
update_gui(current_message)

# ---------------- MAIN LOOP ---------------- #
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
        right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
        ear = (left_ear + right_ear) / 2.0

        single_blink = False
        double_blink = False

        if ear < EAR_THRESHOLD:
            frame_counter += 1
        else:
            if frame_counter >= CONSEC_FRAMES:
                current_time = time.time()
                if current_time - last_blink_time <= DOUBLE_BLINK_GAP:
                    double_blink = True
                    last_blink_time = 0
                else:
                    single_blink = True
                    last_blink_time = current_time
            frame_counter = 0

        # Blink actions
        if single_blink:
            index = (index + 1) % len(messages)
            current_message = messages[index]
            update_gui(current_message)

        if double_blink:
            engine.say(current_message)
            engine.runAndWait()
            update_gui(f"🗣️ Speaking: {current_message}")
            time.sleep(1)
            update_gui(current_message)

    cv2.imshow("Blink Detector", frame)
    root.update()

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
root.destroy()
