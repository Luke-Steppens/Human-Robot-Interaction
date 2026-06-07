#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;


void setup() {
  servo1.attach(4);
  servo2.attach(5);
  servo3.attach(6);
  
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
     // Move to zero
  delay(1000);      // 1 second
}

void move(int angle, Servo servo){
  servo.write(angle);
}



void levelplate(){
  move(74, servo1);
  move(76, servo2);
  move(75, servo3);
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




void loop() {

  // antiClockwise();
  // clockwise();
  

  // oneUp();
  // delay(500);
  // twoUp();
  // delay(500);
  // threeUp();
  // delay(500);
  // levelplate();
  // delay(1000);
    lowplate();
  // delay(1000);

  // slow();
  

  

  
}
