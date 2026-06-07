#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;

enum ballState {POS1, POS2, POS3};
ballState state  = POS1;



void setup() {

  Serial.begin(115200);
  Serial.setTimeout(50);

  servo1.attach(4);
  servo2.attach(5);
  servo3.attach(6);
  
  levelplate();  // starting position
  delay(1000);  // wait before inputs ball moves
  applyState();   // move to the starting state  (POS1)
  delay(500);

  Serial.println("READY");

}

void move(int angle, Servo &servo){
  servo.write(angle);
}



void levelplate(){
  move(64, servo1);
  move(66, servo2);
  move(65, servo3);
}

void lowplate(){
  move(10, servo1);
  move(12, servo2);
  move(0, servo3);
}


void oneUp(){
  move(74, servo1);
  move(18, servo2);
  move(6, servo3);
}


void twoUp(){
  move(76, servo2);
  move(6, servo3);
  move(16, servo1);
}

void threeUp(){
  move(75, servo3);
  move(18, servo2);
  move(16, servo1);
}


void clockwise(){
  oneUp();
  delay(5000);
  twoUp();
  delay(5000);
  threeUp();
  delay(5000);
}

void antiClockwise(){
  threeUp();
  delay(500);
  twoUp();
  delay(500);
  oneUp();
  delay(500);
}

void slow(){
  for(int i = 0; i <= 70; i++){
    move((i + (i * 0.14)), servo1);
    delay(10);
    move((i + (i * 0.17)), servo2);
    delay(10);
    move(i, servo3);
    delay(10);

  }
  for(int i = 0; i > 70; i--){
    move(i + 10, servo1);
    delay(10);
    move(i + 12, servo2);
    delay(10);
    move(i, servo3);
    delay(10);

  }
}



// Positions

void position1(){
  move(16, servo1);  // low
  move(76, servo2);  // high
  move(75, servo3);  // high
}


void position2(){
  move(74, servo1);  // high
  move(76, servo2);  // high
  move(6, servo3);  // low
}


void position3(){
  move(74, servo1);  // high
  move(18, servo2);  // low
  move(75, servo3);  // high
}




void applyState() {
  switch (state) {
    case POS1: position1(); break;
    case POS2: position2(); break;
    case POS3: position3(); break;
  }
}

void stepForward() {
  switch (state) {
    case POS1: state = POS2; break;
    case POS2: state = POS3; break;
    case POS3: state = POS1; break;
  }
  applyState();
}

void stepBackward() {
  switch (state) {
    case POS1: state = POS3; break;
    case POS2: state = POS1; break;
    case POS3: state = POS2; break;
  }
  applyState();
}






void loop() {
  if (Serial.available() > 0) {
    int cmd = Serial.parseInt();

    // +1  move forward once
    if (cmd == 1) {
      stepForward();
    }

    // +2  move forward twice (wair between moves)
    else if (cmd == 2) {
      stepForward();
      delay(800);
      stepForward();
    }

    // -1  move backward once
    else if (cmd == -1) {
      stepBackward();
    }

    // -2  move backward twice (wait between moves)
    else if (cmd == -2) {
      stepBackward();
      delay(800);
      stepBackward();
    }

    Serial.print("CMD ");
    Serial.print(cmd);
    Serial.print(" -> STATE ");
    Serial.println(state);
  }


  //levelplate();
}



