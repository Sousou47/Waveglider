int analogPin = A5; // potentiometer wiper (middle terminal) connected to analog pin 3
                    // outside leads to ground and +5V
float val = 0;  // variable to store the value read

void setup() {
  Serial.begin(9600);           //  setup serial
}

void loop() {
  val = analogRead(analogPin)*5.0 / 1023.0;  // read the input pin
  Serial.println(val);          // debug value
}
