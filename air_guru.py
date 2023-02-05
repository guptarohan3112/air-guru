import mediapipe as mp
import cv2
from functions import performAction
from utils import classify_hand, finger_touching_right_ear, within_facialbounds, straight_hand

"""This file connects to the computers video system, receiving continuous input that is then analysed by utils.py and functions.py"""

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

frame = 0

cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    frame += 1
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)
      
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    for i, landmarks in enumerate([results.right_hand_landmarks, results.left_hand_landmarks]):
        if landmarks:
            mp_drawing.draw_landmarks(
                image,
                landmarks,
                mp_holistic.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            
            gesture = classify_hand(landmarks,i)
            
            fingerTouchingEar = finger_touching_right_ear(results.pose_landmarks, landmarks, 0.05)
            
            withInFace = within_facialbounds(results.pose_landmarks, landmarks)
            
            straightHand = straight_hand(landmarks, 0.01)
            
            # print(frame)
            if frame % 10 == 0:
                if gesture == "VOLUME_UP":
                    performAction(gesture, fingerTouchingEar, withInFace, straightHand)
                    frame = 0
                if gesture == "VOLUME_DOWN":
                    performAction(gesture, fingerTouchingEar, withInFace, straightHand)
            else:
                performAction(gesture, fingerTouchingEar, withInFace, straightHand)
            
         
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
    if cv2.getWindowProperty('MediaPipe Hands', cv2.WND_PROP_VISIBLE) < 1:
      break
cap.release()


