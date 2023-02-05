import mediapipe as mp
import cv2
from functions import performAction
from utils import classify_hand, finger_touching_ear

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
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
    
    for landmarks in [results.right_hand_landmarks, results.left_hand_landmarks]:
        if landmarks:
            mp_drawing.draw_landmarks(
                image,
                landmarks,
                mp_holistic.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            
            gesture = classify_hand(landmarks)
            
            fingerTouchingEar = finger_touching_ear(
                landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].x,
                results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR].x, 0.1)
            
            performAction(gesture, fingerTouchingEar)
            
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
    if cv2.getWindowProperty('MediaPipe Hands', cv2.WND_PROP_VISIBLE) < 1:
      break
cap.release()


