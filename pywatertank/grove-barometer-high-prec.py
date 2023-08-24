from hp206c import hp206c
import sys
import time




def main():
    pres_temp=hp206c()

    ret=pres_temp.isAvailable()
    if pres_temp.OK_HP20X_DEV == ret:
            print("Barometer is available.")
    else:
            print("Barometer isn't available.")
            sys.exit(-1)
    
    while True:
        try:
            pres=pres_temp.ReadPressure()
            temp=pres_temp.ReadTemperature()
            alt=pres_temp.ReadAltitude()
            print(f"Pressure: {pres} HPa,Temperature {temp} (deg C), 'Altitude' {alt} (m above ellipsoid)")
            time.sleep(3)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            sys.exit(0)


if __name__ == "__main__":
    main()
