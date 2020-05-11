#include <Servo.h>


Servo Thruster;
 
void setup()
{
Thruster.attach(8);
Serial.begin(9600);
}
 
void loop()
{

Thruster.write(180);

}
