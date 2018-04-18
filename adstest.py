import time
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

while True:
    values = adc.read_adc(3, gain=GAIN)
    if values > 5000:
        print "Fire detected...."
	time.sleep(2.0)
    time.sleep(0.5)
