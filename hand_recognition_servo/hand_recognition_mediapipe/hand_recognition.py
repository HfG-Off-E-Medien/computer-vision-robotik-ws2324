import cv2
import mediapipe as mp
import serial  # import serial library

# Define capture OpenCV instance
cap = cv2.VideoCapture(0)

# Set drawing and detection capabilities offered by mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Define mapping function
def map_value(value, from_low, from_high, to_low, to_high):
    return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low

# Initialize serial communication with Arduino
arduino = serial.Serial('/dev/cu.usbmodem14201', 9600)  # Replace 'COM3' with the correct serial port

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()

        # Change color codes of the frame
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Set flag
        image.flags.writeable = False

        # Detect hands
        results = hands.process(image)

        # Back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #prints results
        #print(results.multi_hand_landmarks)

        # Render points and connections
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

                # Calculate the distance between the first landmark middle finger and the wrist
                #distance = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.WRIST].y - results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.PINKY_TIP].y
                xpos = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.WRIST].x

                # Map xpos from [0, 1] to [0, 180] for Arduino control
                posx = map_value(xpos, 0, 1, 0, 180)
                posx = int(posx)  # Convert to integer for Arduino
                strs = str(posx)

                # Send the data to Arduino
                arduino.write(strs.encode())

                image = cv2.putText(image, strs, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

# Close the serial connection with Arduino
arduino.close()

cap.release()
cv2.destroyAllWindows()
