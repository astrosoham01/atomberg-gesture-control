import cv2
import mediapipe as mp
import socket
import json
import time

# 🔌 Fan local IP
FAN_IP = "********"
PORT = 5600

# 📡 Send command to fan


def send_command(cmd):
    message = json.dumps(cmd).encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (FAN_IP, PORT))
    sock.close()


#  Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# 📷 Select correct camera index
cap = cv2.VideoCapture(0)   # change if needed

last_action = ""
last_time = time.time()

print("Gesture fan control started...")

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)

    totalFingers = 0

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            lmList = []

            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                lmList.append((int(lm.x*w), int(lm.y*h)))

            if lmList:
                fingers = []

                #  Thumb
                if lmList[4][0] < lmList[3][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Other 4 fingers
                tips = [8, 12, 16, 20]
                for tip in tips:
                    if lmList[tip][1] < lmList[tip-2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                totalFingers = fingers.count(1)

                print("Fingers:", totalFingers)

                cv2.putText(img, f'Fingers:{totalFingers}', (20, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

                # ⏱ avoid spamming commands
                if time.time()-last_time > 1.2:

                    if totalFingers == 0 and last_action != "off":
                        send_command({"power": False})
                        print("Fan OFF")
                        last_action = "off"

                    elif totalFingers == 1 and last_action != "1":
                        send_command({"speed": 1})
                        print("Speed 1")
                        last_action = "1"

                    elif totalFingers == 2 and last_action != "2":
                        send_command({"speed": 2})
                        print("Speed 2")
                        last_action = "2"

                    elif totalFingers == 3 and last_action != "3":
                        send_command({"speed": 3})
                        print("Speed 3")
                        last_action = "3"

                    elif totalFingers == 4 and last_action != "4":
                        send_command({"speed": 4})
                        print("Speed 4")
                        last_action = "4"

                    elif totalFingers == 5 and last_action != "5":
                        send_command({"speed": 5})
                        print("Speed 5")
                        last_action = "5"

                    last_time = time.time()

            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Atomberg Gesture Fan Control", img)

    if cv2.waitKey(1) == 27:
        break
