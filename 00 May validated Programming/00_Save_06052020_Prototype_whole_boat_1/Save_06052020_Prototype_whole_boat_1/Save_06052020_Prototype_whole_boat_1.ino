// Position
// Date
// Batteries

// HARDWARE 
//
// SD
// CLCK 13
// DO 12
// DI 11
// CS 7
//
// GPS
//
// TX - 4
// RX - 3

// Batteries Data - A5
////////////////////////------------------------
// Steering
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
// Steering
////////////////////////------------------------

////////////////////////------------------------
// IMU
#include <Wire.h>
#include <TimerOne.h>

#define    MPU9250_ADDRESS            0x68
#define    MAG_ADDRESS                0x0C





// This function read Nbytes bytes from I2C device at address Address. 
// Put read bytes starting at register Register in the Data array. 
void I2Cread(uint8_t Address, uint8_t Register, uint8_t Nbytes, uint8_t* Data)
{
  // Set register address
  Wire.beginTransmission(Address);
  Wire.write(Register);
  Wire.endTransmission();
  
  // Read Nbytes
  Wire.requestFrom(Address, Nbytes); 
  uint8_t index=0;
  while (Wire.available())
    Data[index++]=Wire.read();
}


// Write a byte (Data) in device (Address) at register (Register)
void I2CwriteByte(uint8_t Address, uint8_t Register, uint8_t Data)
{
  // Set register address
  Wire.beginTransmission(Address);
  Wire.write(Register);
  Wire.write(Data);
  Wire.endTransmission();
}



// Initial time
long int ti;
volatile bool intFlag=false;
//IMU
////////////////////////------------------------




// Imput data
String Serial_reception;


// Boolean for propeller
bool Brush = true;

// --------------------------------------------
// Push button

// Setup the Button

volatile unsigned long time1 ;
volatile unsigned long time2 ;

volatile boolean valid1 = false ;
volatile boolean valid2 = false ;

// Setup the LEDs
int LED = 6;

// Push button
// --------------------------------------------
// -------------------------------------
// IMU

// IMU
// -------------------------------------
// SERVO

#include <Servo.h>  // add servo library

Servo myservo;  // create servo object to control a servo

int val;    // variable to read the value from the analog pin
int PinBatteries = A5; // Value for the batteries voltage
float BatteriesVoltage = 0;


// -------------------------------------
// Brushless, pin 8
Servo Brushless;

// ---------------------------------
// SD Card

#include <SD.h>
File myFile;

// -------------------------------------
// GPS

#include <SoftwareSerial.h>
String gps;
char hour[7];
char date[7];
char north[20];
char east[20];
char Start_chc[10];

SoftwareSerial ss(4, 3);

void setup() {
  ////////////////////////------------------------
// Steering

Rudder.attach(9);
Rudder.write(90);
Xmagnetometer=0;
Ymagnetometer=0;
vectoridealN = 0;
vectoridealE = 0;

// Steering
////////////////////////------------------------
  ////////////////////////////------------------------------------
  // UMU
  // Arduino initializations
  Wire.begin();
  Serial.begin(9600);

  // Set by pass mode for the magnetometers
  I2CwriteByte(MPU9250_ADDRESS,0x37,0x02);
  
  // Request continuous magnetometer measurements in 16 bits
  I2CwriteByte(MAG_ADDRESS,0x0A,0x16);
  
   pinMode(13, OUTPUT);
  Timer1.initialize(10000);         // initialize timer1, and set a 1/2 second period
  Timer1.attachInterrupt(callback);  // attaches callback() as a timer overflow interrupt
  
  
  // Store initial time
  ti=millis();

  // IMU
  /////////////////////////////-----------------------------------
  time1 = time2 = 0;
  // --------------------------------------------------------
  // Push button 


  // Push button
  //--------------------------------------------------------
  
  Serial_reception = "";
  
  Brushless.attach(8);
  // -----------------------------------
  // SERVO
  myservo.attach(5); // Ruddder
  myservo.write(90);
  //myservo.write(45); // Straight 
  
  // -----------------------------------
  // SD Card
    Serial.print("Initializing SD card...");
  // On the Ethernet Shield, CS is pin 4. It's set as an output by default.
  // Note that even if it's not used as the CS pin, the hardware SS pin 
  // (10 on most Arduino boards, 53 on the Mega) must be left as an output 
  // or the SD library functions will not work. 
   pinMode(10, OUTPUT);
   pinMode(7, OUTPUT);
 
  if (!SD.begin(7)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  myFile = SD.open("DATA.csv", FILE_WRITE);
 
  // if the file opened okay, write to it:
  if (myFile) {
    Serial.print("Writing to data.csv...");

    String header = "Date,Time,Position N,Position E,Voltage,IMU1,IMU2,IMU3,IMU4,IMU5,IMU6,IMU7,IMU8,IMU8";
    myFile.println(header);
      // close the file:
    myFile.close();
    Serial.println("done.");
  } else {
    // if the file didn't open, print an error:
    Serial.println("error opening DATA.csv");
  }






// -------------------------------------
// GPS

  Serial.begin(9600);
  ss.begin(9600);
  
  memset(hour, 0, sizeof(hour));
  memset(date, 0, sizeof(date));
  memset(north, 0, sizeof(north));
  memset(east, 0, sizeof(east));
  memset(Start_chc, 0, sizeof(Start_chc));
}

// ---------------------------------------------------------------
  ////////////////////////------------------------
// Steering
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

// Steering
  ////////////////////////------------------------
// -----------------------------------------------------

// ===========================================================================
void brushless(){
  if (Brush == true){
    Brushless.write(180);
  }
}
// ===========================================================================
void Display_data(){

      if (Serial_reception !="" ){
        Serial.println("You asked more informations about : ");
        Serial.print(Serial_reception);
        delay(500);
      }
      
      if (String(Serial_reception[0]) == "p" ){
        Serial.println("Position");
        Serial.print("North coordinates : ");
        Serial.println(north);
        Serial.print("East coordinates : ");
        Serial.println(east);
        delay(3000);
      }


      if (String(Serial_reception[0]) == "d" ){
        Serial.println("Date");
        Serial.print("Date : ");
        Serial.println(date);
        Serial.print("Hour : ");
        Serial.println(hour);
        delay(3000);
      }

      if (String(Serial_reception[0]) == "r" ){
        Serial.println("Rudder value");
        Serial.println(val);

        delay(3000);
      }

     if (String(Serial_reception[0]) == "b" ){
        BatteriesVoltage = analogRead(PinBatteries)*5.0 / 1023.0; // Calculate the Voltage of the batteries

        Serial.println("Batteries voltage");
        Serial.println(BatteriesVoltage);
        delay(3000);

      }
  
}
// ===========================================================================
// ===========================================================================
void Write_data(){
  //Serial.println("Start_chc"); 
  //Serial.println(gps); 
  //Serial.println(gps[16]); 
  if (String(Start_chc) == "GNRMC" && (String(gps[30]) != "") && (String(gps[16]) != "V")){
    Serial.println("DATA OK");
    
    //Serial.println("The start of the character chain is : "); 
    //Serial.println(Start_chc); 
    //Serial.println("From this line we will keep Hour & coordinates");
    memset(date, 0, sizeof(date));
    memset(hour, 0, sizeof(hour));
    memset(north, 0, sizeof(north));
    memset(east, 0, sizeof(east));
    for (int i = 0; i < 6 ; i++) {
        hour[i] = gps[i+6];
    }
    for (int i = 0; i < 9; i++) {
      north[i] = gps[i+18];
    }
    for (int i = 0; i < 10; i++) {
      east[i] = gps[i+31];
    }
  
    for (int i = 0; i < 6; i++) {
      date[i] = gps[i+52];
    }
    gps = "";

    // We have GPS data. Let's steering the boat
    positionN = int(north);
    positionE = int(east);


    IMU_values();
    
    reachpointN = 1;
    reachpointE = 0;
    
    orientation(reachpointE,reachpointN,positionE,positionN,Xmagnetometer,Ymagnetometer);

    
    Serial.println("Date ");
    Serial.println(date);
    Serial.println("North coordinates");
    Serial.println(north);
    Serial.println("East coordinates");
    Serial.println(east);
    Serial.println("Hour");
    Serial.println(hour);
    Serial.println("Batteries Voltage");
    Serial.println(analogRead(PinBatteries)*5.0 / 1023.0);
    
    
      myFile = SD.open("DATA.csv", FILE_WRITE);
    // if the file opened okay, write to it:
      if (myFile) {
        Serial.print("Writing to DATA.csv...");
  
        //myFile.print("Date   Hour   North     East \n"); 
        
        myFile.print(date); myFile.print(",");
        myFile.print(hour); myFile.print(",");
        myFile.print(north); myFile.print(",");
        myFile.print(east); myFile.print(",");
        myFile.print(analogRead(PinBatteries)*5.0 / 1023.0); // Calculate the Voltage of the batteries
      // close the file:
        myFile.close();
        Serial.println("done.");
      } else {
        // if the file didn't open, print an error:
        Serial.println("error opening DATA.csv");
      }
    
    }
    else {
      gps = "";
    }

}
// ===========================================================================
// --------------------------
// IMU


// Counter
long int cpt=0;

void callback()
{ 
  intFlag=true;
  digitalWrite(13, digitalRead(13) ^ 1);
}


void IMU_values(){
 delay(100);
  while (!intFlag);
  intFlag=false;
  
  // Display time
  Serial.print (millis()-ti,DEC);
  Serial.print ("\t");

  
  // _______________
  // ::: Counter :::
  
  // Display data counter
//  Serial.print (cpt++,DEC);
//  Serial.print ("\t");
  

  // _____________________
  // :::  Magnetometer ::: 

  
  // Read register Status 1 and wait for the DRDY: Data Ready
  
  uint8_t ST1;
  do
  {
    I2Cread(MAG_ADDRESS,0x02,1,&ST1);
  }
  while (!(ST1&0x01));

  // Read magnetometer data  
  uint8_t Mag[7];  
  I2Cread(MAG_ADDRESS,0x03,7,Mag);
  

  // Create 16 bits values from 8 bits data
  
  // Magnetometer
  int16_t mx=-(Mag[3]<<8 | Mag[2]);
  int16_t my=-(Mag[1]<<8 | Mag[0]);
  int16_t mz=-(Mag[5]<<8 | Mag[4]);
  
  
  // Magnetometer
  Serial.print (mx+200,DEC); 
  Serial.print ("\t");
  Serial.print (my-70,DEC);
  Serial.print ("\t");
  Serial.print (mz-700,DEC);  
  Serial.print ("\t");
  
  Xmagnetometer=mx+200;
  Ymagnetometer=my-70;
  
  // End of line
  Serial.println("");
//  delay(100);    

  
}

// IMU
// --------------------------
// ===========================================================================


void loop() {
  
  brushless;
  // put your main code here, to run repeatedly:
  gps = "";
  
    while (1==1){


      while (ss.available() > 0) {
        char c = ss.read();
        Serial.write(c);
        gps +=c;   
        if (c == '$') { 
         
          // Verifying the start of character chain
          memset(date, 0, sizeof(Start_chc));
          
          for (int i = 0; i < 5 ; i++) {
            //Serial.println(gps[i]); 
              Start_chc[i] = gps[i];
          }     

          Write_data();
     
           break;
        }
        
      }
      
        Serial_reception = "";
      while (Serial.available() > 0) {
        char a = Serial.read();
        Serial_reception +=a; delay(10);}
        
      // Display readed data
      Display_data();
   
    }

}
