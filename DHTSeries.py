"""Lib for DHT11, DHT21, DHT22 and AM2302

for use;

    import DHTSeries
    DHTSeries.init()
    DHTSeries.measure()

    or

    import DHTSeries as ###name_of_your_sensor : AM2302
    AM2302.init()
    AM2302.measure()

    for exemple in main.py

    import DHTSeries as AM2302
    AM2302.init()
    pyb.delay(3000)  # Time for stabilize the sensors

    while True:
        (hum, tem) = AM2302.measure()
        print("humidité : " + str(hum) + " temperature : " + str(tem))
        pyb.delay(2000)  # respect the delays between measurement
"""

import pyb
from pyb import ExtInt
from pyb import Pin

# We need to use global properties here as any allocation of a memory (aka declaration of a variable)
# during the read cycle causes non-acceptable delay and we are loosing data than
data = None
timer = None
micros = None
dhttype = 0  # 0=DHT11 1=DHT21/DHT22/AM2302

FALL_EDGES = 42  # we have 42 falling edges during data receive

times = list(range(FALL_EDGES))
index = 0


def interuptHandler(line):
    """
    The interrupt handler
    :param line:
    :return:
    """
    global index
    global times
    global micros
    times[index] = micros.counter()
    if index < (FALL_EDGES - 1):  # Avoid overflow of the buffer in case of any noise on the line
        index += 1


def init(timer_id=2, data_pin='Y2', the_dhttype='DHT22'):
    """
    Init the sensor
    :param timer_id: id of the internal Timer in pyboard
    :param data_pin: pin if you have connect the sensor
    :param the_dhttype: type of used sensor
    """
    global data
    global micros
    global timer
    global dhttype
    
    if (the_dhttype == 'DHT11'):
        dhttype = 0
    else:
        dhttype = 1
    
    # Configure the pid for data communication
    data = Pin(data_pin)
    
    # Save the ID of the timer we are going to use
    timer = timer_id
    
    # setup the 1uS timer
    micros = pyb.Timer(timer, prescaler=83, period=0x3fffffff)  # 1MHz ~ 1uS
    
    # Prepare interrupt handler
    ExtInt(data, ExtInt.IRQ_FALLING, Pin.PULL_UP, None)
    ExtInt(data, ExtInt.IRQ_FALLING, Pin.PULL_UP, interuptHandler)
    
    # Prepare start sequence
    data.high()
    pyb.delay(250)


# Start signal
def do_measurement():
    """
    Init the sensor for receive data
    """
    global data
    global micros
    global index
    
    # Send the START signal
    data.init(Pin.OUT_PP)
    data.low()
    micros.counter(0)
    while micros.counter() < 20000:
        pass
    data.high()
    micros.counter(0)
    while micros.counter() < 30:
        pass
    
    # Activate reading on the data pin
    index = 0
    data.init(Pin.IN, Pin.PULL_UP)
    # Till 5mS the measurement must be over
    pyb.delay(5)


def process_data():
    """
    Parse the data read from the sensor
    :return: value of humidity and temperature
    """
    global dhttype
    global times
    
    i = 2  # We ignore the first two falling edges as it is a respomse on the start signal
    result_i = 0
    result = list([0, 0, 0, 0, 0])
    while i < FALL_EDGES:
        result[result_i] <<= 1
        if times[i] - times[i - 1] > 100:
            result[result_i] += 1
        if (i % 8) == 1:
            result_i += 1
        i += 1
    [int_rh, dec_rh, int_t, dec_t, csum] = result
    
    if dhttype == 0:  # dht11
        humidity = int_rh  # dht11 20% ~ 90%
        temperature = int_t  # dht11 0..50°C
    else:  # dht21,dht22,AM2302
        humidity = ((int_rh * 256) + dec_rh) / 10
        temperature = (((int_t & 0x7F) * 256) + dec_t) / 10
        if (int_t & 0x80) > 0:
            temperature *= -1
    
    comp_sum = int_rh + dec_rh + int_t + dec_t
    if (comp_sum & 0xFF) != csum:
        raise ValueError('Checksum does not match')
    return (humidity, temperature)


def measure():
    do_measurement()
    if index != (FALL_EDGES - 1):
        raise ValueError('Data transfer failed: %s falling edges only' % str(index))
    return process_data()
