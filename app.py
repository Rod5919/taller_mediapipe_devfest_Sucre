import base64

import cv2
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)

# Create an GestureRecognizer object.
base_options = python.BaseOptions(model_asset_path='models/gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

GESTURES = {
    "Open_Palm": "Paper",
    "Victory": "Scissors",
    "Closed_Fist": "Rock",
    "None": "None"
}

def rock_paper_scissors(gesture1, gesture2):
    
    if gesture1 == "None" or gesture2 == "None":
        return
    
    global GESTURES
    
    gesture1 = GESTURES[gesture1]
    gesture2 = GESTURES[gesture2]
    
    if gesture1 == gesture2:
        return "Draw"
    elif gesture1 == "Rock":
        if gesture2 == "Paper":
            return "Right Wins"
        else:
            return "Left Wins"
    elif gesture1 == "Paper":
        if gesture2 == "Scissors":
            return "Right Wins"
        else:
            return "Left Wins"
    elif gesture1 == "Scissors":
        if gesture2 == "Rock":
            return "Right Wins"
        else:
            return "Left Wins"

def gesture_recognition(frame):

    global GESTURES

    left_gesture = None
    right_gesture = None

    # Draw dividing line
    cv2.line(frame, (frame.shape[1]//2, 0), (frame.shape[1]//2, frame.shape[0]), (0, 0, 255), 2)

    # Put Title in each half
    cv2.putText(frame, "Left", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, "Right", (frame.shape[1]//2 + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Crop image into two halves
    left, right = frame[:, :frame.shape[1]//2], frame[:, frame.shape[1]//2:]

    # Rotate left counterclockwise and right clockwise
    left = cv2.rotate(left, cv2.ROTATE_90_COUNTERCLOCKWISE)
    right = cv2.rotate(right, cv2.ROTATE_90_CLOCKWISE)
    
    # Left and right resize
    left = cv2.resize(left, (256, 256))
    right = cv2.resize(right, (256, 256))

    # Create mediapipe image object
    left_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=left)
    right_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=right)
        
    # Recognize gesture
    recognition_result_left = recognizer.recognize(left_image)
    recognition_result_right = recognizer.recognize(right_image)
    
    # Get the gesture with the highest confidence
    if len(recognition_result_left.gestures) > 0:
        left_gesture = recognition_result_left.gestures[0][0].category_name
    
    if len(recognition_result_right.gestures) > 0:
        right_gesture = recognition_result_right.gestures[0][0].category_name
    
    # Add text to the frame
    if left_gesture:
        category = GESTURES.get(left_gesture, "None")
        cv2.putText(frame, category, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    if right_gesture:
        category = GESTURES.get(right_gesture, "None")
        cv2.putText(frame, category, (frame.shape[1]//2 + 10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    # Print the winner
    if left_gesture and right_gesture:
        return {
            "winner": rock_paper_scissors(left_gesture, right_gesture),
            "frame": frame
        } 
    return {
        "winner": None,
        "frame": frame
    }        

def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

@socketio.on("connect")
def test_connect():
    print("Connected")
    emit("my response", {"data": "Connected"})

@socketio.on("image")
def receive_image(image):
    # Decode the base64-encoded image data
    image = base64_to_image(image)

    frame_resized = cv2.resize(image, (640, 480))

    # Run the recognizer
    winner, frame_resized = gesture_recognition(frame_resized).values()

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    _, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)

    processed_img_data = base64.b64encode(frame_encoded).decode()

    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data

    emit("processed_image", processed_img_data)

    if winner:
        emit("winner", winner)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')