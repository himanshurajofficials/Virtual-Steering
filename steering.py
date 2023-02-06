import math
import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

import time

keyboard = Controller()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
font = cv2.FONT_HERSHEY_SIMPLEX
# 0 For webcam input:
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)

        results = hands.process(image)
        imageHeight, imageWidth, _ = image.shape

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.waitKey(1)
        co = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                for point in mp_hands.HandLandmark:
                    if str(point) == "HandLandmark.WRIST":
                        normalizedLandmark = hand_landmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                               normalizedLandmark.y,
                                                                                               imageWidth, imageHeight)

                        try:
                            co.append(list(pixelCoordinatesLandmark))
                        except:
                            continue

        # print(co)
        if len(co) == 0:
            cv2.putText(image, "Virtual Steering -By Himanshu Raj", (50, 50), font, 0.9, (51, 0, 104), 2, cv2.LINE_AA)
        if len(co) == 2:
            xm, ym = (co[0][0] + co[1][0]) / 2, (co[0][1] + co[1][1]) / 2

            radius = 150

            try:
                m = (co[1][1] - co[0][1]) / (co[1][0] - co[0][0])
            except:
                continue

            m11 = math.floor(math.degrees(math.atan(m)))
            cv2.circle(img=image, center=(int(xm), int(ym)), radius=radius, color=(195, 255, 62), thickness=22)

            if (co[1][0] > co[0][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65 and m11 <= 24) or (
                    co[0][0] > co[1][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65 and m11 <= 24):

                print("Turn right.")
                time.sleep(1)
                print(math.degrees(math.atan(m)))
                keyboard.release('s')
                keyboard.release('a')
                keyboard.press('d')

                cv2.putText(image, "Turn right", (50, 50), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)

            elif (co[1][0] > co[0][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65 and 24 < m11 < 89) or (
                    co[0][0] > co[1][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65 and 24 < m11 < 89):

                print("Turn right.")
                time.sleep(0.7)
                print(math.degrees(math.atan(m)))
                keyboard.release('s')
                keyboard.release('a')
                keyboard.press('d')

                cv2.putText(image, "Fast Turn right", (50, 50), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)

            elif (co[0][0] > co[1][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65 and m11 >= -24) or (
                    co[1][0] > co[0][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65 and m11 >= -24):
                print("Turn left.")
                time.sleep(1)
                keyboard.release('s')
                keyboard.release('d')
                keyboard.press('a')
                # print("hello world >20")
                print(math.degrees(math.atan(m)))

                cv2.putText(image, "Turn left", (50, 50), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)

            elif (co[0][0] > co[1][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65 and -90 < m11 < -24) or (
                    co[1][0] > co[0][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65 and -90 < m11 < -24):
                print("Turn left.")
                time.sleep(0.7)
                keyboard.release('s')
                keyboard.release('d')
                keyboard.press('a')
                # print("hello world <19")
                print(math.degrees(math.atan(m)))

                cv2.putText(image, "Fast Turn left", (50, 50), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)

            else:
                print("keeping straight")

                # time.sleep(0.01)
                print(math.degrees(math.atan(m)))
                keyboard.release('s')
                keyboard.release('a')
                keyboard.release('d')
                keyboard.press('w')

                cv2.putText(image, "keep straight and Accelerate", (50, 50), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)

        if len(co) == 1:
            print("keeping back")
            keyboard.release('a')
            keyboard.release('d')
            keyboard.release('w')
            keyboard.press('s')
            cv2.putText(image, "keeping back and Decelerate", (50, 50), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('MediaPipe Hands', image)

        # Flip the image horizontally for a selfie-view display.
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
cap.release()
