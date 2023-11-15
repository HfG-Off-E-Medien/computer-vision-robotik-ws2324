from pyfirmata import Arduino, OUTPUT
import time

# Enter your serial port path
port = '/dev/cu.usbmodem21401'  # Modify this with your path

# Create the board object
board = Arduino(port)

# Set up the LED pin
led_pin = 13  # Assuming the LED is connected to digital pin 13
board.digital[led_pin].mode = OUTPUT

# Function to control the LED
def control_led(state):
    board.digital[led_pin].write(state)

try:
    while True:
        # User input for LED control
        state = int(input("Enter LED state (1 for ON, 0 for OFF, -1 to exit): "))
        
        if state == -1:
            break  # Exit the loop
        
        # Ensure the state is either 0 or 1
        state = 1 if state == 1 else 0

        # Control the LED based on user input
        control_led(state)
        
        # Add a delay for visibility
        time.sleep(0.5)

except KeyboardInterrupt:
    pass
finally:
    # Release the connection to the Arduino board
    board.exit()
