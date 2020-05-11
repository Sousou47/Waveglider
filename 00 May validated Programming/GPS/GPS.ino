
#include <SoftwareSerial.h>

// The serial connection to the GPS module
SoftwareSerial ss(4, 3);
byte gpsData;
String gps;

void setup(){
  Serial.begin(9600);
  ss.begin(9600);
 
}

void loop(){
  while (ss.available() > 0){
    // get the byte data from the GPS
    gpsData = ss.read();
    Serial.write(gpsData);

  }



}
