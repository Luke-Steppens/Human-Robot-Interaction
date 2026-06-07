#include <Servo.h>

Servo north;
Servo east;
Servo south;
Servo west;

void setup() {
  north.attach(4);
  east.attach(5);
  south.attach(6);
  west.attach(7);
  north.write(0);
  east.write(0);
  south.write(0);
  west.write(0);   // 
  delay(1000);     // 
}

void move(int angle, Servo servo){
  servo.write(angle);
}

// ==============================================
// ========   Plate Movement Functions   ========
// ==============================================

void levelplate(){
  move(30, north);
  move(30, east);
  move(30, south);
  move(30, west);
}


void northup(){
  move(45, north);
  move(30, east);
  move(30, south);
  move(15, west);
}


void eastup(){
  move(45, east);
  move(30, south);
  move(30, north);
  move(15, west);
}

void southup(){
  move(45, south);
  move(30, west);
  move(30, east);
  move(15, north);
}

void westup(){
  move(45, west);
  move(30, north);
  move(30, south);
  move(15, east);
}

// ==============================================
// ========        Ball  Locations      =========
// ==============================================


void ballnorth(){
  southup();
  delay(2000);
  levelplate();
  delay(2000);
}

void balleast(){
  westup();
  delay(2000);
  levelplate();
  delay(2000);
}

void ballsouth(){
  northup();
  delay(2000);
  levelplate();
  delay(2000);
}

void ballwest(){
  eastup();
  delay(2000);
  levelplate();
  delay(2000);
}


// ==============================================
// ========    Ball + Point, Location    ========  (think of better name of section)
// ==============================================


// All Postions the ball can be starting from north

void onePointFromNorth(){
  balleast();
}

void twoPointFromNorth(){
  balleast();
  ballsouth();
}

void onePointBackNorth(){
  ballwest();
}

void twoPointBackNorth(){
  ballwest();
  ballsouth();
}

// All Postions the ball can be starting from east

void onePointFromEast(){
  ballsouth();
}

void twoPointFromEast(){
  ballsouth();
  ballwest();
}

void onePointBackEast(){
  ballnorth();
}

void twoPointBackEast(){
  ballnorth();
  ballwest();
}

// All Positions the ball can be starting from south

void onePointFromSouth(){
  ballwest();
}

void twoPointFromSouth(){
  ballwest();
  ballnorth();
}

void onePointBackSouth(){
  balleast();
}

void twoPointBackSouth(){
  balleast();
  ballnorth();
}

// All Positions the ball can be starting from west

void onePointFromWest(){
  ballnorth();
}

void twoPointFromWest(){
  ballnorth();
  balleast();
}

void onePointBackWest(){
  ballsouth();
}

void twoPointBackWest(){
  ballsouth();
  balleast();
}




// move(15, north);



void loop() {


  ballnorth();
  balleast();
  ballsouth();
  ballwest();
  // levelplate();
  
  // northup();
  // delay(1000);
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