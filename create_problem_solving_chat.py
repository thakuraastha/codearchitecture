from flask import Flask, request, jsonify
import cv2
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Define the directory for storing user data
USER_DATA_DIR = os.path.join("user_data")

# Define the dimensions of the app window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Define the font for the quiz questions and options
font = cv2.FONT_HERSHEY_SIMPLEX

# Define the video capture object
cap = cv2.VideoCapture(0)

# Load the images for the tutorial
tutorial_images = [
    cv2.imread(os.path.join("tutorial_images", "image1.png")),
    cv2.imread(os.path.join("tutorial_images", "image2.png")),
    cv2.imread(os.path.join("tutorial_images", "image3.png")),
]

# Define the quiz questions and answers
quiz_questions = [
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": "4",
    },
    {
        "question": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Rome"],
        "answer": "Paris",
    },
    {
        "question": "What is the tallest mountain in the world?",
        "options": ["Mount Kilimanjaro", "Mount Everest", "Mount Fuji", "Mount Rushmore"],
        "answer": "Mount Everest",
    },
]

# Define the function to display quiz questions
def display_quiz_question(frame, question, options):
    # Display the question
    cv2.putText(frame, question, (50, 50), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    # Display the options
    y_offset = 100
    for option in options:
        cv2.putText(frame, option, (50, y_offset), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        y_offset += 50

# Define the function to capture user data
def capture_user_data():
    # Capture 30 frames of video
    frames = []
    for i in range(30):
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    
    # Convert the frames to a numpy array
    data = np.array(frames)
    
    # Flatten the array and normalize the values
    data = data.reshape((data.shape[0], -1))
    data = data.astype(np.float32) / 255.0
    
    # Compute the mean of the data
    mean = np.mean(data, axis=0)
    
    # Subtract the mean from the data
    data -= mean
    
    # Compute the singular value decomposition of the data
    _, _, v = np.linalg.svd(data, full_matrices=False)
    
    # Keep the first 10 principal components
    v = v[:10, :]
    
    # Compute the feature vector for the data
    feature_vector = np.dot(data, v.T)
    
    return feature_vector.flatten()

# Define the route for the tutorial
@app.route("/tutorial", methods=["POST"])
def tutorial():
    # Load and display the first image
    current_image_index =
