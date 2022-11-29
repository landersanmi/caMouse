import cv2
import numpy as np
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

#cap = cv2.VideoCapture('http://192.168.0.14:8080/video')
cap = cv2.VideoCapture(0)
window_name = 'Hand recognition'
ret, frame = cap.read()

while True:
    _, frame = cap.read()
    x , y, c = frame.shape

    # Flip the frame vertically
    #frame = cv2.flip(frame, 1)

    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(framergb)

    landmarks=[]
    landmarks_raw = []
    dots = np.empty((0,2), int)

    if result.multi_hand_landmarks:
        for handslms in result.multi_hand_landmarks:
            for i, lm in enumerate(handslms.landmark):
                lmx, lmy = int(lm.x * x), int(lm.y * y)
                cv2.circle(frame, (lmx, lmy), 3, (255,0,0), -1)
                dots = np.append(dots, [[lmx, lmy]] , axis=0)
                landmarks_raw.append([lm.x, lm.y, lm.z])
            
            dots_relocated = dots - dots.min(axis=0)
            for dot in dots_relocated: cv2.circle(frame, (dot[0], dot[1]), 3, (0,0,255), -1)
            rect = cv2.boundingRect(dots)
            x, y, w, h = rect
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)


    # Show the final output
    cv2.imshow(window_name, frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key & 0xFF == ord('l'):
        print(landmarks)
        print(landmarks_raw)

cap.release()
cv2.destroyAllWindows()

