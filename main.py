import cv2
import mediapipe as mp
import numpy as np


mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    corners = []

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            h, w, _ = frame.shape

            thumb = hand_landmarks.landmark[4]

            index = hand_landmarks.landmark[8]

            thumb_point = (
                int(thumb.x * w),
                int(thumb.y * h)
            )

            index_point = (
                int(index.x * w),
                int(index.y * h)
            )

            corners.append((thumb_point, index_point))

            # Red Points
            cv2.circle(frame, thumb_point, 10git add ., (0, 0, 255), -1)
            cv2.circle(frame, index_point, 10, (0, 0, 255), -1)

    if len(corners) == 2:

        left_thumb, left_index = corners[0]
        right_thumb, right_index = corners[1]

        polygon = np.array([
            left_index,
            right_index,
            right_thumb,
            left_thumb
        ], dtype=np.int32)

        # Create mask
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)

        cv2.fillPoly(mask, [polygon], 255)

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        frame[mask == 255] = gray[mask == 255]

        cv2.polylines(
            frame,
            [polygon],
            True,
            (255, 255, 255),
            1
        )

    cv2.imshow("Gesture Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()