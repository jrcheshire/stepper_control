// Stepper motor control using Arduino and Pyserial
// James Cheshire 2017 (last updated 5/17/2017)

int dirPin = 0;
int stepPin = 1;

int key = 0;
int val = 0;

String angleStr;
String speedStr;
String rotStr;

int temp = 0;
int angle = 0;
int speed = 0;
int rotations = 0;
int numSteps = 0;
float degPerStep = 1.8;
float timePerStep = 0;

void setup() {
  Serial.begin(115200);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin, OUTPUT);

  while(!Serial);
  
}

void loop(){
  
  if(Serial.available() > 0){
    // Read input string from serial port
    key = Serial.read();
    boolean finished = false;
    while(!finished){
      for(int i = 0; i < Serial.available(); i++){
        val = Serial.read();
        if(!key){
          angleStr += val;
        }
        else if(key){
          if(val == 44){
            temp = 1;
          }
          else if(val != 44 && !temp){
            speedStr += val;
          }
          else if(val != 44 && temp){
            rotStr += val;
          }
        }
      }
      delay(1100);
      if(Serial.available() == 0){
        finished = true;
      }
    }
    temp = 0;
    
    angle = angleStr.toInt();
    speed = speedStr.toInt();
    rotations = rotStr.toInt();

    // Perform rotation
    digitalWrite(dirPin, LOW); // Change this to HIGH to make it run in the other direction

    if(!key){
      numSteps = angle/degPerStep;
      for(int i = 0; i < numSteps; i++){
        digitalWrite(stepPin, HIGH);
        delay(100);
        digitalWrite(stepPin, LOW);
        delay(100);
      }
    }
    else if(key){
      numSteps = (360/degPerStep)*rotations;
      timePerStep = 1000*degPerStep/speed;
      for(int i = 0; i < numSteps; i++){
        digitalWrite(stepPin, HIGH);
        delay(timePerStep/2);
        digitalWrite(stepPin, LOW);
        delay(timePerStep/2);
      }
    }
    angleStr = "";
    speedStr = "";
    rotStr = "";
  }
}

