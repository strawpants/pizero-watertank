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


def set_up():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sockettop_ctrlpin, GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(socketlow_ctrlpin, GPIO.OUT,initial=GPIO.HIGH)

def main():
    set_up()
    airpump_ctrl(True)
    
    while True:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            airpump_ctrl(False)
            print("KeyboardInterrupt, shutting down airpump")
            GPIO.cleanup()
            sys.exit(0)


if __name__ == "__main__":
    main()
