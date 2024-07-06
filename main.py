# doesn't  work idk why :(
import cv2
from ultralytics import YOLO
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading


model = YOLO('yolov8x.pt')

class_names = {
    0: "apple",
    1: "book",
    2: "pen",

}


cap = cv2.VideoCapture(0)

def camera_feed():
	while not stop_event.is_set():
		ret, frame = cap.read()
		if not ret:
			break
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		im = Image.fromarray(frame)
		img = ImageTk.PhotoImage(image=im)
		camera_label.configure(image=img)
		camera_label.image = img
	cap.release()


def capture_and_analyze():
    global cap
    ret, frame = cap.read()
    if not ret:
        return
    results = model(frame)
    print(results)  

    detected_objects = process_results(results)  


    if any(obj in detected_objects for obj in ["apple", "book", "pen"]):
        result_text.set("Object detected. You can pass.")
    else:
        result_text.set("No specified object detected. Please retake.")

def process_results(results):
    detected_objects = []
   
    for detection in results:
        class_id = int(detection[5])  
        object_name = class_names.get(class_id, "Unknown")  
        detected_objects.append(object_name)
    return detected_objects

def close_program():
    global cap
    if cap.isOpened():
        cap.release() 



root = tk.Tk()
root.title("Object Detection")

camera_label = tk.Label(root)
camera_label.pack()

captured_label = tk.Label(root)
captured_label.pack()

capture_button = ttk.Button(root, text="Capture and Analyze", command=capture_and_analyze)
capture_button.pack()

result_text = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_text)
result_label.pack()

stop_event = threading.Event()
thread = threading.Thread(target=camera_feed)
thread.start()

root.mainloop()

stop_event.set()
thread.join()

root.protocol("WM_DELETE_WINDOW", close_program) 
