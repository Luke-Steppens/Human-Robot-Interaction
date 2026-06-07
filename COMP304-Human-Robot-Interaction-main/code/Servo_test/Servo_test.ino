#include <Servo.h>

Servo north;
Servo east;
Servo south;
Servo west;

void setup() {
  north.attach(4);
  east.attach(7);
  south.attach(6);
  west.attach(5);
  north.write(0);
  east.write(0);
  south.write(0);
  west.write(0);   // Move to zero
  delay(1000);      // 1 second
}

void move(int angle, Servo servo){
  servo.write(angle);
}



void levelplate(){
  move(30, north);
  move(30, east);
  move(30, south);
  move(30, west);
}




void northup(){
  move(60, north);
  move(30, east);
  move(30, south);
  move(15, west);
}


void eastup(){
  move(60, east);
  move(30, south);
  move(30, north);
  move(15, west);
}

void southup(){
  move(60, south);
  move(30, west);
  move(30, east);
  move(15, north);
}

void westup(){
  move(60, west);
  move(30, north);
  move(30, south);
  move(15, east);
}

void ballnorth(){
  southup();
  levelplate();
}

void balleast(){
  westup();
  levelplate();
}

void ballsouth(){
  northup();
  levelplate();
}

void ballwest(){
  eastup();
  levelplate();
}


// move(15, north);



void loop() {

  northup();
  delay(1000);
  // eastup();
  // delay(1000);
  // southup();
  // delay(1000);
  // westup();
  // delay(1000);


  // move(15, servo3);

  // north.write(60);
  // delay(1000);

  // north.write(0);
  // delay(1000);

  // east.write(60);
  // delay(1000);

  // east.write(0);
  // delay(1000);

  // south.write(60);
  // delay(1000);

  // south.write(0);
  // delay(1000);

  // west.write(60);
  // delay(1000);

  // west.write(0);
  // delay(1000);

  
}
