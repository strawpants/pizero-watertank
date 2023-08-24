import RPi.GPIO as GPIO
import sys
import time

usleep = lambda x: time.sleep(x*1e-6)

#tstart=0
#tend=0

#def set_tstart(pin):
#    print("set tstart")
#    tstart= time.time()

#def set_tend(pin):
#    print("set tend")
#    tend= time.time()
_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

def getdistance(pin,speedofsound=340):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,GPIO.LOW)
        usleep(2)
        GPIO.output(pin,GPIO.HIGH)
        usleep(10)
        GPIO.output(pin,GPIO.LOW)
        GPIO.setup(pin, GPIO.IN)

        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if GPIO.input(pin):
                break
            count += 1
        if count >= _TIMEOUT1:
            return None,None

        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not GPIO.input(pin):
                break
            count += 1
        if count >= _TIMEOUT2:
            return None,None

        t2 = time.time()

        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None,None


        return t2-t1,(t2-t1)*speedofsound/2


#def getdistance(pin,speedofsound=340):
    #set gpio pin as putput staring with low
#    GPIO.setup(pin, GPIO.OUT)
    #usleep(2)
#    GPIO.output(pin,GPIO.LOW)
    
#    usleep(2)
    # send a 10 microsecond pulse to start a measurement
#    GPIO.output(pin,GPIO.HIGH)
#    usleep(12)
#    GPIO.output(pin,GPIO.LOW)
    
    #now the same pin is used to receive the observation as a pulse (where the length of the pulse is the measurement
#    GPIO.setup(pin, GPIO.IN)
#    risedetect = GPIO.wait_for_edge(pin, GPIO.RISING,timeout=200)
#    tstart=time.time()        
    
#    if risedetect == None:
#        print("timeout on transmit encountered")
#        return None,None


#    falldetect = GPIO.wait_for_edge(pin, GPIO.FALLING, timeout=100)
#    tend=time.time()        
    
#    if falldetect == None:
#        print("timeout on receive encountered")
#        return None,None

    #return travel time a
#    dt=tend-tstart
#    return dt,speedofsound*dt/2


def set_up(pin):
    GPIO.setmode(GPIO.BCM)
    time.sleep(1)

def main():
    signalpin=24
    set_up(signalpin)
    while True:
        try:
            dt,dist=getdistance(signalpin)
            if dt == None:
                print("Failed measurement")
            else:
                print(f"travel time {dt}, distance {1e2*dist} cm")
            time.sleep(2)
        except KeyboardInterrupt:
            GPIO.cleanup()

            print("KeyboardInterrupt")
            sys.exit(0)


if __name__ == "__main__":
    main()
