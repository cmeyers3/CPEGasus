#include <Servo.h>
#include "char2braille_array.h"
#include "pin_assignments.h" 
#include <stdlib.h>
#include <stdbool.h>


char incoming_byte = 0;  
const short cell_size = 6;   // 6 dots per cell 
const int   pin_high  = 180; // pin raise = servo at 180 deg
const int   pin_low   = 0;   // pin lower = servo at 0 deg 
// Set up servos  
const short pinStart  = 0; 
const short pinEnd    = 48; // number of servos used 
Servo servos[pinEnd]; //  create array of servos 

void setup() { 
	Serial.begin(9600); // probably speed this up 
	for(int i = pinStart; i < pinEnd; i++) { 
    servos[i].attach(pins[i]); // attach all servos 
    servos[i].write(pin_low); // set all to down 
	} 
} 

void loop() { 
	short current_cell 	= 0; // start displaying at cell 0 
	if(Serial.available() > 0) { 
		Serial.print("I received: "); 
		Serial.println(incoming_byte); 
		short braille_index = incoming_byte - 33; // 33 is ASCII for ! (the first element in the char2braille array) 
		Serial.println("char2braille index: "); 
		Serial.println(braille_index); 
    bool cell_array[6] = {0, 0, 0, 0, 0, 0}; // initialize pin array 
    for(short i = 0; i < 6; i++) { // get dot array  
		  cell_array[i] = braille_array[braille_index][i];
    }
		for(int j = 0; j < 6; j++) { 
			short pin = (current_cell * cell_size) + j; // pin/servo to change 
			if(cell_array[j]) { 
        servos[pin].write(pin_high); // set pin/servo to 180 if dot == 1
			} 
			else { 
				servos[pin].write(pin_low); // set pin/servo to 0 if dot == 0
			}	
			current_cell ++; // go to next cell 
		} 
	} 
} 
