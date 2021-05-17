

#define NUM_LEDS 36
#define DATA_PIN 6

const char strumenti[][20] = {
  "bass",
  "piano",
  "string_ensamble",
  "brass_section",
  "woods",
  "battery"
};



CRGB leds[NUM_LEDS];

void initNeoPixel() {
  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(84);
}


void ledRefresh()
{
  FastLED.show();
}

int trovaStrumento(char *strum)
{
  int ret;
  int i;
  ret = -1;
  for (i = 0; i < 6 && ret < 0; i++) {
    if (strcmp(strumenti[i], strum) == 0) {
      ret = i;
    }
  }
  return ret;
}

void aggiornaLED()
{
  // trova strumento -> quali led vanno accesi o spenti
  int strumento;
  int l;
  strumento = trovaStrumento(matrice[1]);
  if (strumento >= 0) {
    if (strcmp(matrice[3], "verde") == 0) {
      if (strcmp(matrice[2], "1") == 0) { // accendi il verde
        for (l = 0; l < 6; l++) {
          leds[l + strumento * 6] = CRGB::Green;
        }
      } else {
        for (l = 0; l < 6; l++) {
          leds[l + strumento * 6] = CRGB::Black;
        }
      }
    }
    if (strcmp(matrice[3], "rosso") == 0) {
      if (strcmp(matrice[2], "1") == 0) { // accendi il verde
        for (l = 0; l < 6; l++) {
          leds[l + strumento * 6] = CRGB::Red;
        }
      } else {
        for (l = 0; l < 6; l++) {
          leds[l + strumento * 6] = CRGB::Black;
        }
      }
    }
    ledRefresh();
  }
}
void fadeall() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i].nscale8(250);
  }
}


void accensione() {
  FastLED.setBrightness(84);
  int k = 0;
  for (k = 0; k < 4; k++) {
    static uint8_t hue = 0;
    // First slide the led in one direction
    for (int i = 0; i < NUM_LEDS; i++) {
      // Set the i'th led to red
      leds[i] = CHSV(hue++, 255, 255);
      // Show the leds
      FastLED.show();
      // now that we've shown the leds, reset the i'th led to black
      // leds[i] = CRGB::Black;
      fadeall();
      // Wait a little bit before we loop around and do it again
      delay(10);
    }
    Serial.print("x");

    // Now go in the other direction.
    for (int i = (NUM_LEDS) - 1; i >= 0; i--) {
      // Set the i'th led to red
      leds[i] = CHSV(hue++, 255, 255);
      // Show the leds
      FastLED.show();
      // now that we've shown the leds, reset the i'th led to black
      // leds[i] = CRGB::Black;
      fadeall();
      // Wait a little bit before we loop around and do it again
      delay(10);
    }
  }
  FastLED.clear();  // clear all pixel data
  FastLED.show();
}

void start() {
 int i=0;
  fill_solid( leds, NUM_LEDS, CRGB::Red);
  FastLED.setBrightness(0);
  FastLED.show();
  fade_in();
  delay(700);
  fade_out();
  FastLED.clear();
  FastLED.show();
  delay(700);
  
  fill_solid( leds, NUM_LEDS, CRGB::Yellow);
  FastLED.setBrightness(0);
  FastLED.show();
  fade_in();
  delay(700);
  fade_out();
  FastLED.clear();
  FastLED.show();
  delay(700);
  
  for (i = 0; i< 3; i++) {
    fill_solid( leds, NUM_LEDS, CRGB::Green);
    FastLED.setBrightness(0);
    FastLED.show();
   fade_in();
  delay(200);
  fade_out();
    FastLED.clear();
    FastLED.show();
    delay(200);
  }
}

void fade_in(){
 int k=0;
  for(k=0;k<85;k++){
  FastLED.setBrightness(k);
  FastLED.show();
  }
}

void fade_out(){
int  k=0;
  for(k=85;k>0;k--){
  FastLED.setBrightness(k);
  FastLED.show();
  }
  }
