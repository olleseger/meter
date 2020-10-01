import time
import serial
import paho.mqtt.client as mqtt

debug = False

if not debug:
    hostname = "192.168.1.29"
    client = mqtt.Client("Aidon")
    client.username_pw_set(username="homeassistant",password="eidou8poo8odaibae5Phob7ooheingo4UFaef5aecheiphie6ShaeDe0eemahY2y")
    client.connect(hostname)

##############################################
# format of telegram
##############################################
N = 581 # total length
N_header = 20 # length of header
N_timestamp = 24 # length of timestamp
N_line1 = 21
N_line2 = 19
N_trailer = 3

ser = serial.Serial("/dev/ttyUSB0", baudrate = 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=2)

etime2 = 0
while 1:
    measurements = []
    M=0
    while M<N:
        stime1 = time.time() 
        r = ser.read(N)
        etime1 = (time.time() - stime1)
        M = len(r)

    if debug:
        print("\n\nM={0:03d} t= {1:f} ms   t={2:f} ms".format(M, 1000*etime1, 1000*etime2))

    stime2 = time.time()

    ############################
    # Header
    ############################
    l = r[:N_header]
    r = r[N_header:]

    if debug:
        print("\nHeader", end="\t\t\t\t\t")
        for i in range(N_header):
            print("{0:02x}".format(l[i]), end=" ")
    print("")
    
    ############################
    # Timestamp
    ############################
    l = r[:N_timestamp]
    r = r[N_timestamp:] 

    year = int.from_bytes(l[12:14], byteorder="big")
    month = l[14]
    day = l[15]
    hour = l[17] + 1
    min = l[18]
    sec = l[19]

    print("Timestamp: {0:4d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}".format(year, month, day, hour, min, sec), end="\t\t")

    if debug:
        #print("\n\nOBIS={0:d}-{1:d}:{2:d}.{3:d}.{4:d}.{5:d}".format(l[4], l[5], l[6], l[7], l[8], l[9]), end=" ")
        for i in range(N_timestamp):
            print("{0:02x}".format(l[i]), end=" ")
    print("")

    ############################
    # Read 4 quadrants momentary power
    ############################
    for quad in range(4):
        l = r[:N_line1]
        r = r[N_line1:]

        p = int.from_bytes(l[13:15], byteorder="big")
        measurements.append(p)
        
        print("Momentary power {0:d}=      {1:4d} W".format(quad+1, p), end="\t\t")

        if debug:
            #print("\n\nOBIS={0:d}-{1:d}:{2:d}.{3:d}.{4:d}.{5:d}".format(l[4], l[5], l[6], l[7], l[8], l[9]), end=" ")
            for i in range(N_line1):
                print("{0:02x}".format(l[i]), end=" ")
        print("")
        
    ############################
    # Read 3 phases current
    ############################
    for phase in range(3):
        l = r[:N_line2]
        r = r[N_line2:]

        v = int.from_bytes(l[11:13], byteorder="big")/10.0
        measurements.append(v)
    
        print("Momentary current (L{0:d})=    {1:3.1f} A".format(phase+1, v), end="\t")

        if debug:
            #print("\n\nOBIS={0:d}-{1:d}:{2:d}.{3:d}.{4:d}.{5:d}".format(l[4], l[5], l[6], l[7], l[8], l[9]), end=" ")
            for i in range(N_line2):
                print("{0:02x}".format(l[i]), end=" ")
        print("")
        
    ############################
    # Read 3 phases voltage
    ############################
    for phase in range(3):
        l = r[:N_line2]
        r = r[N_line2:]

        v = int.from_bytes(l[11:13], byteorder="big")/10.0
        measurements.append(v)
    
        print("Momentary voltage (L{0:d})=    {1:3.1f} V".format(phase+1, v), end="\t")

        if debug:
            #print("\n\nOBIS={0:d}-{1:d}:{2:d}.{3:d}.{4:d}.{5:d}".format(l[4], l[5], l[6], l[7], l[8], l[9]), end=" ")
            for i in range(N_line2):
                print("{0:02x}".format(l[i]), end=" ")
        print("")
        
    ############################
    # Read 3x4 momentary powers
    ############################
    for phase in range(3):
        for quad in range(4):
            l = r[:N_line1]
            r = r[N_line1:]

            p = int.from_bytes(l[13:15], byteorder="big")
            measurements.append(p)
            
            print("Momentary power {0:d} (L{1:d})=   {2:4d} W".format(quad+1, phase+1, p), end="\t")

            if debug:
                #print("\n\nOBIS={0:d}-{1:d}:{2:d}.{3:d}.{4:d}.{5:d}".format(l[4], l[5], l[6], l[7], l[8], l[9]), end=" ")
                for i in range(N_line1):
                    print("{0:02x}".format(l[i]), end=" ")
            print("")
            
    ############################
    # Read 4 quadrants of energy
    ############################
    for quad in range(4):
        l = r[:N_line1]
        r = r[N_line1:]

        e = int.from_bytes(l[12:15], byteorder="big")/1000.0
        measurements.append(e)
        
        print("Cumulative energy {0:d}=       {1:5.1f} kWh".format(quad+1, e), end="\t")

        if debug:
            #print("\n\nOBIS={0:d}-{1:d}:{2:d}.{3:d}.{4:d}.{5:d}".format(l[4], l[5], l[6], l[7], l[8], l[9]), end=" ")
            for i in range(N_line1):
                print("{0:02x}".format(l[i]), end=" ")
        print("")
        
    ############################
    # Trailer
    ############################
    l= r

    if debug:
        print("Trailer", end="\t\t\t\t\t")
        for i in range(N_trailer):
            print("{0:02x}".format(l[i]), end=" ")

    
    print("")
    etime2 = (time.time() - stime2)
    
    ############################
    # Publicera till MQTT
    ############################
    if not debug:
        client.publish("meter/activepower", measurements[0])
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




        

