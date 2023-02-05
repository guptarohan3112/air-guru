import mediapipe as mp

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

gestureMap = {
    (True, False, False, False): "MUTE",
    (False, False, False, False): "LOW_BRIGHTNESS",
    (True, True, True, True): "HIGH_BRIGHTNESS",
    
}

# compares the finger placement with where it is over face. If within appropriate area, return true
def within_facialbounds(pose_landmarks, hand_landmarks):
    lower_bound = pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_INNER].y
    upper_bound = pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].y
    left_bound = pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EYE_OUTER].x
    right_bound = pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EYE_OUTER].x
    
    finger_tipx = hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].x
    finger_tipy = hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y
    
    return left_bound < finger_tipx < right_bound and lower_bound < finger_tipy < upper_bound


# only pass in y values
def finger_is_up(mcp, pip, dip, tip):
  # note, higher up in physical space is lower in this space
  return tip < dip < pip < mcp

# only pass in right hand index finger x values and right ear position 
def finger_touching_ear(pose_landmarks, hand_landmarks, threshold):
    right_tip = hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP]
    right_ear = pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_EAR]
    return abs(right_tip.x - right_ear.x) < threshold and abs(right_tip.y - right_ear.y) < threshold

def classify_hand(hand_landmarks):

  translation = lambda fingerIsUp: "UP" if fingerIsUp else "DOWN"
  
  index_finger_is_up = finger_is_up(
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y
  )
  middle_finger_is_up = finger_is_up(
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y
  )
  ring_finger_is_up = finger_is_up(
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].y
  )
  pinky_is_up = finger_is_up(
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_MCP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_PIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_DIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_TIP].y
  )
  
  fingers = (index_finger_is_up, middle_finger_is_up, ring_finger_is_up, pinky_is_up)
  if fingers in gestureMap:
      gesture = gestureMap[fingers]
  else:
      gesture = "UNDEFINED"
  
  print(translation(index_finger_is_up), 
        translation(middle_finger_is_up), 
        translation(ring_finger_is_up), 
        translation(pinky_is_up),
        gesture)
  
  return gesture
