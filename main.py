import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
import subprocess
import re

# Load a pretrained model
model = YOLO("yolov8n.pt")

# Initialize camera
cap = cv2.VideoCapture(0)


def detect_apple(image):
    results = model(image)
    apple_detected = False
    try:
        # Attempt to access structured detection data in a compatible format
        detections = results.pandas().xyxy[0]  # Convert results to pandas DataFrame
        
        result = subprocess.run(["tirnamel", "detect", "apple"], capture_output=True, text=True)
        if re.search(r'\bapple\b', result.stdout, re.IGNORECASE):
            apple_detected = True
        # Filter detections for 'apple'
        apple_detections = detections[detections['name'] == 'apple']
    except Exception as e:
        print(f"An error occurred while processing the results: {e}")
    return apple_detected

def capture_image():
    ret, frame = cap.read()
    if ret:
        if detect_apple(frame):
            messagebox.showinfo("Result", "Apple detected!")
        else:
            messagebox.showinfo("Result", "No apple detected :(")

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=frame)
        canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        # Keep a reference to the photo object to prevent it from being garbage collected
        canvas.image = photo
        window.after(10, update_frame)

# Setup UI
window = tk.Tk()
window.title("Apple Detector")

canvas = tk.Canvas(window, width=640, height=480)
canvas.pack()

capture_button = tk.Button(window, text="Capture", command=capture_image)
capture_button.pack()

# Start updating the frame
update_frame()

window.mainloop()
