import cv2
import mediapipe as mp
import time


class HandDetector():
    def __init__(self, mode=False, max_hands=2, detection_conf=0.5, track_conf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_conf = detection_conf
        self.track_conf = track_conf

        # initialize mp
        self.mp_hands = mp.solutions.hands
        # self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.detection_conf, self.track_conf)
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=int(self.max_hands), # Must be an integer
            min_detection_confidence=float(self.detection_conf),
            min_tracking_confidence=float(self.track_conf)
        )
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


