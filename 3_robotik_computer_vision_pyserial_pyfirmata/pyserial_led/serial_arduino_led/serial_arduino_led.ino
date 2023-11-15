/*
 * Author:Ivan Iovine
 * Institution: Robotik Lab HfG Offenbach
 */

int ledPin = 13;  // define led pin

void setup() {
  pinMode(ledPin, OUTPUT);  // Config pin LED and init as OUTPUT
  Serial.begin(9600);  // init Serial Baudrate
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // read serial from python
    if (command == 'H') {
      digitalWrite(ledPin, HIGH);  // high led
      //Serial.println("LED is ON");  // Send a response with a newline character
    } else if (command == 'L') {
      digitalWrite(ledPin, LOW);  // low led
      //Serial.println("LED is OFF");  // Send a response with a newline character
    }
  }
}h
