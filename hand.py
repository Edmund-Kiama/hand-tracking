import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) #targets webcam

# initialize mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils


while True:
    success, frame = cap.read() # reads image

    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert bgr to rgb
    results = hands.process(frame_RGB) #process hands
    #print(results.multi_hand_landmarks) #print on landmark found
    
    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_lms,mp_hands.HAND_CONNECTIONS) # draws land marks
            

    

    cv2.imshow("image", frame) #displays the image
    cv2.waitKey(1)