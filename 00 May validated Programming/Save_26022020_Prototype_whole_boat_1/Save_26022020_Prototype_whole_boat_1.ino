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

int potpin = 3;  // analog pin used to connect the potentiometer
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
char north[11];
char east[20];
char Start_chc[10];

SoftwareSerial ss(4, 3);

void setup() {
  Serial.begin(9600);
  time1 = time2 = 0;
  // --------------------------------------------------------
  // Push button 
  // Set Pin Modes
  pinMode(LED, OUTPUT);

  //Attach the interrupt

  attachInterrupt(digitalPinToInterrupt(2), button_down, HIGH); 
  // https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/
  // Push button
  //--------------------------------------------------------
  
  Serial_reception = "";
  
  Brushless.attach(8);
  // -----------------------------------
  // SERVO
  myservo.attach(5); // Ruddder
  
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
// Push button

void button_down ()
{
  //Serial.println("----------------------------------------------------------------------------");
 while (1==1){
      if (!valid1)
    {
      if (time1 == 0 ){
       
        time1 = millis() ;
        //Serial.println("time1");
        //Serial.println(time1);
        valid1 = true ;
        break;
      }
      else{
        time2 = millis() ;
        valid2 = true ;
        //Serial.println("time2");
        //Serial.println(time2);
        
      }
    }
    if (valid1 && !valid2)
    {
      time2 = millis() ;
      valid2 = true ;
      Serial.println("time2");
      Serial.println(time2);
    }
    break;
 }
}

// Push button
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
// PUSH BUTTON


void push_button (){

        if (valid2){
          unsigned long buttonTime = time2-time1;
          //Serial.println("buttonTime");
          //Serial.println(buttonTime);
          if (buttonTime >= 2000 && buttonTime < 5000) {
            analogWrite(LED, 255);  
            //Serial.println("SIGNAL1");
            delay(1000);  
            analogWrite(LED, LOW);  
          }
          else if(buttonTime >= 5000){
            analogWrite(LED, 255);
            //Serial.println("SIGNAL2");
            delay(1000);  
            analogWrite(LED, LOW);  
          }
          time1 = time2 = 0;
          valid1 = valid2 = false ;
        }
  
}
// PUSH BUTTON
// --------------------------
// ===========================================================================


void loop() {
  
  brushless;
  // put your main code here, to run repeatedly:
  gps = "";
  
    while (1==1){

      push_button ();


        if (pow((val-analogRead(potpin)),2)>100){
          val = analogRead(potpin);            // reads the value of the potentiometer (value between 0 and 1023)
          myservo.write(map(val, 0, 1023, 0, 180));                  // sets the servo position according to the scaled value
          //myservo.write(val/5.68);
          
          Serial.println(val/5.68);
          delay(150);                           // waits for the servo to get there
        }
     

     
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
