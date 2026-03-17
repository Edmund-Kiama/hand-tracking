import handTrackingModule as htm
import cv2
import time
import subprocess
import numpy as np

cap = cv2.VideoCapture(0)

detector = htm.HandDetector()
p_time = 0
vol = 50

while True:
    success, image = cap.read()

    detector.find_hands(image)
    lm_list = detector.find_position(image)

    if len(lm_list) > 0 :
        thumb = lm_list[4]
        finger = lm_list[8]

        x1, y1 = thumb[1], thumb[2]
        x2, y2 = finger[1], finger[2] 

        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
        
        # Compute distance
        distance = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
        
        # Map distance to volume (50-250 px -> 0-100%)
        vol_range = 200
        min_dist = 50
        vol = np.clip((distance - min_dist) / vol_range * 100, 0, 100).astype(int)
        
        # Set volume
        subprocess.call(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{vol}%'])
        
        # Visual volume bar
        bar_width = 400
        bar_height = 20
        x_bar, y_bar = 50, 450
        cv2.rectangle(image, (x_bar, y_bar), (x_bar + bar_width, y_bar + bar_height), (0, 0, 0), 3)
        cv2.rectangle(image, (x_bar, y_bar), (x_bar + int(vol * bar_width / 100), y_bar + bar_height), (0, 255, 0), cv2.FILLED)

    # FPS
    c_time = time.time()
    fps = 1 / (c_time - p_time) if p_time != 0 else 0
    p_time = c_time
    cv2.putText(image, f'FPS: {int(fps)} VOL: {vol}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    
    cv2.imshow("image", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
