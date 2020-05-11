
int Winchup = 4;
int Winchdown = 5;


void setup() {
  // put your setup code here, to run once:
  pinMode(Winchup, OUTPUT);
  pinMode(Winchdown, OUTPUT);

  Serial.begin(9600);

}

void winchup(){
 analogWrite(Winchdown,0); 
 analogWrite(Winchup,255);  
 delay(1000);
}

void winchdown(){
 analogWrite(Winchup,0);  
 analogWrite(Winchdown,255); 
 delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
winchdown();
winchup();
}
