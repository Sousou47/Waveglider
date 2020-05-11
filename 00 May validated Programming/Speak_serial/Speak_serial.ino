String Serial_reception;

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  Serial_reception = "";
}

void loop() {
  // send data only when you receive data:
  while (Serial.available() > 0) {
    char c = Serial.read();
    Serial_reception +=c;
  }

    // say what you got:
  Serial.print("I received: ");
  Serial.println(Serial_reception);
  delay(1000);
  Serial_reception = "";
}
