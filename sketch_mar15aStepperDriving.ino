// Include the Arduino Stepper Library
#include <Stepper.h>

// Number of steps per output rotation (200)
int stepsPerRevolution = 200;

// Create Instance of Stepper library
Stepper myStepper(stepsPerRevolution, 12, 11, 10, 9);


void setup()
{
	// set the speed at 120 rpm:
	myStepper.setSpeed(120);
	// initialize the serial port:
	//Serial.begin(9600);
  pinMode(3, INPUT_PULLUP);
  pinMode(4,INPUT_PULLUP);
  bool dirA = digitalRead(3);
  bool dirB = digitalRead(4);
  if(dirA == false){stepsPerRevolution = 200;}
  if(dirB == false){stepsPerRevolution = -200;} 
}

void loop() 
{
	myStepper.step(stepsPerRevolution);
}


