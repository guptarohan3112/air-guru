import mediapipe as mp

# mp_hands = mp.solutions.hands
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


# only pass in y values
def finger_is_up(mcp, pip, dip, tip):
  # note, higher up in physical space is lower in this space
  return tip < dip < pip < mcp


def classify_hand(hand_landmarks):

  translation = lambda fingerIsUp: "UP" if fingerIsUp else "DOWN"
  
  index_finger_is_up = translation(finger_is_up(
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_PIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_DIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y
  ))
  middle_finger_is_up = translation(finger_is_up(
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_DIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y
  ))
  ring_finger_is_up = translation(finger_is_up(
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_PIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_DIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].y
  ))
  pinky_is_up = translation(finger_is_up(
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_MCP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_PIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_DIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_TIP].y
  ))
  
  print(index_finger_is_up, middle_finger_is_up, ring_finger_is_up, pinky_is_up)