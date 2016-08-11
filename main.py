import pyb
import DHTSeries as AM2302


print("start program")

AM2302.init()
pyb.delay(3000)  # Time for stabilize the sensors

while True:
    (hum, tem) = AM2302.measure()
    print("humidité : " + str(hum) + " temperature : " + str(tem))
    pyb.delay(2000)  # respect the delays between measurement
