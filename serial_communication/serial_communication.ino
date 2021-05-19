#include <VarSpeedServo.h>

#include <FastLED.h>



#define START_VALUE '('
#define STOP_VALUE ')'
#define SEPARATOR ','



VarSpeedServo myservo_coda; //create servo object to control a servo
VarSpeedServo myservo_zampe;

void setup() {
  Serial.begin(9600);
  while (!Serial) {} // wait for serial port to connect. Needed for native USB
  initNeoPixel();
  initServo();
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

  if (strcmp(matrice[0], "motore") == 0) {
    if (strcmp(matrice[1], "coda") == 0)
      muoviCoda();
    if (strcmp(matrice[1], "zampe") == 0)
      muoviZampe();
  }

  if (strcmp(matrice[0], "animazione") == 0) {
    if (strcmp(matrice[1], "accensione") == 0)
      accensione();
      if (strcmp(matrice[1], "start") == 0)
      start();
    //if (strcmp(matrice[1], "end") == 0)
    //endgame();
  }
}
