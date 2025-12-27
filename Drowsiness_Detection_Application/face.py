import cv2
import numpy as np
import pygame
import time
import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading

pygame.mixer.init()
alarm_sound = pygame.mixer.Sound("alarm.mp3")

EYE_AR_THRESH = 0.3   # Increased for faster response
EYE_AR_CONSEC_FRAMES = 15  # Reduced for quicker detection
LOG_FILE = "drowsiness_log.csv"

class DrowsinessDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Drowsiness Detector")
        
        self.COUNTER = 0
        self.ALARM_ON = False
        self.running = False
        
        self.setup_ui()

        self.use_phone_camera = False
        self.cap = None
        self.initialize_camera()

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')  # Faster model
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

        self.update_preview()

    def initialize_camera(self):
        if self.use_phone_camera:
            self.cap = cv2.VideoCapture("https://192.0.0.4:8080/0")
        else:
            self.cap = cv2.VideoCapture(0)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.video_label = ttk.Label(main_frame)
        self.video_label.pack(pady=10)

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=10)

        self.start_btn = ttk.Button(control_frame, text="Start", command=self.start_detection)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop_detection, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.camera_btn = ttk.Button(control_frame, text="Switch Camera", command=self.switch_camera)
        self.camera_btn.pack(side=tk.LEFT, padx=5)

        log_frame = ttk.LabelFrame(main_frame, text="Detection Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.log_text = tk.Text(log_frame, height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var, 
                relief=tk.SUNKEN).pack(fill=tk.X)

    def switch_camera(self):
        self.use_phone_camera = not self.use_phone_camera
        self.cap.release()
        self.initialize_camera()

    def start_detection(self):
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.detection_thread = threading.Thread(target=self.detect_drowsiness)
        self.detection_thread.daemon = True
        self.detection_thread.start()

    def stop_detection(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def update_preview(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (320, 240))  # Smaller frame for faster processing
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.process_frame(frame)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
        self.root.after(10, self.update_preview)

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
            if len(eyes) >= 2:
                self.COUNTER = 0
                if self.ALARM_ON:
                    self.stop_alarm()
            else:
                self.COUNTER += 1
                if self.COUNTER >= EYE_AR_CONSEC_FRAMES:
                    if not self.ALARM_ON:
                        self.trigger_alarm()
                        self.log_drowsiness()
                    self.ALARM_ON = True

        status = "NORMAL" if self.COUNTER < EYE_AR_CONSEC_FRAMES else "DROWSY!"
        self.status_var.set(f"Status: {status}")

    def trigger_alarm(self):
        alarm_sound.play(-1)
        self.ALARM_ON = True

    def stop_alarm(self):
        alarm_sound.stop()
        self.ALARM_ON = False

    def log_drowsiness(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"drowsy_{timestamp.replace(':', '-')}.png"
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite(filename, frame)

        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, filename])

        self.log_text.insert(tk.END, f"{timestamp} - {filename}\n")
        self.log_text.see(tk.END)

    def on_closing(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DrowsinessDetector(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
