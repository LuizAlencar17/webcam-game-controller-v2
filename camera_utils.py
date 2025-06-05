import cv2


def initialize_camera(width=640, height=480, camera_id=0):
    """
    Initializes the camera for video capture.

    Args:
        width (int): Desired width of the camera frame. Default is 640.
        height (int): Desired height of the camera frame. Default is 480.
        camera_id (int): ID of the camera to use. Default is 0.

    Returns:
        tuple: (cap, cam_width, cam_height) where cap is the VideoCapture object,
               cam_width and cam_height are the actual width and height of the camera frame.

    Raises:
        RuntimeError: If the camera cannot be opened.
    """
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError("Error: Could not open the camera.")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return cap, cam_width, cam_height
