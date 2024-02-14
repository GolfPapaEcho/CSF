import time
import csv
from datetime import datetime
from os import path
import smbus2
start = time.time()
bus = smbus2.SMBus(20)
ADDRESS = 0x18
buffer = bytearray(5)




def read_pressure(YOUR_ADDRESS):
    #bus.write_byte(YOUR_ADDRESS, 0x30)
    bus.write_byte(YOUR_ADDRESS, 0xAA)
    bus.write_byte(YOUR_ADDRESS, 0)
    bus.write_byte(YOUR_ADDRESS, 0)
    time.sleep(0.008)
    buffer[4] = bus.read_byte(YOUR_ADDRESS)
    buffer[3] = bus.read_byte(YOUR_ADDRESS)
    buffer[2] = bus.read_byte(YOUR_ADDRESS)
    buffer[1] = bus.read_byte(YOUR_ADDRESS)
    buffer[0] = bus.read_byte(YOUR_ADDRESS)
    return buffer

try:
    while True:
        now = datetime.now()
        dTString = now.strftime("%d.%m.%Y.%H:%M:%S")
        fileName = path.expanduser("~/Pressure/" + "CSFPressure" + dTString + ".csv")
        with open(fileName, 'w') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['TimeB4Measurement/s', 'TimeAfterMeasurement/s', 'Pressure/Counts'])
            for i in range(1000):
                timeB4Measuremnt = time.time()
                presscounts = read_pressure(ADDRESS)
                timeAfterMeasurement = time.time()
                writer.writerow([timeB4Measuremnt, timeAfterMeasurement, presscounts])
                print(presscounts)
            f.close()
        end = time.time()
        print("run time = :", (end-start))
except KeyboardInterrupt:
    f.close()
    end = time.time()
    print("run time = :", (end-start))
    print('\n', "Exit on Ctrl-C: Good bye!")

except:
    f.close()
    print("Other error or exception occurred!, csv closed")
    raise

finally:
    print("Goodbye")
