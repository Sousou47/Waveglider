
String data;
String PositionN;
String PositionE;
String if_positionreached;
boolean Reached;
int counter_directions;
void setup() {
  // put your setup code here, to run once:

Serial.begin(115200);
data = "1 59.549 10.438 2 34.587 23.934 3 34.583 100.243 4 28.242 83.343";
}

void interpretation(){

  Reached = false;
  PositionE="";
  PositionN="";
  // put your main code here, to run repeatedly:
    counter_directions = 0;
    for (int i(0); i < data.length(); i++)
  {
    if (counter_directions == 1){
      PositionN += data[i];
    }
    if (counter_directions == 2){
      PositionE += data[i];
    }
    if (String(data[i]) == String(" ")){
      counter_directions +=1;
    }
    if (counter_directions == 3){
      // Test if the coordinates to be reached is enought close than the GPS position
      // PositionE
      // PositionN
      Reached = false;
      //Reached = true;
    }
      if (Reached == true){
        if_positionreached += data[i];
    }
       
  }
Serial.println(PositionE);
Serial.println(PositionN);
// We remove the first character that is : " ".
if_positionreached.remove(0,1);
if (Reached == true){
    data = if_positionreached;
}

Serial.println(data);

  
}


void loop() {
interpretation();
delay(100000);
}
