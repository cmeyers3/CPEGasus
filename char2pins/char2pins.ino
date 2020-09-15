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

#define pinStart    = 0
#define pinEnd      = 48;       // Number servos used
#define cell_size   = 6;        // Dots per cell
#define pin_high    = 2000;     // Servo HIGH angle
#define pin_low     = 1000;     // Servo LOW angle

char incoming_byte = 0;  
Servo servos[pinEnd];           // Create array of servos 

void setup() { 
    Serial.begin(76800);        

    for(int i = pinStart; i < pinEnd; i++) { 
        servos[i].attach(pins[i], 800, 2200);       // Attach all servos 
        servos[i].write(pin_low);                   // Set all to down 
    } 
} 

void loop() { 
    short current_cell 	= 0;                        // Start displaying at cell 0 

    if(Serial.available() > 0) { 
        Serial.print("I received: "); 
        Serial.println(incoming_byte); 

        // 33 is ASCII for ! (the first element in the char2braille array) 
        short braille_index = incoming_byte - 33;   

        Serial.print("char2braille index: "); 
        Serial.println(braille_index); 
        bool cell_array[6] = {0, 0, 0, 0, 0, 0};        // Initialize pin array 
        
        for(short i = 0; i < 6; i++)                    // Get dot array  
            cell_array[i] = braille_array[braille_index][i];

        for(int j = 0; j < 6; j++) { 
            short pin = (current_cell * cell_size) + j; // pin/servo to change 
            
            if (cell_array[j]) 
                servos[pin].writeMicroseconds(pin_high); // set pin/servo to 180 if dot == 1
            else 
                servos[pin].writeMicroseconds(pin_low); // set pin/servo to 0 if dot == 0
            
            current_cell ++;                            // go to next cell 
        } 
    } 
} 
