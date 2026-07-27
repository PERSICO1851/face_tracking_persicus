#importing#####################################
import cv2
import mediapipe
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import GestureRecognizer
import numpy as np
import time
import random
import random
################################################

#setup
cap = cv2.VideoCapture(1) #nome fotocamera, nel mio caso uso la n1.
base_options = python.BaseOptions(model_asset_path='models/hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,running_mode=vision.RunningMode.VIDEO, num_hands=2)
hand_landmarker = vision.HandLandmarker.create_from_options(options)
gesture_base_options = python.BaseOptions(model_asset_path="models/gesture_recognizer.task")
gesture_options = vision.GestureRecognizerOptions(base_options=gesture_base_options,running_mode=vision.RunningMode.VIDEO)
gesture_recognizer = vision.GestureRecognizer.create_from_options(gesture_options)

timestamp = 0
 #timestamp in millisecondi
#detect function for switching between modes
def detect(gesture_results,mode,fist_triggered):
    if gesture_results.gestures:
        gesture = gesture_results.gestures[0][0].category_name
        if gesture == "Closed_Fist" and not fist_triggered:
            fist_triggered = True
            if mode < 3: #switch between modes
                mode += 1
            else:
                mode = 1
        elif gesture != "Closed_Fist":
            fist_triggered = False
    else:
        gesture = None
    return mode, gesture, fist_triggered
    

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
        cv2.circle(frame, (x, y), 3, (0, 0, 0), -2)

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
    cv2.fillConvexPoly(frame, np.array([thumb1, thumb2, index2, index1]), (0, 0, 255),) #fill the area between the lines with red color
#draw solid lines 
def draw_solid(frame, hand_landmarks1,hand_landmarks2):
    height, width, _ = frame.shape
    thumb_tip = landmark_to_pixel(hand_landmarks1[4], width, height)
    middle_tip = landmark_to_pixel(hand_landmarks1[8], width, height)
    ring_tip = landmark_to_pixel(hand_landmarks1[16], width, height)
    pinky_tip = landmark_to_pixel(hand_landmarks1[20], width, height)
    thumb_tip2 = landmark_to_pixel(hand_landmarks2[4], width, height)
    middle_tip2 = landmark_to_pixel(hand_landmarks2[8], width, height)
    ring_tip2 = landmark_to_pixel(hand_landmarks2[16], width, height)
    pinky_tip2 = landmark_to_pixel(hand_landmarks2[20], width, height)
    #creation of the base quadrilateral for the solid shape
    cv2.polylines(frame,np.array([[thumb_tip, middle_tip, ring_tip, pinky_tip]]),True,(0,0,255),2)
    cv2.polylines(frame,np.array([[thumb_tip2, middle_tip2, ring_tip2, pinky_tip2]]),True,(0,0,255),2) #polylines function draws lines betweeen a set of points created by np.array
    #connect points for creating the solid
    cv2.line(frame, thumb_tip, thumb_tip2, (0, 0, 255), 2)
    cv2.line(frame, middle_tip, middle_tip2, (0, 0, 255), 2)
    cv2.line(frame, ring_tip, ring_tip2, (0, 0, 255), 2)
    cv2.line(frame, pinky_tip, pinky_tip2, (0, 0, 255), 2)
    #
def draw_mask(frame, hand_landmarks1, hand_landmarks2):
    # Use thumb1, thumb2, index1, index2 to form a rectangle
    h, w, _ = frame.shape
    thumb1 = landmark_to_pixel(hand_landmarks1[4], w, h)
    thumb2 = landmark_to_pixel(hand_landmarks2[4], w, h)
    index1 = landmark_to_pixel(hand_landmarks1[8], w, h)
    index2 = landmark_to_pixel(hand_landmarks2[8], w, h)

    cv2.polylines(frame, np.array([[thumb1, thumb2, index2, index1]]), True, (0, 0, 0), 2)  # Draw the rectangle outline
    poly = np.array([thumb1, thumb2, index2, index1], dtype=np.int32) #points 

    # create single-channel mask and fill rectangle
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [poly], 255) #creat the fill mask

    # create a semi-transparent colored overlay inside the rectangle
    overlay = frame.copy()
    cv2.fillPoly(overlay, [poly], (0, 0, 255))
    alpha = 0.35 #livello trasparenza 
    blended = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    # create glitch effect and apply it only where mask is present
    glitch = create_glitch(frame)
    frame[mask == 255] = glitch[mask == 255]

    return

def create_glitch(frame):
    glitch = frame.copy()
    h, w = frame.shape[:2]

    # Creiamo alcune bande glitch casuali
    for i in range(10):
        y = random.randint(0, max(0, h - 1))
        height = random.randint(2, min(20, max(2, h // 10)))
        shift = random.randint(-50, 50)
        y2 = min(y + height, h)

        # copia la fascia per evitare view condivise
        stripe = frame[y:y2, :].copy()
        stripe_shifted = np.roll(stripe, shift, axis=1)
        glitch[y:y2, :] = stripe_shifted

    return glitch

    return glitch


fist_triggered = False 
mode = 1 #initial mode of the program.

while True:
    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #convert from BGR to RGB
    mediapipe_frame = mediapipe.Image(image_format=mediapipe.ImageFormat.SRGB, data=rgb_frame) #convert from numpy array to mediapipe image

    results = hand_landmarker.detect_for_video(mediapipe_frame,timestamp) #detect hands
    hand_landmarks = results.hand_landmarks
    gesture_results = gesture_recognizer.recognize_for_video(mediapipe_frame,timestamp) #detect gestures
    mode, gesture, fist_triggered = detect(gesture_results,mode,fist_triggered) #detect the gesture and switch
    gesture = gesture_results.gestures[0][0].category_name if gesture_results.gestures else None
    cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if hand_landmarks:
        for hand in hand_landmarks:
            draw_point(frame, hand) #draw points on camera
        if len(hand_landmarks) == 2: #if there are two hands
            #detect(hand_landmarks) #detect the gesture and switch
            match mode:
                case 1:
                    hand1,hand2 = hand_landmarks[0],hand_landmarks[1] #get the two hands
                    drawfinger_lines(frame,hand1,hand2)
                case 2:
                    hand1,hand2 = hand_landmarks[0],hand_landmarks[1] #get the two hands
                    draw_solid(frame,hand1,hand2)
                case 3:
                    hand1,hand2 = hand_landmarks[0],hand_landmarks[1] #get the two hands
                    draw_mask(frame, hand1, hand2)

                    




    timestamp += 33 #a quanti frame al secondo imposto il frame, 33 equivalentea a 30 fps
    cv2.imshow("Webcam", frame) #mostra i drawings sulla webcam
    #print(f"Frame read: {ret},{bool(results.hand_landmarks)}") #stampa True se la videocamera è attiva, False se non lo è #processa il frame con mediapipe
    if cv2.waitKey(1) & 0xFF == ord('q'): #stoppa se premi il tasto 'q'
        break

cap.release()
cv2.destroyAllWindows()