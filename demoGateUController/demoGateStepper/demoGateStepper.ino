/*
  Stepper Motor Driver Code:
  goes onto an arduino connected to the testing apparatus. Currently just spins the stepper motor when 
*/
#define STEPPER_PIN_1 2
#define STEPPER_PIN_2 3
#define STEPPER_DIR 4
#define STEPPER_PULSE 5
#define STEPPER_IN 6

bool gate_open = false;

void setup() {
  pinMode(STEPPER_PIN_1, OUTPUT);
  pinMode(STEPPER_PIN_2, OUTPUT);
  pinMode(STEPPER_DIR, OUTPUT);
  pinMode(STEPPER_PULSE, OUTPUT);
  pinMode(STEPPER_IN, INPUT);
  digitalWrite(STEPPER_DIR, LOW);
  Serial.begin(9600);
}

void loop() {
  if(digitalRead(STEPPER_IN)){
    // We have a command to open the gate
    if(gate_open){
      // gate is already open, do nothing
      Serial.println("gate is already open...");
    }
    else{
      open();
    }
  }
  else{
    if(gate_open){
      close();
    }
    // implicit else, do nothing because gate is already shut
  }
}

//////////////////////////////////////////////////////////////////
// Gate Open/Close functions:

// Stepper motor set to 200 pulses per revolution
// We want the gate to swing 90 degrees, 360/200 = 90/50
// so pulse 50 times

void open(){
  digitalWrite(STEPPER_DIR, HIGH); // set direction
  for(int x = 0; x <=50; x++){
    digitalWrite(STEPPER_PULSE, LOW);
    digitalWrite(STEPPER_PULSE, HIGH);
    delayMicroseconds(500);
  }
  gate_open = true;
}

void close(){
  digitalWrite(STEPPER_DIR, LOW); // set direction
  for(int x = 0; x <=50; x++){
    digitalWrite(STEPPER_PULSE, LOW);
    digitalWrite(STEPPER_PULSE, HIGH);
    delayMicroseconds(500);
  }
  gate_open = false;
}
