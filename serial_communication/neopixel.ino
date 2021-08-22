#define FRAMES_PER_SECOND  120
#define NUM_LEDS 36
#define DATA_PIN 6

FASTLED_USING_NAMESPACE
uint8_t gHue = 0;

const char strumenti[][20] = {
  "bass",
  "piano",
  "string_ensamble",
  "brass_section",
  "woods",
  "drums"
};

CRGB leds[NUM_LEDS];

// Inizializzazione NeoPixel, come da libreria

void initNeoPixel() { 
  FastLED.addLeds<WS2812, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(150);
}

void ledRefresh()
{
  FastLED.show();
}

// trovaStrumento-> Funzione usata da aggiornaLED
// Restituisce nella variabile "ret" la posizione nell'array "strumenti" dello strumento chiamato da Raspberry

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

// aggiornaLED-> Analizza la matrice ed aggiorna lo stato dei 36 NeoPixel.
// Identifica lo strumento chiamato con trovaStrumento, indirizza i led corrispondeti a quello strumento,
// li accende di rosso o verde o li spegne

void aggiornaLED()
{
  
  int strumento;
  int l;
  strumento = trovaStrumento(matrice[1]);
  if (strumento >= 0) {
    if (strcmp(matrice[3], "green") == 0) {
      if (strcmp(matrice[2], "1") == 0) {
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
      if (strcmp(matrice[2], "1") == 0) {
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

// victroy-> Algoritmo reperito online
// La funzione va avanti all'infinito (richiamata dal loop) finchè non arriva il messaggio (animation,end)
// Scorre i led in una direzione, spostando un colore dal LED al successivo
// Arrivato alla fine, torna indietro e fa la stessa cosa. Cambia colore secondo la scala RGB.

void victory() {

  int durata = 1500;
  FastLED.setBrightness(150);
  int k = 0;
  static uint8_t hue = 0;
    
  for (int i = 0; i < NUM_LEDS; i++) {      
    leds[i] = CHSV(hue++, 255, 255);
    FastLED.show();
    fadeall();
    delay(10);
  }

  for (int i = (NUM_LEDS) - 1; i >= 0; i--) {
    leds[i] = CHSV(hue++, 255, 255);
    FastLED.show();
    fadeall();   
    delay(10);
  }
}

// fadeall-> Funzione dell'algoritmo victory, spegne lentamente tutti i led

void fadeall() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i].nscale8(250);
  }
}

// start-> Accende e spegne tutti i LED contemporaneamente, colorandoli prima di rosso, 
// poi di giallo e infine per tre volte di verde

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

// fade_in-> Aumento graduale della luminossità

void fade_in() {
  int k = 0;
  for (k = 0; k < 130; k++) {
    FastLED.setBrightness(k);
    FastLED.show();
  }
}
// fade_out-> Diminuzione graduale della luminosità

void fade_out() {
  int  k = 0;
  for (k = 130; k > 0; k--) {
    FastLED.setBrightness(k);
    FastLED.show();
  }
}

// gameOn-> Algoritmo reperito online.
// Un punto colorato scorre avanti e indietro creando una scia, sfumando e cambiando colore secondo la scala RGB

void gameOn() {
  FastLED.setBrightness(150);
  int i;
  int durata = 1500;
  long int current_millis = millis();

  while (millis() - current_millis < 5000) { //timer
    Serial.println(millis() - current_millis);
    fadeToBlackBy( leds, NUM_LEDS, 20);
    int pos = beatsin16( 13, 0, NUM_LEDS );
    leds[pos] += CHSV( gHue, 255, 192);
    FastLED.show();
    FastLED.delay(1000 / FRAMES_PER_SECOND);

    EVERY_N_MILLISECONDS( 20 ) {
      gHue++;
    }
  }
  current_millis = 0;
  fade_out();
  green_light(durata);

}

// endGame-> Spegne tutti i led con fade_out

void endGame(){ 
  fade_out();
  FastLED.clear();
  FastLED.show();
}

// green_light-> Prende in ingresso un intero (una durata in millisecondi)
// Accende per quella durata i led, per poi spegnerli per lo stesso tempo

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
