import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def get_hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2
):
    """
    Initializes and returns a MediaPipe Hands object for hand detection.

    Args:
        min_detection_confidence (float): Minimum confidence value ([0.0, 1.0]) for hand detection to be considered successful.
        min_tracking_confidence (float): Minimum confidence value ([0.0, 1.0]) for the hand landmarks to be considered tracked successfully.
        max_num_hands (int): Maximum number of hands to detect.

    Returns:
        mp.solutions.hands.Hands: Configured MediaPipe Hands object.
    """
    return mp_hands.Hands(
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
        max_num_hands=max_num_hands,
    )


def draw_hand_landmarks(frame, hand_landmarks):
    """
    Draws hand landmarks and connections on the given frame.

    Args:
        frame (np.ndarray): The image frame to draw on.
        hand_landmarks: The hand landmarks detected by MediaPipe.
    """
    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
