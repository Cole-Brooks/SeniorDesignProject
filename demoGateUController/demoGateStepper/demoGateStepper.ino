/*
  Stepper Motor Driver Code:
  goes onto an arduino connected to the testing apparatus. Currently just spins the stepper motor when 
*/
#define STEPPER_PIN_1 2
#define STEPPER_PIN_2 3
#define STEPPER_DIR 4
#define STEPPER_PULSE 5
int step_number = 0;
void setup() {
  pinMode(STEPPER_PIN_1, OUTPUT);
  pinMode(STEPPER_PIN_2, OUTPUT);
  pinMode(STEPPER_DIR, OUTPUT);
  pinMode(STEPPER_PULSE, OUTPUT);
  digitalWrite(STEPPER_DIR, LOW);
  Serial.begin(9600);
}

void loop() {
  // Stepper motor set to 200 pulses per revolution
  // We want the gate to swing 90 degrees
  for(x = 0; x <=50; x++){
    digitalWrite(STEPPER_PULSE, LOW);
    digitalWrite(STEPPER_PULSE, HIGH);
    delayMicroseconds(500);
  }

}


