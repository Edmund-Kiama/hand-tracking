import cv2
import mediapipe as mp
import time


class HandDetector():
    def __init__(self, mode=False, max_hands=2, detection_conf=0.5, track_conf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_conf = int(detection_conf)
        self.track_conf = int(track_conf)

        # initialize mp
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.detection_conf, self.track_conf)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self,frame,draw=True):
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert bgr to rgb
        self.results = self.hands.process(frame_RGB) #process hands
        #print(results.multi_hand_landmarks) #print on landmark found
        
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, hand_lms,self.mp_hands.HAND_CONNECTIONS) # draws land marks

        return frame
    
    def find_position(self, frame, hand_no=0, draw=True):    
        lm_list = []    

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            
            for index, lm in enumerate(my_hand.landmark):
                height, width, channels = frame.shape # from frame
                cx, cy = int(lm.x*width), int(lm.y*height)  # landmark position in frame
                
                lm_list.append([index, cx, cy])

                if draw:
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            
        return lm_list

  

    #frame rate
    # current_time = time.time()
    # fps = 1/ (current_time - prev_time)
    # prev_time = current_time

    # #display
    # cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2) 
    # cv2.imshow("image", frame) 

    # cv2.waitKey(1)

def main():

    prev_time = 0
    current_time = 0
    cap = cv2.VideoCapture(0) #targets webcam
    detector=HandDetector()

    while True:
        success, frame = cap.read() # reads image
        frame = detector.find_hands(frame)
        lm_list = detector.find_position(frame)
        if len(lm_list) != 0:
            print(lm_list[4])

         #frame rate
        current_time = time.time()
        fps = 1/ (current_time - prev_time )
        prev_time = current_time

        #display
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2) 
        cv2.imshow("image", frame) 

        cv2.waitKey(1)





if __name__ == "__main__":
    main()