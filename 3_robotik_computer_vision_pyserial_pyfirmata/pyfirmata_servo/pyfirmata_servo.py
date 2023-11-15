from pyfirmata import Arduino, SERVO
import time

# Enter your serial port path
port = '/dev/cu.usbmodem21401'  # Modify this with your path

# Create the board object
board = Arduino(port)

# Set up the servo pin
servo_pin = 13
board.digital[servo_pin].mode = SERVO

# Function to control the servo
def move_servo(angle):
    board.digital[servo_pin].write(angle)

try:
    while True:
        # User input for the servo angle
        angle = int(input("Enter the servo angle (0 to 180, -1 to exit): "))
        
        if angle == -1:
            break  # Exit the loop
        
        # Ensure the angle is between 0 and 180
        angle = max(0, min(angle, 180))

        # Move the servo to the specified angle
        move_servo(angle)
        
        # Add a delay to allow the servo to reach the desired position
        time.sleep(0.5)

except KeyboardInterrupt:
    pass
finally:
    # Release the connection to the Arduino board
    board.exit()