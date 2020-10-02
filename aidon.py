import time
import serial
import math
import paho.mqtt.client as mqtt
import crc16

debug = False

##############################################
# format of telegram
##############################################
N = 581 # total length
N_header = 20 # length of header
N_trailer = 3

# key : [unit divide_by]
units = {
    0x1b : ["W", 1],
    0x1d : ["VAr", 1],
    0x1e : ["kWh", 1000.0],
    0x20 : ["kVArh", 1000.0],
    0x21 : ["A", 10.0],
    0x23 : ["V", 10.0]
}

# key : nr_bytes
values = {
    0x06 : 4,
    0x10 : 2,
    0x12 : 2
}

################################################
# format strings
# obis_key : string
################################################
aidon_strings = {
    0x0107 : "Momentary active power+       = {0:4d} {1:s}\t",
    0x0207 : "Momentary active power-       = {0:4d} {1:s}\t",
    0x0307 : "Momentary reactive power+     = {0:4d} {1:s}",
    0x0407 : "Momentary reactive power-     = {0:4d} {1:s}",
    0x1f07 : "Momentary current (L1)        = {0:3.1f} {1:s}\t",
    0x3307 : "Momentary current (L2)        = {0:3.1f} {1:s}\t",
    0x4707 : "Momentary current (L3)        = {0:3.1f} {1:s}\t",
    0x2007 : "Momentary voltage (L1)        = {0:3.1f} {1:s}\t",
    0x3407 : "Momentary voltage (L2)        = {0:3.1f} {1:s}\t",
    0x4807 : "Momentary voltage (L3)        = {0:3.1f} {1:s}\t",
    0x1507 : "Momentary active power+ (L1)  = {0:4d} {1:s}\t",
    0x1607 : "Momentary active power- (L1)  = {0:4d} {1:s}\t",
    0x1707 : "Momentary reactive power+ (L1)= {0:4d} {1:s}",
    0x1807 : "Momentary reactive power- (L1)= {0:4d} {1:s}",
    0x2907 : "Momentary active power+ (L2)  = {0:4d} {1:s}\t",
    0x2a07 : "Momentary active power- (L2)  = {0:4d} {1:s}\t",
    0x2b07 : "Momentary reactive power+ (L2)= {0:4d} {1:s}",
    0x2c07 : "Momentary reactive power- (L2)= {0:4d} {1:s}",
    0x3d07 : "Momentary active power+ (L3)  = {0:4d} {1:s}\t",
    0x3e07 : "Momentary active power- (L3)  = {0:4d} {1:s}\t",
    0x3f07 : "Momentary reactive power+ (L3)= {0:4d} {1:s}",
    0x4007 : "Momentary reactive power- (L3)= {0:4d} {1:s}",
    0x0108 : "Cumulative active energy+     = {0:5.1f} {1:s}",
    0x0208 : "Cumulative active energy-     = {0:5.1f} {1:s}",
    0x0308 : "Cumulative reactive energy+   = {0:5.1f} {1:s}",
    0x0408 : "Cumulative reactive energy-   = {0:5.1f} {1:s}",
}

if not debug:
    hostname = "192.168.1.29"
    client = mqtt.Client("Aidon")
    client.username_pw_set(username="homeassistant",
                           password="eidou8poo8odaibae5Phob7ooheingo4UFaef5aecheiphie6ShaeDe0eemahY2y")
    client.connect(hostname)


ser = serial.Serial("/dev/ttyUSB0", baudrate = 115200, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=2)

etime2 = 0
while 1:
    measurements = []

    stime1 = time.time() 

    while 1:
        r = ser.read(N)
        M = len(r)
        if M==N and r[0] == 0x7e:
            break
        
    etime1 = (time.time() - stime1)
    stime2 = time.time()

    ############################
    # Header
    ############################
    if debug:
        print("\nHeader", end="\t\t\t\t\t\t")
        for i in range(N_header):
            print("{0:02x}".format(r[i]), end=" ")
    print("")

    N_lines = r[N_header-1]

    crc = crc16.crc16xmodem(r[18:-3])

    r = r[N_header:]

    ############################
    # Timestamp
    ############################
    N_timestamp = 12 + r[11]
    year = int.from_bytes(r[12:14], byteorder="big")
    month = r[14]
    day = r[15]
    hour = r[17] + 1
    min = r[18]
    sec = r[19]

    print("Timestamp: {0:4d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}".format(year, month, day, hour, min, sec), end="\t\t\t")

    if debug:
        #print("\n\nOBIS={0:d}-{1:d}:{2:d}.{3:d}.{4:d}.{5:d}".format(r[4], r[5], r[6], r[7], r[8], r[9]), end=" ")
        for i in range(N_timestamp):
            print("{0:02x}".format(r[i]), end=" ")
    print("")

    r = r[N_timestamp:] 

    ############################
    # Read 4 quadrants momentary power
    # Read 3 phases current
    # Read 3 phases voltage
    # Read 3x4 momentary powers
    # Read 4 quadrants of energy
    ############################
    for lines in range(N_lines-1):
        nr = values[r[10]]
        N_line = 11 + nr + 6
        obis = int.from_bytes(r[6:8], byteorder="big")
        fmt = aidon_strings[obis]
        
        dv = units[r[N_line-1]][1]
        un = units[r[N_line-1]][0]
        
        p = int.from_bytes(r[11:11+nr], byteorder="big", signed = False)
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
        print("Trailer", end="\t\t\t\t\t\t")
        for i in range(N_trailer):
            print("{0:02x}".format(r[i]), end=" ")
            
    print("")

    
    ############################
    # Publicera till MQTT
    ############################
    ap = measurements[0] - measurements[1]
    rp = measurements[2] - measurements[3]
    fi = 180*math.atan2(rp,ap)/math.pi

    print("Phase angle = {0:3.1f}".format(fi))

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

    etime2 = (time.time() - stime2)
    
    if debug:
        print("crc = {0:04x}".format(crc))
        print("M={0:03d} t= {1:4.1f} ms   t={2:2.1f} ms".format(M, 1000*etime1, 1000*etime2))





        

