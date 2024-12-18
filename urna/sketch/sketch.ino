const int numButtons[10] = {4, 5, 6, 7, 8, 9, 10, 11, 12, 13};
const int clearButton = 2;
const int confirmButton = 3;

unsigned long lastDebounceTime[10];
unsigned long lastDebounceTimeControl[3];
unsigned long debounceDelay = 50;
bool lastButtonState[10];
bool buttonState[10];

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 10; i++) {
    pinMode(numButtons[i], INPUT_PULLUP);
    lastButtonState[i] = HIGH;
    lastDebounceTime[i] = 0;
  }

  pinMode(clearButton, INPUT_PULLUP);
  pinMode(confirmButton, INPUT_PULLUP);
}

void loop() {
  for (int i = 0; i < 10; i++) {
    debounceButton(i);
  }

  debounceControlButton(clearButton, "Botão Limpar pressionado", 1);
  debounceControlButton(confirmButton, "Botão Confirmar pressionado", 2);

  delay(10);
}

void debounceButton(int index) {
  int reading = digitalRead(numButtons[index]);

  if (reading != lastButtonState[index]) {
    lastDebounceTime[index] = millis();
  }

  if ((millis() - lastDebounceTime[index]) > debounceDelay) {
    if (reading != buttonState[index]) {
      buttonState[index] = reading;
      if (buttonState[index] == LOW) {
        Serial.println(index);
      }
    }
  }

  lastButtonState[index] = reading;
}

void debounceControlButton(int pin, String buttonName, int controlIndex) {
  int reading = digitalRead(pin);

  static int lastControlButtonState[3] = {HIGH, HIGH, HIGH};
  static unsigned long lastDebounceTimeControl[3] = {0, 0, 0};

  if (reading != lastControlButtonState[controlIndex]) {
    lastDebounceTimeControl[controlIndex] = millis();
  }

  if ((millis() - lastDebounceTimeControl[controlIndex]) > debounceDelay) {
    if (reading == LOW) {
      if (pin == clearButton) {
        Serial.println("LIMPAR");
      } else if (pin == confirmButton) {
        Serial.println("CONFIRMAR");
      }
    }
  }

  lastControlButtonState[controlIndex] = reading;
}
