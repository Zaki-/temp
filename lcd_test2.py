from time import sleep
import sys
# make sure Adafruit_CharLCD is in the path
sys.path.append('/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCD')
from Adafruit_CharLCD import Adafruit_CharLCD
# instantiate lcd and specify pins
lcd = Adafruit_CharLCD(pin_rs=26, pin_e=19, pins_db=[13, 6, 5, 11])
lcd.clear()
# specify columns and rows
lcd.begin(16,2)
# display text on LCD display \n = new line
lcd.message('Adafruit CharLCD\n  Raspberry Pi')
sleep(3)
# scroll text off display
for x in range(0, 16):
    lcd.scrollDisplayRight()
    sleep(.1)
sleep(3)
# scroll text on display
for x in range(0, 16):
    lcd.DisplayLeft()
    sleep(.1)
