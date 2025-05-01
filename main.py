# Importing libraries

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import angle_and_distance as angAndDist
import time
last_action_time = 0
cooldown = 1  # Minimum delay (in seconds) between two consecutive gestures/actions to prevent rapid repeat triggers
c=0
message_text = ""
message_time = 0
message_display_duration = 1  # Message display duration (in seconds)

# initialization of mediapipe for hand recognition

mphands=mp.solutions.hands
hands=mphands.Hands(static_image_mode=False,model_complexity=1,min_tracking_confidence=0.7,min_detection_confidence=0.7,max_num_hands=1)


# Mouse functions

# Gesture detection functions
def move_mouse(index_finger_tip):
    if index_finger_tip:
        # Convert normalized values to actual webcam coordinates
        x = int(index_finger_tip.x * bw)
        y = int(index_finger_tip.y * bh)

        # Only map if the finger is inside the rectangle
        # if 50 <= x <= bw - 50 and 50 <= y <= bh - 50:
            # Map (x, y) from box region to full screen
        mapped_x = np.interp(x, [100, bw - 100], [0, scrW])
        mapped_y = np.interp(y, [100, bh - 100], [0, scrH])

        pyautogui.moveTo(mapped_x, mapped_y)

# Checking if the gesture is Left Click
def is_left_click(lm_list,thumb_index_dist):
    return (angAndDist.getAngle( lm_list[5 ], lm_list[6 ], lm_list[8 ] ) < 50 and angAndDist.getAngle( lm_list[9 ], lm_list[10 ], lm_list[12 ] ) > 50 and thumb_index_dist > 50)

# Checking if the gesture is Right Click
def is_right_click(lm_list,thumb_index_dist):
    return (angAndDist.getAngle( lm_list[9 ], lm_list[10 ], lm_list[12 ] ) < 50 and angAndDist.getAngle( lm_list[5 ], lm_list[6 ], lm_list[8 ] ) > 90 and thumb_index_dist > 50)

# Checking if the gesture is Double Click

def is_double_click(lm_list,thumb_index_dist):
    return (angAndDist.getAngle( lm_list[5 ], lm_list[6 ], lm_list[8 ] ) < 50 and angAndDist.getAngle( lm_list[9 ], lm_list[10 ], lm_list[12 ] ) < 50 and thumb_index_dist > 50)

# Checking if the gesture is Screenshot

def is_screenshot(lm_list,thumb_index_dist):
    return (angAndDist.getAngle( lm_list[5 ], lm_list[6 ], lm_list[8 ] ) < 50 and angAndDist.getAngle( lm_list[9 ], lm_list[10 ], lm_list[12 ] ) < 50 and thumb_index_dist < 50)

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_lm=processed.multi_hand_landmarks[0]
        return hand_lm.landmark[mphands.HandLandmark.INDEX_FINGER_TIP]

    return None

# Detecting hand gestures
def detect_gestures(frame,lm_list,processed):
    global last_action_time,c,message_time,message_text

    current_time = time.time ( )
    if len(lm_list)>=21:
        index_finger_tip=find_finger_tip(processed)
        thumb_index_dist=angAndDist.getDist( [ lm_list[4 ], lm_list[5 ] ] )
        # moving the cursor
        if thumb_index_dist<50 and angAndDist.getAngle( lm_list[5 ], lm_list[6 ], lm_list[8 ] )>90:
            if 100 <= int(index_finger_tip.x*bw) <= bw - 100 and 100 <= int(index_finger_tip.y *bh)<= bh - 100 :
                move_mouse ( index_finger_tip )
            else :
                cv2.putText ( frame, "No movement! Put index finger in the box.", (110, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2 )
        elif current_time - last_action_time > cooldown :
            # Left click
            if is_left_click(lm_list,thumb_index_dist):
                pyautogui.click()
                message_text="Left Click"
                message_time = current_time
                last_action_time = current_time

            # Right click
            elif is_right_click(lm_list,thumb_index_dist):
                pyautogui.rightClick()
                message_text="Right Click"
                message_time = current_time
                last_action_time = current_time

            # Double click
            elif is_double_click(lm_list,thumb_index_dist):
                pyautogui.doubleClick()
                message_text="Double Click"
                message_time = current_time
                last_action_time = current_time

            # Screenshot
            elif is_screenshot(lm_list,thumb_index_dist):
                img=pyautogui.screenshot()
                img.save ( fr"C:\Users\srivasthav\OneDrive\Desktop\ai_img{c}.png" )
                c+=1
                message_text="ScreenShot Captured"
                message_time = current_time
                last_action_time = current_time
                print(c)
        # Show message if within display duration
        if message_text and (time.time ( ) - message_time < message_display_duration) :
            cv2.putText ( frame, message_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3 )




# Main
scrW,scrH=pyautogui.size()
bw = 640  # Width of the OpenCV capture window (camera frame width)
bh = 480  # Height of the OpenCV capture window (camera frame height)

cap=cv2.VideoCapture(0)
cap.set(3,bw)
cap.set(4,bh)
draw=mp.solutions.drawing_utils
try:
    cv2.namedWindow ( "Frame", cv2.WINDOW_NORMAL )
    cv2.resizeWindow ( "Frame", bw, bh )
    while cap.isOpened() and cv2.getWindowProperty('Frame', cv2.WND_PROP_VISIBLE) >= 1 :
        ret,frame=cap.read()

        if not ret:
            break
        cv2.rectangle(frame,(100,100),(bw-100,bh-100),(250,250,2),2)
        frame=cv2.flip(frame,1)
        cv2.putText ( frame, "AI Cursor", (250, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, ( 85,40,0), 3 )
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        processed=hands.process(frameRGB)
        lm_list=[]

        if processed.multi_hand_landmarks:
            hand_lm=processed.multi_hand_landmarks[0]
            draw.draw_landmarks(frame,hand_lm,mphands.HAND_CONNECTIONS)
            for lm in hand_lm.landmark:
                lm_list.append((lm.x,lm.y))
        detect_gestures(frame,lm_list,processed)

        cv2.imshow('Frame',frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()


    