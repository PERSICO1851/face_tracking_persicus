#importing#####################################
import cv2
import mediapipe
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
################################################

#setup
cap = cv2.VideoCapture(0) #nome fotocamera, nel mio caso uso la n1.
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,running_mode=vision.RunningMode.VIDEO, num_hands=2)
hand_landmarker = vision.HandLandmarker.create_from_options(options)
timestamp = 0
 #timestamp in millisecondi

#functiont that converts mediapipe landmarks to pixel coordinates
def landmark_to_pixel(landmark, width, height):
    x = int(landmark.x * width)
    y = int(landmark.y * height)

    return (x, y)


#draw points on camera, comment if u dont want to see them
def draw_point(frame, hand_landmarks):
    height, width, _ = frame.shape
    for landmark in hand_landmarks:
        x,y = landmark_to_pixel(landmark, width, height) #convert from cartesian points to pixel coordinates 
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -2)

#draw finger lines 
def drawfinger_lines(frame, hand_landmarks1,hand_landmarks2):
    height, width, _ = frame.shape
    thumb1 = landmark_to_pixel(hand_landmarks1[4], width, height)
    thumb2 = landmark_to_pixel(hand_landmarks2[4], width, height)
    index1 = landmark_to_pixel(hand_landmarks1[8], width, height)
    index2 = landmark_to_pixel(hand_landmarks2[8], width, height)
    cv2.line(frame,thumb1,thumb2,(0,0,255),2)
    cv2.line(frame,index1,index2,(0,0,255),2)
    cv2.line(frame, thumb1,index1,(0,0,255),2)
    cv2.line(frame, thumb2,index2,(0,0,255),2)




while True:
    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #convert from BGR to RGB
    mediapipe_frame = mediapipe.Image(image_format=mediapipe.ImageFormat.SRGB, data=rgb_frame) #convert from numpy array to mediapipe image

    results = hand_landmarker.detect_for_video(mediapipe_frame,timestamp) #detect hands
    hand_landmarks = results.hand_landmarks
    if hand_landmarks: #verifies if there are hands
        for hand in hand_landmarks:
            draw_point(frame, hand) #draw points on camera
        if len(hand_landmarks) == 2: #if there are two hands
            hand1,hand2 = hand_landmarks[0],hand_landmarks[1] #get the two hands
            drawfinger_lines(frame,hand1,hand2)





    timestamp += 33
    cv2.imshow("Webcam", frame) #mostra i drawings sulla webcam
    print(f"Frame read: {ret},{bool(results.hand_landmarks)}") #stampa True se la videocamera è attiva, False se non lo è #processa il frame con mediapipe
    if cv2.waitKey(1) & 0xFF == ord('q'): #stoppa se premi il tasto 'q'
        break

cap.release()
cv2.destroyAllWindows()