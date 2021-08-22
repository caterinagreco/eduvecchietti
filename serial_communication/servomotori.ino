#define PIN_CODA 9
// #define PIN_ZAMPE 10

//ATTENZIONE->in servoCorrect ho scritto 15 invece che 5 come posizione

// initServo-> Indirizza il pin al quale è collegato il serovmotore
// e lo setta nella posizione di riposo di 45 gradi

void   initServo()
{
  myservo_coda.attach(PIN_CODA);  
  myservo_coda.write(45, 255, true); 
}

// servoCorrect()-> Sposta il servomotore a destra di 40 gradi rispetto
// alla posizione di riposo e poi di 40 a sinistra rispetto alla posizione di riposo
// per poi tornare a 45 gradi

void servoCorrect() {
  int i = 0;
  for (i = 0; i < 2; i++) {

    myservo_coda.write(85, 150, true); 
    delay(100);
    myservo_coda.write(15, 150, true); 
    delay(100);
  }
 
  myservo_coda.write(45, 150, true); 
}

// servoVictory-> Esegue per 4 volte lo stesso movimento di servoCorrect

void servoVictory() { 
  int i = 0;
  for (i = 0; i < 4; i++) {
    myservo_coda.write(85, 150, true);
    delay(100);
    myservo_coda.write(5, 150, true);
    delay(100);
  }
  myservo_coda.write(45, 150, true);
}
