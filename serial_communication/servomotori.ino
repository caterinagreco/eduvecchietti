#define PIN_CODA 9
#define PIN_ZAMPE 10

void   initServo()
{
  myservo_coda.attach(PIN_CODA);  // attaches the servo on pin 9 to the servo object
  myservo_coda.write(0,255,true); // set the intial position of the servo, as fast as possible, wait until done

  myservo_zampe.attach(PIN_ZAMPE);  // attaches the servo on pin 10 to the servo object
  myservo_zampe.write(0,255,true); // set the intial position of the servo, as fast as possible, wait until done

}

void muoviCoda(){
  int i=0;
  for(i=0;i<4;i++){
    myservo_coda.write(60,100,true);        // move the servo to 180, max speed, wait until done                                      // write(degrees 0-180, speed 1-255, wait to complete true-false)
    myservo_coda.write(0,100,true);           // move the servo to 180, slow speed, wait until done    
  }
}

void muoviZampe(){
  int i=0;
  for(i=0;i<4;i++){
    myservo_zampe.write(50,100,true);        // move the servo to 180, max speed, wait until done                                      // write(degrees 0-180, speed 1-255, wait to complete true-false)
    myservo_zampe.write(0,100,true);           // move the servo to 180, slow speed, wait until done    
  }
}
