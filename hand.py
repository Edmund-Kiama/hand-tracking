import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) #targets webcam

# initialize mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils

prev_time = 0
current_time = 0


while True:
    success, frame = cap.read() # reads image

    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert bgr to rgb
    results = hands.process(frame_RGB) #process hands
    #print(results.multi_hand_landmarks) #print on landmark found
    
    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_lms,mp_hands.HAND_CONNECTIONS) # draws land marks
            

    #frame rate
    current_time = time.time()
    fps = 1/ (current_time - prev_time)
    prev_time = current_time

    #display
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2) 
    cv2.imshow("image", frame) 
    
    cv2.waitKey(1)