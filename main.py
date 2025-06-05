from camera_utils import initialize_camera
from hand_detection import get_hands, draw_hand_landmarks
from steering_wheel import draw_steering_wheel, calculate_steering_angle
from controls import KeyboardController
import cv2
import numpy as np

STEERING_WHEEL_RADIUS = 80
STEERING_THRESHOLD = 15
MAX_STEERING_ANGLE = 20


def main():
    cap, cam_width, cam_height = initialize_camera()
    steering_wheel_center = (cam_width // 2, int(cam_height * 0.75))
    wheel_img_size = int(2 * STEERING_WHEEL_RADIUS * 1.5)
    wheel_base_img = np.zeros((wheel_img_size, wheel_img_size, 4), dtype=np.uint8)
    hands = get_hands()
    keyboard = KeyboardController()
    current_steering_angle = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera. End of stream?")
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
            keyboard.press("w")
            hand_landmarks_list = results.multi_hand_landmarks
            hand1_x = hand_landmarks_list[0].landmark[0].x
            hand2_x = hand_landmarks_list[1].landmark[0].x
            if hand1_x < hand2_x:
                left_hand_landmarks = hand_landmarks_list[0]
                right_hand_landmarks = hand_landmarks_list[1]
            else:
                left_hand_landmarks = hand_landmarks_list[1]
                right_hand_landmarks = hand_landmarks_list[0]
            for hand_landmarks in hand_landmarks_list:
                draw_hand_landmarks(frame, hand_landmarks)
            lx = int(left_hand_landmarks.landmark[5].x * frame.shape[1])
            ly = int(left_hand_landmarks.landmark[5].y * frame.shape[0])
            rx = int(right_hand_landmarks.landmark[5].x * frame.shape[1])
            ry = int(right_hand_landmarks.landmark[5].y * frame.shape[0])
            cv2.circle(frame, (lx, ly), 8, (0, 255, 0), -1)
            cv2.circle(frame, (rx, ry), 8, (0, 0, 255), -1)
            cv2.line(frame, (lx, ly), (rx, ry), (255, 255, 0), 2)
            angle = calculate_steering_angle(lx, ly, rx, ry)
            current_steering_angle = max(min(angle, MAX_STEERING_ANGLE), -MAX_STEERING_ANGLE)
            if current_steering_angle > STEERING_THRESHOLD:
                keyboard.press("a")
                cv2.putText(frame, "Turning A (key A)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
            elif current_steering_angle < -STEERING_THRESHOLD:
                keyboard.press("d")
                cv2.putText(frame, "Turning D (key D)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
            else:
                keyboard.release("a")
                keyboard.release("d")
                cv2.putText(frame, "Straight (keys released)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            keyboard.release("w")
            keyboard.release("a")
            keyboard.release("d")
            current_steering_angle = 0
            cv2.putText(frame, "Keep both hands visible!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

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
        cv2.imshow("Driving Simulator (Gestures)", frame)
        key = cv2.waitKey(20) & 0xFF
        if key == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Simulator closed.")

if __name__ == "__main__":
    main()
