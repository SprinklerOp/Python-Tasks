import tkinter as tk
from tkinter import messagebox
import cv2
import mediapipe as mp
import time
from threading import Thread

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Define the multiple-choice questions and answers
questions = [
    {"question": "What is the full form of AWS?", 
     "options": ["Amazon web-based service", "Amazon web-store service", "Amazon web service", "Amazon web-data service"], 
     "answer": 3},
    {"question": "Which AWS service provides a fully managed, scalable, and serverless data warehouse?", 
     "options": ["Amazon S3", "Amazon RDS", "AWS Redshift", "AWS Glue"], 
     "answer": 3},
    {"question": "What AWS service is used to create and manage virtual private networks (VPNs) in the cloud?", 
     "options": ["Amazon VPC", "Amazon EC2", "AWS Direct Connect", "Amazon Route 53"], 
     "answer": 1},
    {"question": "What is the purpose of AWS Lambda?", 
     "options": ["Managing databases in the cloud", "Storing and retrieving large amounts of data", 
                 "Scaling EC2 instances automatically", "Running code without provisioning or managing servers"], 
     "answer": 4},
    {"question": "Which AWS service provides a scalable, fully managed NoSQL database?", 
     "options": ["Amazon S3", "AWS Lambda", "Amazon DynamoDB", "Amazon Redshift"], 
     "answer": 3},
    {"question": "What AWS service can be used to monitor and gain insights into application performance?", 
     "options": ["AWS CloudTrail", "AWS Config", "AWS CloudWatch", "AWS Trusted Advisor"], 
     "answer": 3},
    {"question": "Which AWS service provides serverless functions that can be executed in response to events?", 
     "options": ["Amazon S3", "AWS Lambda", "Amazon EC2", "Amazon Redshift"], 
     "answer": 2},
    {"question": "Which AWS service can be used to manage and monitor containerized applications?", 
     "options": ["AWS Elastic Beanstalk", "Amazon EKS", "Amazon ECS", "AWS CodeDeploy"], 
     "answer": 3},
    {"question": "Which AWS service provides managed file storage for EC2 instances?", 
     "options": ["Amazon S3", "AWS Lambda", "Amazon EFS", "Amazon RDS"], 
     "answer": 3},
    {"question": "What is the primary purpose of AWS Identity and Access Management (IAM)?", 
     "options": ["Managing billing and cost allocation", "Configuring network security groups", 
                 "Monitoring application performance", "Managing user access and permissions"], 
     "answer": 4}
]

# Function to count the number of raised fingers
def count_fingers(image, hand_landmarks):
    if hand_landmarks:
        landmarks = hand_landmarks[0].landmark
        fingers = []

        # Thumb
        if landmarks[mp_hands.HandLandmark.THUMB_TIP].x < landmarks[mp_hands.HandLandmark.THUMB_IP].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for lm_index in [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                         mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]:
            if landmarks[lm_index].y < landmarks[lm_index - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers.count(1)
    return 0

class MCQApp:
    def _init_(self, root):
        self.root = root
        self.root.title("MCQ Hand Gesture Recognition")
        self.root.geometry("800x600")

        self.question_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.question_label.pack(pady=20)

        self.option_labels = []
        for i in range(4):
            label = tk.Label(root, text="", font=("Helvetica", 14))
            label.pack(pady=5)
            self.option_labels.append(label)

        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 14), fg="green")
        self.feedback_label.pack(pady=20)

        self.score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 14))
        self.score_label.pack(pady=10)

        self.current_question = 0
        self.correct_answer_given = False
        self.score = 0

        self.cap = cv2.VideoCapture(0)
        self.video_label = tk.Label(root)
        self.video_label.pack(pady=10)
        
        self.update_question()
        self.update_frame()

    def update_question(self):
        question = questions[self.current_question]
        self.question_label.config(text=question["question"])
        for idx, option in enumerate(question["options"], 1):
            self.option_labels[idx-1].config(text=f"{idx}. {option}")

    def check_answer(self, finger_count):
        question = questions[self.current_question]
        if finger_count == question["answer"]:
            self.feedback_label.config(text="Correct!", fg="green")
            self.correct_answer_given = True
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
        else:
            self.feedback_label.config(text="Incorrect. Try again.", fg="red")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                finger_count = count_fingers(frame, result.multi_hand_landmarks)
                if 0 < finger_count <= 4:
                    self.check_answer(finger_count)
                    if self.correct_answer_given:
                        time.sleep(2)
                        self.correct_answer_given = False
                        self.current_question += 1
                        if self.current_question >= len(questions):
                            messagebox.showinfo("Quiz Completed", f"You have completed the quiz! Your score is {self.score}.")
                            self.root.quit()
                        else:
                            self.update_question()

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (640, 480))
            self.img = tk.PhotoImage(master=self.root, data=cv2.imencode('.png', img)[1].tobytes())
            self.video_label.config(image=self.img)

        self.root.after(10, self.update_frame)

if _name_ == "_main_":
    root = tk.Tk()
    app = MCQApp(root)
    root.mainloop()
