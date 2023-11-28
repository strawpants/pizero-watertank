#!/usr/bin/env python
import RPi.GPIO as GPIO
import sys
import time

millisleep = lambda x: time.sleep(x*1e-3)

def waitfortip(pin):
    riseDetected=GPIO.wait_for_edge(pin, GPIO.RISING,timeout=10*60*1000)
    if riseDetected is None:
        return False
    millisleep(333)
    return True

def set_up(pin):
    print("Setup tipping bucket")
    GPIO.setmode(GPIO.BCM)
    time.sleep(1)
    GPIO.setup(pin, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)

def main():
    bucketpin=10
    set_up(bucketpin)
    tips=0
    while True:
        try:
            print("waiting for tip event")
            tipevent=waitfortip(bucketpin)
            if tipevent:
                tips+=1
                print(f"tip detected: total tips since start {tips}")
            else:
                print("wait for edge timed out")
        except KeyboardInterrupt:
            GPIO.cleanup()

            print("KeyboardInterrupt")
            sys.exit(0)


if __name__ == "__main__":
    main()
