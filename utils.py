import mediapipe as mp
import numpy as np

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

gestureMap = {
    (True, False, False, False): "MUTE",
    (False, False, False, False): "LOW_BRIGHTNESS",
    (True, True, True, True): "HIGH_BRIGHTNESS",
}

unitVector = {
    "x_axis": np.asarray([1, 0]),
    "y_axis": np.asarray([0, 1])
}

# only pass in y values
def finger_is_up(mcp, pip, dip, tip):
  # note, higher up in physical space is lower in this space
  return tip < dip < pip < mcp


def finger_vector(tip_X, tip_Y, mcp_X, mcp_Y):
    # Find vector difference
    x_diff = tip_X - mcp_X
    y_diff = tip_Y - mcp_Y
    return (x_diff, y_diff)


def finger_angle(finger_vec: set):
    # Find unit vector
    finger_unit_vector = np.asarray(finger_vec) / np.linalg.norm(np.asarray(finger_vec))
    
    # Find angle between x-axis and finger vector
    return np.arccos(np.clip(np.dot(finger_unit_vector, unitVector["x_axis"]), -1.0, 1.0))


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

  index_finger_vector = finger_vector(
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].x,
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].x,
      hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].y 
  )
  index_angle = finger_angle(index_finger_vector)*180/np.pi

  middle_finger_vector = finger_vector(
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].x,
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].x,
      hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y 
  )
  middle_angle = finger_angle(middle_finger_vector)*180/np.pi

  ring_finger_vector = finger_vector(
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].x,
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].x,
      hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_MCP].y 
  )
  ring_angle = finger_angle(ring_finger_vector)*180/np.pi

  pinky_finger_vector = finger_vector(
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_TIP].x,
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_TIP].y,
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_MCP].x,
      hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_MCP].y
  )
  pinky_angle = finger_angle(pinky_finger_vector)*180/np.pi
  
  fingers = (index_finger_is_up, middle_finger_is_up, ring_finger_is_up, pinky_is_up)
  fingers_vector = (index_finger_vector, middle_finger_vector, ring_finger_vector, pinky_finger_vector)
  fingers_angles = (index_angle, middle_angle, ring_angle, pinky_angle)
  print(fingers_vector)
  print(fingers_angles)

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
