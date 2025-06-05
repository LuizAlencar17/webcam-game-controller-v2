from camera_utils import initialize_camera
from hand_detection import get_hands, draw_hand_landmarks
from steering_wheel import draw_steering_wheel, calculate_steering_angle
from controls import KeyboardController
import cv2
import numpy as np

# Constants for steering wheel and control thresholds
STEERING_WHEEL_RADIUS = 80  # Radius of the virtual steering wheel
STEERING_THRESHOLD = 15     # Minimum angle to trigger left/right turn
MAX_STEERING_ANGLE = 20     # Maximum steering angle allowed


def main():
    """
    Main function to run the webcam-based game controller.
    Initializes the camera, hand detection, and keyboard controller.
    Continuously reads frames from the camera, detects hands, calculates steering angle,
    simulates keyboard input for driving, and overlays a virtual steering wheel on the video feed.
    """
    # Initialize camera and get its dimensions
    cap, cam_width, cam_height = initialize_camera()
    # Set the center position for the virtual steering wheel overlay
    steering_wheel_center = (cam_width // 2, int(cam_height * 0.75))
    # Create a blank image for the steering wheel
    wheel_img_size = int(2 * STEERING_WHEEL_RADIUS * 1.5)
    wheel_base_img = np.zeros((wheel_img_size, wheel_img_size, 4), dtype=np.uint8)
    # Initialize hand detection and keyboard controller
    hands = get_hands()
    keyboard = KeyboardController()
    current_steering_angle = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera. End of stream?")
            break
        # Flip the frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)
        # Convert frame to RGB for hand detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # If two hands are detected, process steering logic
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
            keyboard.press("w")  # Simulate pressing 'w' to move forward
            hand_landmarks_list = results.multi_hand_landmarks
            # Determine which hand is left/right based on x-coordinates
            hand1_x = hand_landmarks_list[0].landmark[0].x
            hand2_x = hand_landmarks_list[1].landmark[0].x
            if hand1_x < hand2_x:
                left_hand_landmarks = hand_landmarks_list[0]
                right_hand_landmarks = hand_landmarks_list[1]
            else:
                left_hand_landmarks = hand_landmarks_list[1]
                right_hand_landmarks = hand_landmarks_list[0]
            # Draw landmarks for both hands
            for hand_landmarks in hand_landmarks_list:
                draw_hand_landmarks(frame, hand_landmarks)
            # Get coordinates for steering calculation
            lx = int(left_hand_landmarks.landmark[5].x * frame.shape[1])
            ly = int(left_hand_landmarks.landmark[5].y * frame.shape[0])
            rx = int(right_hand_landmarks.landmark[5].x * frame.shape[1])
            ry = int(right_hand_landmarks.landmark[5].y * frame.shape[0])
            # Draw circles and line between hands
            cv2.circle(frame, (lx, ly), 8, (0, 255, 0), -1)
            cv2.circle(frame, (rx, ry), 8, (0, 0, 255), -1)
            cv2.line(frame, (lx, ly), (rx, ry), (255, 255, 0), 2)
            # Calculate steering angle based on hand positions
            angle = calculate_steering_angle(lx, ly, rx, ry)
            current_steering_angle = max(
                min(angle, MAX_STEERING_ANGLE), -MAX_STEERING_ANGLE
            )
            # Simulate keyboard input based on steering angle
            if current_steering_angle > STEERING_THRESHOLD:
                keyboard.press("a")  # Turn left
                cv2.putText(
                    frame,
                    "Turning A (key A)",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
            elif current_steering_angle < -STEERING_THRESHOLD:
                keyboard.press("d")  # Turn right
                cv2.putText(
                    frame,
                    "Turning D (key D)",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
            else:
                keyboard.release("a")  # Go straight
                keyboard.release("d")
                cv2.putText(
                    frame,
                    "Straight (keys released)",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )
        else:
            # If not both hands are visible, release all keys and show warning
            keyboard.release("w")
            keyboard.release("a")
            keyboard.release("d")
            current_steering_angle = 0
            cv2.putText(
                frame,
                "Keep both hands visible!",
                (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

        # Draw and overlay the virtual steering wheel on the frame
        rotated_wheel_image = draw_steering_wheel(
            wheel_base_img,
            wheel_base_img.shape[1] // 2,
            wheel_base_img.shape[0] // 2,
            STEERING_WHEEL_RADIUS,
            current_steering_angle,
        )
        x_offset = steering_wheel_center[0] - rotated_wheel_image.shape[1] // 2
        y_offset = steering_wheel_center[1] - rotated_wheel_image.shape[0] // 2
        x_offset = max(0, x_offset)
        y_offset = max(0, y_offset)
        y1, y2 = y_offset, y_offset + rotated_wheel_image.shape[0]
        x1, x2 = x_offset, x_offset + rotated_wheel_image.shape[1]
        y2 = min(y2, frame.shape[0])
        x2 = min(x2, frame.shape[1])
        rotated_wheel_image_cropped = rotated_wheel_image[0 : (y2 - y1), 0 : (x2 - x1)]
        alpha_s = rotated_wheel_image_cropped[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            frame[y1:y2, x1:x2, c] = (
                alpha_s * rotated_wheel_image_cropped[:, :, c]
                + alpha_l * frame[y1:y2, x1:x2, c]
            )
        # Show the frame with overlays
        cv2.imshow("Driving Simulator (Gestures)", frame)
        key = cv2.waitKey(20) & 0xFF
        if key == ord("q"):
            break
    # Release resources and close windows
    cap.release()
    cv2.destroyAllWindows()
    print("Simulator closed.")


if __name__ == "__main__":
    main()
