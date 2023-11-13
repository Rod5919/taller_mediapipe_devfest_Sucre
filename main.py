import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# STEP 2: Create an GestureRecognizer object.
base_options = python.BaseOptions(model_asset_path='models/gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

# Create a VideoCapture object to get images from the camera
cap = cv2.VideoCapture(0)

def rock_paper_scissors(gesture1, gesture2):
    
    if gesture1 == "None" or gesture2 == "None":
        return
    
    gestures = {
        "Open_Palm": "Paper",
        "Victory": "Scissors",
        "Closed_Fist": "Rock"
    }
    
    gesture1 = gestures[gesture1]
    gesture2 = gestures[gesture2]
    
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

# Loop to continuously get frames from the camera and show them
while True:
    left_gesture = None
    right_gesture = None
    
    # Read a frame from the camera
    ret, frame = cap.read()

    # If the frame was not successfully read, break out of the loop
    if not ret:
        break

    # Draw dividing line
    cv2.line(frame, (frame.shape[1]//2, 0), (frame.shape[1]//2, frame.shape[0]), (0, 0, 255), 2)

    # Put Title in each half
    cv2.putText(frame, "Left", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, "Right", (frame.shape[1]//2 + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Crop image into two halves
    left, right = frame[:, :frame.shape[1]//2], frame[:, frame.shape[1]//2:]

    # Left and right resize
    left = cv2.resize(left, (256, 256))
    right = cv2.resize(right, (256, 256))

    # Show the frames 
    cv2.imshow("Camera", frame)
    cv2.imshow("Left", left)
    cv2.imshow("Right", right)

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
    
    # Print the gestures
    print("Left: ", left_gesture)
    print("Right: ", right_gesture, end='\n\n')

    # Print the winner
    if left_gesture and right_gesture:
        if winner := rock_paper_scissors(left_gesture, right_gesture):
            print("--------------------")
            print("Winner: ")
            print(winner)
            print("--------------------", end='\n\n')

    # Wait for a key press and check if the "q" key was pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()
