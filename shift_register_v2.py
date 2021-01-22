#!/usr/bin/env python

import RPi.GPIO as GPIO   # um die Pins ansteuern zu koennen, brauchen wir die Lib
import time             # fuer die Delays benoetigen wir die time-Lib
#GPIO.setwarnings(False)   # Keine Warnungen anzeigen

#SER = 4
#SCK = 5
#RCK = 6
#
# BOARD MODE
#

SER = 29 
SCK = 31 
RCK = 7

GPIO.setmode(GPIO.BOARD)      # Programmiermodus, um die Pins zu setzen

elapsed = 0.05

GPIO.setup(SER,GPIO.OUT)      # Setze Pin 4 als Ausgang (SER)
GPIO.setup(SCK,GPIO.OUT)      # Setze Pin 5 als Ausgang (SCK)
GPIO.setup(RCK,GPIO.OUT)      # Setze Pin 6 als Ausgang (RCK)

while 1:                # unendliche Schleife
    for y in range(8):  # Schleife wird 8Mal (8bit) ausgefuehrt
        GPIO.output(SER,1)  # eine 1 an den seriellen Input senden
        time.sleep( elapsed ) # 100ms warten
        GPIO.output(SCK,1)  # SCK-Pin auf High ziehen, damit das Register anfaengt die Bits um eine Stelle zu verschieben
        time.sleep( elapsed ) # 100ms warten
        GPIO.output(SCK,0)  # SCK_Pin wieder auf LOW ziehen
        GPIO.output(SER,0)  # Das Datenpin loeschen
        GPIO.output(RCK,1)  # RCK auf HIGH setzen, damit das Register zur Ausgabe kopiert wird
        time.sleep( elapsed ) # 100ms warten
        GPIO.output(RCK,0)  # RCK wieder auf LOW setzen

    for y in range(8):  # Schleife wird 8Mal (8bit) ausgefuehrt
        GPIO.output(SER,0)  # eine 0 an den seriellen Input senden
        time.sleep( elapsed ) # 100ms warten
        GPIO.output(SCK,1)  # SCK-Pin auf High ziehen, damit das Register anfaengt die Bits um eine Stelle zu verschieben
        time.sleep( elapsed ) # 100ms warten
        GPIO.output(SCK,0)  # SCK_Pin wieder auf LOW ziehen
        GPIO.output(SER,0)  # Das Datenpin loeschen -> eine 0 senden
        GPIO.output(RCK,1)  # RCK auf HIGH setzen, damit das Register zur Ausgabe kopiert wird
        time.sleep( elapsed ) # 100ms warten
        GPIO.output(RCK,0)  # RCK wieder auf LOW setzen
