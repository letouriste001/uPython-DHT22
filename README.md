uPython-DHT22
=============

This module provides a device driver for DHT22 (or DHT11 or AM2302) sensors on microPython board.

You can check more about these temperature and humidity sensors at the following page: http://www.adafruit.com/products/385

You can check more about the microPython project here: http://micropython.org/

Wiring
------

The basic wiring is designed to use no additional parts (like a pull-up resistor) and can be directly put to the microPython board.
The wiring:

```
Sensor pin | board pin
-----------+----------
    VDD    |    3.3v
    DTA    |    Y2
    GND    |    GND
```

Installation
------------
There are two files:
* DHTSeries.py - the module implementing communication with the sensor

The simplest installation way is to follow these steps (Linux):

1. Connect your microPython board to your PC using a USB cable
2. Mount the device pointing to the board (/dev/sdb1 in my case)
  ```
  mkdir ~/tmp
  sudo mount /dev/sdb1 ~/tmp
  ```
3. copy DHTSeries.py and main.py files to the board
  ```
  sudo cp DHTSeries.py main.py ~/tmp
  ```
4. Unmount the device
  ```
  sudo umount ~/tmp
  ```
5. Restart your microPython board

