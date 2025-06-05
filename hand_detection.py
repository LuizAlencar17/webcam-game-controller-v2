import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def get_hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2):
    return mp_hands.Hands(
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
        max_num_hands=max_num_hands
    )

def draw_hand_landmarks(frame, hand_landmarks):
    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
