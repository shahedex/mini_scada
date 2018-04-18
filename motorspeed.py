import RPi.GPIO as GPIO # import GPIO librery
import time
import Adafruit_ADS1x15
from time import sleep
import pymssql

motor_speed = 0;
gas_data = 0;
valve_cond = 0;
water_level = 0;

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

def gas_data():
    values = adc.read_adc(3, gain=GAIN)
    if values > 5000:
        print "Fire detected...."
	time.sleep(2.0)
    time.sleep(0.5)

def start_motor(speeds):
    GPIO.setmode(GPIO.BCM)
    Motor1A = 20 # set GPIO-02 as Input 1 of the controller IC
    Motor1B = 16 # set GPIO-03 as Input 2 of the controller IC
    Motor1E = 21 # set GPIO-04 as Enable pin 1 of the controller IC
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)
    pwm=GPIO.PWM(21,100) # configuring Enable pin means GPIO-04 for PWM
    pwm.start(speeds) # starting it with 50% dutycycle
    print "GO forward"
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    time.sleep(5.0)
##    pwm.ChangeDutyCycle(speeds) # increasing dutycycle to 80
##    GPIO.output(Motor1A,GPIO.HIGH)
##    GPIO.output(Motor1B,GPIO.LOW)
##    GPIO.output(Motor1E,GPIO.HIGH)
##    time.sleep(4.0)
    #pwm.stop() # stop PWM from GPIO output it is necessary
    GPIO.cleanup()

def data_fetch():
    try:
        conn = pymssql.connect("116.193.220.12", "apu", "Sel12345", "cuet_meter")
        cursor = conn.cursor()
        cursor.execute("select * from Persons")
        for row in cursor:
            print(row)
            global motor_speed
            motor_speed = row[2]
    except Exception as e:
        print(e)
if __name__ == "__main__":
    while True:
        data_fetch()
        if int(motor_speed)<100:
            start_motor(5)
        elif int(motor_speed)>100 and int(motor_speed)<200:
            start_motor(10)
        elif int(motor_speed)>200:
            start_motor(80)
        #time.sleep(1.0)