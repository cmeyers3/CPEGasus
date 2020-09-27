/* char2pins.ino 
 * Arduino main source code for Braille Bot
 * 
 * CPEGasus
 */

#include <Servo.h>
#include "char2braille_array.h"
#include "pin_assignments.h" 
#include <stdlib.h>
#include <stdbool.h>

#define refresh     '~'         // Character to send for refresh
#define pinStart    0
#define pinEnd      48          // Number servos used
#define cell_size   6           // Dots per cell
#define pin_high    2000        // Servo HIGH angle
#define pin_low     1000        // Servo LOW angle
#define anaPin      A5          // Analog pin for photoresistor

char    incoming_byte   = 0;  
short   current_cell    = 0;
int     thresh          = 0;    // ADC threshold to send ready signal
Servo   servos[pinEnd];         // Create array of servos 

void setup() { 
    Serial.begin(57600);        

    for(short i = pinStart; i < pinEnd; i++) { 
        servos[i].attach(pins[i], 800, 2200);       // Attach all servos 
        servos[i].writeMicroseconds(pin_low);       // Set all to down 
        delay(100);
    } 

    int temp = 0;
    for (short i = 0; i < 1024; i++) temp += analogRead(anaPin); 
    thresh = temp >> 10;
} 

void loop() { 
    if (current_cell > 7) current_cell = 0;

    incoming_byte = Serial.read();
    if(incoming_byte > 0) { 
        // Convert ASCII to braille index (see char2braille_array.h)
        short braille_index = incoming_byte - 32;   
        bool cell_array[6] = {0, 0, 0, 0, 0, 0};        // Initialize pin array 
        
        for(short i = 0; i < 6; i++)                    // Get dot array  
            cell_array[i] = braille_array[braille_index][i];

        for(short j = 0; j < 6; j++) { 
            short pin = (current_cell * cell_size) + j; // pin/servo to change 
            
            if (cell_array[j])      // Set pin/servo to MAX if (dot == 1) 
                servos[pin].writeMicroseconds(pin_high); 
            else                    // Set pin/servo to MIN if (dot == 0)
                servos[pin].writeMicroseconds(pin_low);
        }

        delay(100);
        current_cell++; 
    } 

    int val = analogRead(A0);
    if (val < (0.8 * thresh)) {
        Serial.print(refresh);
        current_cell = 0;
    }
} 
