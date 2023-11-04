#import opencv
import cv2
#import the library mediapipe
import mediapipe as mp
import serial

#define capture openCV istance
cap = cv2.VideoCapture(0)

#set drawing and detection capabilities offered by mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Create serial object named arduino
arduino = serial.Serial('/dev/cu.usbmodem14201', 9600)  # Replace 'COM3' with the correct serial port

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        
        #change color codes of the frame
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #set flag
        image.flags.writeable = False

        #detect hands
        results = hands.process(image)

        #back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #render points and connections
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS) 
                
                # Check the position of the index finger tip
                index_finger_tip = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                
                # Check if the index finger is pointed (you can adjust this threshold)
                if index_finger_tip.y < hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y:
                    arduino.write(b'1')  # Send '1' to Arduino to turn on the LED
                else:
                    arduino.write(b'0')  # Send '0' to Arduino to turn off the LED

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

# Close the serial connection
arduino.close()

cap.release()
cv2.destroyAllWindows()

