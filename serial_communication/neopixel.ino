#define FRAMES_PER_SECOND  120
#define NUM_LEDS 36
#define DATA_PIN 6

FASTLED_USING_NAMESPACE

const char strumenti[][20] = {
  "bass",
  "piano",
  "string_ensamble",
  "brass_section",
  "woods",
  "drums"
};

CRGB leds[NUM_LEDS];

void initNeoPixel() {
  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(150);
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
    if (strcmp(matrice[3], "green") == 0) {
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
    if (strcmp(matrice[3], "red") == 0) {
      if (strcmp(matrice[2], "1") == 0) { // accendi il rosso
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


void victory() { // la funzione va avanti all'infinito (richiamata dal loop) finchè non arriva il messaggio (animation,end)

  int durata = 1500;
  FastLED.setBrightness(150);
  int k = 0;

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




void start() {
  int i = 0;
  int durata = 100;
  
  fill_solid( leds, NUM_LEDS, CRGB::Red);
  FastLED.setBrightness(0);
  FastLED.show();
  fade_in();
  delay(500);
  fade_out();
  FastLED.clear();
  FastLED.show();
  delay(500);

  fill_solid( leds, NUM_LEDS, CRGB::Yellow);
  FastLED.setBrightness(0);
  FastLED.show();
  fade_in();
  delay(500);
  fade_out();
  FastLED.clear();
  FastLED.show();
  delay(500);

  for (i = 0; i < 3; i++) {
    green_light(durata);
  }
}

void fade_in() {
  int k = 0;
  for (k = 0; k < 130; k++) {
    FastLED.setBrightness(k);
    FastLED.show();
  }
}

void fade_out() {
  int  k = 0;
  for (k = 130; k > 0; k--) {
    FastLED.setBrightness(k);
    FastLED.show();
  }
}

uint8_t gHue = 0; // rotating "base color" used by many of the patterns

void gameOn() {
  FastLED.setBrightness(150);
  int i;
  int durata = 1500;
  long int current_millis = millis();

  while (millis() - current_millis < 5000) { //timer
    Serial.println(millis() - current_millis);
    // a colored dot sweeping back and forth, with fading trails
    fadeToBlackBy( leds, NUM_LEDS, 20);
    int pos = beatsin16( 13, 0, NUM_LEDS );
    leds[pos] += CHSV( gHue, 255, 192);
    // send the 'leds' array out to the actual LED strip
    FastLED.show();
    // insert a delay to keep the framerate modest
    FastLED.delay(1000 / FRAMES_PER_SECOND);

    // do some periodic updates
    EVERY_N_MILLISECONDS( 20 ) {
      gHue++;  // slowly cycle the "base color" through the rainbow
    }
  }
  current_millis = 0;
  fade_out();
  green_light(durata);

}

void endGame(){
  fade_out();
  FastLED.clear();
  FastLED.show();
}

void green_light(int durata) {

  fill_solid( leds, NUM_LEDS, CRGB::Green);
  FastLED.setBrightness(0);
  FastLED.show();
  fade_in();
  delay(durata);
  fade_out();
  FastLED.clear();
  FastLED.show();
  delay(durata);
  FastLED.setBrightness(150);

}
