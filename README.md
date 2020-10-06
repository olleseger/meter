# Aidon 6534

## Software for reading of the Aidon 6534 meter. 

## Things needed
- A Raspberry Pi 4
- A [USB-serial cable](https://www.kjell.com/se/produkter/el-verktyg/arduino/moduler/luxorparts-usb-till-seriell-adapter-for-arduino-p88064)
- A 10 k resistor
- The program `ft232r_prog` for reprogramming the FTDI chip on the USB-serial cable.

## Connecting the RaspberryPi to the  Aidon 6534
Connect the Raspberry Pi to a USB-serial cable. 
Then connect an RJ12 cable to the USB-serial cable:

| Aidon-RJ12       |  USB-serial cable  |
| ----             | ----           |
| 1 - 5V           |                |
| 2 - RTS          | 5V             |
| 3 - GND          | GND            |
| 4 -              |                |
| 5 - Data         | RxD            |
| 6 - GND          |                |

A 10k resistor is connected between 5V and RxD on the FTDI. The RxD input on the USB-serial cable is inverted with the program `ft232r_prog`.
Aidon uses `115200,8N1` serial communication. The `Data` output is `open collector` and inverted.

## Running the program
Run the program by:
```python
python3 aidon3.py
```

If you run the program with the debug flag:
```python
python3 aidon3.py -d
```
you get this printout. It is the example in [Aidon](dokument/Aidon.pdf):
```bash
debug
Flags OK! first=last= 0x7e
Length OK! from header=received= 579
CRC OK! calculated=sent= 0x40be
Package length =  579
Nr of registers =   27

Flag:                                           7e 
Header:                                         a2 43 41 08 83 13 85 eb e6 e7 00 0f 40 00 00 00 00 01 1b 
Timestamp: 2019-12-16 08:59:40                  02 02 09 06 00 00 01 00 00 ff 09 0c 07 e3 0c 10 01 07 3b 28 ff 80 00 ff 
Momentary active power+       = 1122 W          02 03 09 06 01 00 01 07 00 ff 06 00 00 04 62 02 02 0f 00 16 1b 
Momentary active power-       =    0 W          02 03 09 06 01 00 02 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1b 
Momentary reactive power+     = 1507 VAr        02 03 09 06 01 00 03 07 00 ff 06 00 00 05 e3 02 02 0f 00 16 1d 
Momentary reactive power-     =    0 VAr        02 03 09 06 01 00 04 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1d 
Momentary current (L1)        = 0.0 A           02 03 09 06 01 00 1f 07 00 ff 10 00 00 02 02 0f ff 16 21 
Momentary current (L2)        = 7.5 A           02 03 09 06 01 00 33 07 00 ff 10 00 4b 02 02 0f ff 16 21 
Momentary current (L3)        = 0.0 A           02 03 09 06 01 00 47 07 00 ff 10 00 00 02 02 0f ff 16 21 
Momentary voltage (L1)        = 230.7 V         02 03 09 06 01 00 20 07 00 ff 12 09 03 02 02 0f ff 16 23 
Momentary voltage (L2)        = 249.9 V         02 03 09 06 01 00 34 07 00 ff 12 09 c3 02 02 0f ff 16 23 
Momentary voltage (L3)        = 230.8 V         02 03 09 06 01 00 48 07 00 ff 12 09 04 02 02 0f ff 16 23 
Momentary active power+ (L1)  =    0 W          02 03 09 06 01 00 15 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1b 
Momentary active power- (L1)  =    0 W          02 03 09 06 01 00 16 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1b 
Momentary reactive power+ (L1)=    0 VAr        02 03 09 06 01 00 17 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1d 
Momentary reactive power- (L1)=    0 VAr        02 03 09 06 01 00 18 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1d 
Momentary active power+ (L2)  = 1122 W          02 03 09 06 01 00 29 07 00 ff 06 00 00 04 62 02 02 0f 00 16 1b 
Momentary active power- (L2)  =    0 W          02 03 09 06 01 00 2a 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1b 
Momentary reactive power+ (L2)= 1506 VAr        02 03 09 06 01 00 2b 07 00 ff 06 00 00 05 e2 02 02 0f 00 16 1d 
Momentary reactive power- (L2)=    0 VAr        02 03 09 06 01 00 2c 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1d 
Momentary active power+ (L3)  =    0 W          02 03 09 06 01 00 3d 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1b 
Momentary active power- (L3)  =    0 W          02 03 09 06 01 00 3e 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1b 
Momentary reactive power+ (L3)=    0 VAr        02 03 09 06 01 00 3f 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1d 
Momentary reactive power- (L3)=    0 VAr        02 03 09 06 01 00 40 07 00 ff 06 00 00 00 00 02 02 0f 00 16 1d 
Cumulative active energy+     = 10049.9 kWh     02 03 09 06 01 00 01 08 00 ff 06 00 99 59 86 02 02 0f 00 16 1e 
Cumulative active energy-     =   0.0 kWh       02 03 09 06 01 00 02 08 00 ff 06 00 00 00 08 02 02 0f 00 16 1e 
Cumulative reactive energy+   = 6614.3 kVArh    02 03 09 06 01 00 03 08 00 ff 06 00 64 ed 4b 02 02 0f 00 16 20 
Cumulative reactive energy-   =   0.0 kVArh     02 03 09 06 01 00 04 08 00 ff 06 00 00 00 05 02 02 0f 00 16 20 
CRC:                                            40be
Flag:                                           7e
```
As can clearly be seen this is not ASCII!

## Data Sent

The software publishes the following MQTT topics:

```
meter/activepower
meter/activepower1
meter/activepower2
meter/activepower3
meter/voltage1
meter/voltage2
meter/voltage3
meter/current1
meter/current2
meter/current3
meter/activeenergy
```

## Home asssistant configuration
Put this in a `.yaml` file:
```
sensor:
  - platform: mqtt
    state_topic: "meter/activepower"
    name: "Active Power"
    unit_of_measurement: "W"
#
# and so on
```


![bild](bilder/Homeassistant.JPG)





