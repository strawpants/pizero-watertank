import RPi.GPIO as GPIO
import sys
import time

sockettop_ctrlpin=6
socketlow_ctrlpin=5

def airpump_ctrl(switchOn=True,pin=socketlow_ctrlpin):
    if switchOn:
        print("starting airpump")
        GPIO.output(pin, GPIO.LOW)
    else:
        print("stopping airpump")
        GPIO.output(pin, GPIO.HIGH)

def waterpump_ctrl(switchOn=True,pin=sockettop_ctrlpin):
    if switchOn:
        print("starting waterpump")
        GPIO.output(pin, GPIO.LOW)
    else:
        print("stopping waterpump")
        GPIO.output(pin, GPIO.HIGH)


def set_up():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sockettop_ctrlpin, GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(socketlow_ctrlpin, GPIO.OUT,initial=GPIO.HIGH)

def main():
    set_up()
    waterpump_ctrl(True)
    
    while True:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            waterpump_ctrl(False)
            print("KeyboardInterrupt, shutting down pump")
            GPIO.cleanup()
            sys.exit(0)


if __name__ == "__main__":
    main()
