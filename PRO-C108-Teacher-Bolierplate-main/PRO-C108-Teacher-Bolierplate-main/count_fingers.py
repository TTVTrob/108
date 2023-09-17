import cv2
import mediapipe as mp
tipID=[4,8,12,16,20]
cap = cv2.VideoCapture(0)  
mphands=mp.solutions.hands
mpdrawing=mp.solutions.drawing_utils
hands=mphands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5)
def drawlandmark(image,hand_landmarks):
    if hand_landmarks:
        for landmarks in hand_landmarks:
            mpdrawing.draw_landmarks(image,landmarks,mphands.HAND_CONNECTIONS)
def countFingers(image,hand_landmarks,handno=0):
    if hand_landmarks:
        landmarks=hand_landmarks[handno].landmarks
        print(landmarks)
        fingers=[]
        for lm_index in tipID:
            fingertipy=landmarks[lm_index].y
            fingerbottomy=landmarks[lm_index-2].y
            if lm_index!=4:
                if fingertipy<fingerbottomy:
                    fingers.append(1)
                    print("finger with ID", lm_index," is open")
                if fingertipy>fingerbottomy:
                    fingers.append(0)
                    print("finger with ID", lm_index," is closed")
        print(fingers)
        totalfingers=fingers.count(1)
        text=f'fingers:{totalfingers}'
        cv2.putText(image,text,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)

while True:
    success, image = cap.read()
    image=cv2.flip(image,1)
    result=hands.process(image)
    hand_landmarks=result.multi_hand_landmarks
    drawlandmark(image,hand_landmarks)
    countFingers(image,hand_landmarks)
    cv2.imshow("Media Controller", image)

    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()

