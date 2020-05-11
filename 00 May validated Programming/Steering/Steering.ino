
#include <math.h>
#include <Servo.h>  // add servo library
Servo Rudder;  // create servo object to control a servo

float Xmagnetometer;
float Ymagnetometer;
float actual_angle;
float exhausted_angle;
float positionE;
float reachpointE;
float positionN;
float reachpointN;
float vectoridealE;
float vectoridealN;
float differenceangle; 

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);

Rudder.attach(9);
Rudder.write(90);
delay(2000);
Xmagnetometer=0;
Ymagnetometer=0;
vectoridealN = 0;
vectoridealE = 0;
 
}



void orientation( float(reachpointE),float(reachpointN),float(positionE),float(positionN),float(Xmagnetometer),float(Ymagnetometer)){



actual_angle =   atan2 (Xmagnetometer,Ymagnetometer);  // arc tangent of y/x


vectoridealE = reachpointE - positionE;
vectoridealN = reachpointN - positionN;

exhausted_angle =    atan2 (vectoridealN,vectoridealE);  // arc tangent of y/x

differenceangle =   actual_angle - exhausted_angle;
Serial.println("");
Serial.println("actual_angle");
Serial.println(actual_angle);
Serial.println("exhausted_angle");
Serial.println(exhausted_angle);
Serial.println("Angle difference : ");
Serial.println(differenceangle);


if (differenceangle <= -0.78){ Serial.println("Ruder - 35°");Rudder.write(45);}
if (differenceangle > -0.17 && differenceangle < -0.78){ Serial.println("Ruder - 15°");Rudder.write(75);}
if (differenceangle > -0.17 && differenceangle < 0.17){ Serial.println("Ruder 0°");Rudder.write(90);}
if (differenceangle > 0.17 && differenceangle < 0.78){ Serial.println("Ruder 15°");Rudder.write(105);}
if (differenceangle > 0.78){ Serial.println("Ruder 35°");Rudder.write(115);}
Serial.println("");
delay(2000);
}

void loop() {


positionN = 0;
positionE = 0;

Xmagnetometer=0;
Ymagnetometer=1;

reachpointN = 1;
reachpointE = 0;

orientation(reachpointE,reachpointN,positionE,positionN,Xmagnetometer,Ymagnetometer);

Xmagnetometer=1;
Ymagnetometer=0;

reachpointN = 0;
reachpointE = 1;

orientation(reachpointE,reachpointN,positionE,positionN,Xmagnetometer,Ymagnetometer);


Xmagnetometer=1;
Ymagnetometer=1;
reachpointN = 1;
reachpointE = 1;
orientation(reachpointE,reachpointN,positionE,positionN,Xmagnetometer,Ymagnetometer);


}
