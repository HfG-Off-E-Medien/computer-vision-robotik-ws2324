/*
 * Author:Ivan Iovine
 * Institution: Robotik Lab HfG Offenbach
 */

#include <Servo.h> // use Servo library
Servo myservo; // define var from type servo gived by the library 
String inByte; // define String to read incoming Bytes from Serial
int d = 0; // define integer var for servo degree

void setup() {
   myservo.attach(6); // config pin servo
   Serial.begin(9600); // init Serial Baudrate for Serial communication
   Serial.setTimeout(10); // set Timeout to avoid noise
}

void loop() {
   if(Serial.available()>0) // check if serial data is available
   {
    // If data is available to read,
     inByte = Serial.readString(); // read it and store it in val
     Serial.println(inByte); // send back the value to python via seril
     d = inByte.toInt(); // convert string in integer
     myservo.write(d); // use integer as servo degree
   }
 }
