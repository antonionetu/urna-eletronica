#include <SPI.h>
#include <SD.h>

const int numButtons[10] = {4, 5, 6, 7, 8, 9, 10, 11, 12, 13};
const int cancelButton = 1;
const int clearButton = 2;
const int confirmButton = 3;

String input = "";

void setup() {
  Serial.begin(9600);

  if (!SD.begin(4)) {
    Serial.println("Erro ao inicializar o SD card!");
    return;
  }

  for (int i = 0; i < 10; i++) {
    pinMode(numButtons[i], INPUT_PULLUP);
  }
  pinMode(cancelButton, INPUT_PULLUP);
  pinMode(clearButton, INPUT_PULLUP);
  pinMode(confirmButton, INPUT_PULLUP);
}

void loop() {
  for (int i = 0; i < 10; i++) {
    if (digitalRead(numButtons[i]) == LOW) {
      input += String(i);
      File file = SD.open("../temp.txt", FILE_WRITE);
      
      if (file) {
        file.print(input);
        file.close();
      }
      
      delay(300);
    }
  }

  if (digitalRead(cancelButton) == LOW) {
    input = "";
    delay(300);
  }

  if (digitalRead(clearButton) == LOW) {
    input = "";
    delay(300);
  }

  if (digitalRead(confirmButton) == LOW) {
    delay(300);
    const char *command = "cmd /c ..\\client\\exec.bat";
    system(command);
  }
}
