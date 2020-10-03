import serial
import time
import math
import libscrc
import telegram
import paho.mqtt.client as mqtt
debug = False

if not debug:
    hostname = "192.168.1.29"
    client = mqtt.Client("Aidon")
    client.username_pw_set(username="homeassistant",
                           password="eidou8poo8odaibae5Phob7ooheingo4UFaef5aecheiphie6ShaeDe0eemahY2y")
    client.connect(hostname)

    ser = serial.Serial("/dev/ttyUSB0", baudrate = 115200, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=2)

while True:
    measurements = []

    if debug:
        r = telegram.telegram
    else:
        while True:
            r = ser.read(telegram.N)
            M = len(r)
            if M == telegram.N:
                break

    if r[0] == 0x7e and r[-1] == 0x7e:
        print("Flags OK!")
        
    crc = libscrc.ibm(r[18:-3])
    crc_sent = int.from_bytes(r[0:2], byteorder="big")
    print("crc sent: {0:04x}  crc received: {1:04x}".format(crc_sent, crc), end="\t\t")

    ############################
    # Header
    ############################
    if debug:
        print("\nHeader", end="\t\t\t\t\t\t")
        for i in range(telegram.N_header):
            print("{0:02x}".format(r[i]), end=" ")
    print("")

    N_lines = r[telegram.N_header-1]

    r = r[telegram.N_header:]

    ############################
    # Read Timestamp
    # Read 4 quadrants momentary power
    # Read 3 phases current
    # Read 3 phases voltage
    # Read 3x4 momentary powers
    # Read 4 quadrants of energy
    ############################
    for lines in range(N_lines):
        obis = int.from_bytes(r[4:8], byteorder="big")
        fmt = telegram.aidon_strings[obis]

        if fmt[:9] == "Timestamp":
            N_line = 12 + r[11]

            year = int.from_bytes(r[12:14], byteorder="big")
            month = r[14]
            day = r[15]
            hour = r[17] + 1
            min = r[18]
            sec = r[19]
            print(fmt.format(year, month, day, hour, min, sec), end="\t")
        else:
            key = r[10]
            nr = telegram.values[key][0]
            pm = telegram.values[key][1]
            
            N_line = 11 + nr + 6

            key = r[N_line-1]
            dv = telegram.units[key][1]
            un = telegram.units[key][0]
        
            p = int.from_bytes(r[11:11+nr], byteorder="big", signed = pm)
            if dv != 1:
                p = p/dv
                
            measurements.append(p)
            print(fmt.format(p, un), end="\t")

        if debug:
            #print("\n\nOBIS={0:d}-{1:d}:{2:d}.{3:d}.{4:d}.{5:d}".format(r[4], r[5], r[6], r[7], r[8], r[9]), end=" ")
            for i in range(N_line):
                print("{0:02x}".format(r[i]), end=" ")
        print("")
        
        r = r[N_line:]
            
    ############################
    # Trailer
    ############################
    if debug:
        time.sleep(10.0)
            
    
    ############################
    # Publicera till MQTT
    ############################
    ap = measurements[0] - measurements[1]
    rp = measurements[2] - measurements[3]
    fi = 180*math.atan2(rp,ap)/math.pi

    print("")

    if not debug:
        client.publish("meter/activepower", ap)
        client.publish("meter/reactivepower", rp)
        client.publish("meter/fi", fi)
        
        client.publish("meter/current1", measurements[4])
        client.publish("meter/current2", measurements[5])
        client.publish("meter/current3", measurements[6])

        client.publish("meter/voltage1", measurements[7])
        client.publish("meter/voltage2", measurements[8])
        client.publish("meter/voltage3", measurements[9])

        client.publish("meter/activepower1", measurements[10])
        client.publish("meter/activepower2", measurements[14])
        client.publish("meter/activepower3", measurements[18])
        
        client.publish("meter/activeenergy", measurements[22])






        

