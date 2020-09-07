/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/Blink
*/
int incoming_byte = 0; 
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  //open serial port 
  Serial.begin(9600); 
  
}

// the loop function runs over and over again forever
void loop() {
  //check for incoming serial data: 
  if (Serial.available() > 0) { 
    incoming_byte = Serial.read(); 
    if(incoming_byte != 10) {   
      Serial.print("I received: "); 
      Serial.println(incoming_byte); 
      int vArray[5] = {1, 2, 3, 4, 5}; 
      int light_time = vArray[incoming_byte - 65]; 
      Serial.println("Light time: "); 
      Serial.println(light_time*1000); 
      Serial.println("Turning on...."); 
      digitalWrite(LED_BUILTIN, HIGH);    // turn the LED on (HIGH is the voltage level)
      delay(light_time*1000);             // wait for a second
      Serial.println("Turning off...."); 
      digitalWrite(LED_BUILTIN, LOW);     // turn the LED off by making the voltage LOW
      delay(light_time*1000);             // wait for a second
      Serial.println("End of loop"); 
    } 
  } 
}
