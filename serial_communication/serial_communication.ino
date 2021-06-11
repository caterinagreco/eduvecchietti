

#include <VarSpeedServo.h>

#include <FastLED.h>



#define START_VALUE '('
#define STOP_VALUE ')'
#define SEPARATOR ','

int testVictory;


VarSpeedServo myservo_coda; //create servo object to control a servo
VarSpeedServo myservo_zampe;

void setup() {
  Serial.begin(9600);
  while (!Serial) {} // wait for serial port to connect. Needed for native USB
  initNeoPixel();
  initServo();
  testVictory=0;

}

char stringa[100];
int Index;

void loop() {

  int i;
  int num;
  int ser;
  num = Serial.available();
  while (num != 0) {
    num--;
    ser = Serial.read();
    if (ser >= 0) {
      switch (ser) {
        case START_VALUE:
          Index = 1;
          stringa[0] = START_VALUE;
          break;
        case STOP_VALUE:
          if (Index >= 0) {
            stringa[Index] = STOP_VALUE;
            stringa[Index + 1] = 0;
            // Serial.println(stringa);
            elabora();
            Index = -1;
          }
          break;
        default:
          if (Index >= 0) {
            stringa[Index] = (unsigned char)ser;
            Index++;
          }
          break;
      }
    }
  }
  if(testVictory!=0)
    victory();
}

char matrice[5][20];

void elabora() {
  int i = 0;
  int j = 0;
  int c = 1;
  while (stringa[c] != STOP_VALUE) {
    if (stringa[c] != SEPARATOR ) {
      matrice[i][j] = stringa[c];
      c++;
      j++;
    } else {
      matrice[i][j] = '\0';
      c++;
      // Serial.println(matrice[i]);
      i++;
      j = 0;
    }
  }
  matrice[i][j] = '\0';
  // Serial.println(matrice[i]);


  if (strcmp(matrice[0], "led") == 0) {
    //chiama neopixel
    aggiornaLED();
  }

  if (strcmp(matrice[0], "servo") == 0) {
    if (strcmp(matrice[1], "correct") == 0)
      servoCorrect();
    if (strcmp(matrice[1], "victory") == 0)
      servoVictory();
  }

  if (strcmp(matrice[0], "animation") == 0) {
    if (strcmp(matrice[1], "gameon") == 0)
      gameOn();
    if (strcmp(matrice[1], "victory") == 0)
      testVictory=1;
      // victory();
    if (strcmp(matrice[1], "start") == 0)
      start();
    if (strcmp(matrice[1], "end") == 0) {
      endGame();
      testVictory=0;
    }
  
  }
}
