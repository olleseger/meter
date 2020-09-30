import time
import serial
import paho.mqtt.client as mqtt

hostname = "192.168.1.29"

client = mqtt.Client("Aidon")
client.username_pw_set(username="homeassistant",password="eidou8poo8odaibae5Phob7ooheingo4UFaef5aecheiphie6ShaeDe0eemahY2y")
client.connect(hostname)

N = 581

ser = serial.Serial("/dev/ttyUSB0", baudrate = 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=2)

etime2 = 0
while 1:
    M=0
    while M<N:
        stime1 = time.time() 
        r = ser.read(N)
        etime1 = (time.time() - stime1)
        M = len(r)
    
    print("\n\nM={0:03d} t= {1:f} ms   t={2:f} ms".format(M, 1000*etime1, 1000*etime2))

    stime2 = time.time() 
    for i in range(len(r)):
        if i<10:
            if r[i]== 0x7e and r[i+1]==0xa2 and r[i+2]==0x43:
                print("\nHeader", end="\t\t\t\t\t\t")
        elif r[i]==2 and r[i+1]==2 and r[i+2]==9 and r[i+3]==6:
            #print("\n\nOBIS={0:d}-{1:d}:{2:d}.{3:d}.{4:d}.{5:d}".format(r[i+4],r[i+5],r[i+6],r[i+7],r[i+8],r[i+9]), end=" ")
            print("")
            year = 256*r[i+12] + r[i+13]
            month = r[i+14]
            day = r[i+15]
            hour = r[i+17] + 1
            min = r[i+18]
            sec = r[i+19]
            print("Timestamp: {0:4d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}".format(year, month, day, hour, min, sec), end="\t\t\t")
        elif r[i]==2 and r[i+1]==3:
            #print("\n\nOBIS={0:d}-{1:d}:{2:d}.{3:d}.{4:d}.{5:d}".format(r[i+4],r[i+5],r[i+6],r[i+7],r[i+8],r[i+9]), end="  ")
            print("")
            if r[i+6]==1 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary Active power+ (Q1+Q4)=  {0:4d} W".format(p), end="\t")
                client.publish("meter/activepower", p)
            elif r[i+6]==2 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary Active power- (Q2+Q3)=  {0:4d} W".format(p), end="\t")
            elif r[i+6]==3 and r[i+7]==7:
                q = 256*r[i+13] + r[i+14]
                print("Momentary Reactive power+ (Q1+Q2)={0:4d} VAr".format(q), end="\t")
            elif r[i+6]==4 and r[i+7]==7:
                q = 256*r[i+13] + r[i+14]
                print("Momentary Reactive power- (Q3+Q4)={0:4d} VAr".format(q), end="\t")
            elif r[i+6]==1 and r[i+7]==8:
                e = (65536.0*r[i+12] + 256.0*r[i+13] + 1.0*r[i+14])/1000.0
                print("Cumulative active energy+ =        {0:5.1f} kWh".format(e), end="\t")
                client.publish("meter/activeenergy", e)
            elif r[i+6]==2 and r[i+7]==8:
                e = (65536.0*r[i+12] + 256.0*r[i+13] + 1.0*r[i+14])/1000.0
                print("Cumulative active energy- =        {0:5.1f} kWh".format(e), end="\t")
            elif r[i+6]==3 and r[i+7]==8:
                e = (65536.0*r[i+12] + 256.0*r[i+13] + 1.0*r[i+14])/1000.0
                print("Cumulative reactive energy+ =      {0:5.1f} kVArh".format(e), end="\t")
            elif r[i+6]==4 and r[i+7]==8:
                e = (65536.0*r[i+12] + 256.0*r[i+13] + 1.0*r[i+14])/1000.0
                print("Cumulative reactive energy- =      {0:5.1f} kVArh".format(e), end="\t")
            elif r[i+6]==32 and r[i+7]==7:
                v = (256.0*r[i+11] + 1.0*r[i+12])/10.0
                print("Momentary RMS phase voltage L1=    {0:3.1f} V".format(v), end="\t")
                client.publish("meter/voltage1", v)
            elif r[i+6]==52 and r[i+7]==7:
                v = (256.0*r[i+11] + 1.0*r[i+12])/10.0
                print("Momentary RMS phase voltage L2=    {0:3.1f} V".format(v), end="\t")
                client.publish("meter/voltage2", v)
            elif r[i+6]==72 and r[i+7]==7:
                v = (256.0*r[i+11] + 1.0*r[i+12])/10.0
                print("Momentary RMS phase voltage L3=    {0:3.1f} V".format(v), end="\t")
                client.publish("meter/voltage3", v)
            elif r[i+6]==31 and r[i+7]==7:
                v = (256.0*r[i+11] + 1.0*r[i+12])/10.0
                print("Momentary RMS current phase (L1)=    {0:3.1f} A".format(v), end="\t")
                client.publish("meter/current1", v)
            elif r[i+6]==51 and r[i+7]==7:
                v = (256.0*r[i+11] + 1.0*r[i+12])/10.0
                print("Momentary RMS current phase (L2)=    {0:3.1f} A".format(v), end="\t")
                client.publish("meter/current2", v)
            elif r[i+6]==71 and r[i+7]==7:
                v = (256.0*r[i+11] + 1.0*r[i+12])/10.0
                print("Momentary RMS current phase (L3)=    {0:3.1f} A".format(v), end="\t")
                client.publish("meter/current3", v)
            elif r[i+6]==21 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary active power+ (L1)=     {0:4d} W".format(p), end="\t")
                client.publish("meter/activepower1", p)
            elif r[i+6]==22 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary active power- (L1)=     {0:4d} W".format(p), end="\t")                
            elif r[i+6]==41 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary active power+ (L2)=     {0:4d} W".format(p), end="\t")
                client.publish("meter/activepower2", p)
            elif r[i+6]==42 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary active power- (L2)=     {0:4d} W".format(p), end="\t")
            elif r[i+6]==61 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary active power+ (L3)=     {0:4d} W".format(p), end="\t")
                client.publish("meter/activepower3", p)
            elif r[i+6]==62 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary active power- (L3)=     {0:4d} W".format(p), end="\t")
            elif r[i+6]==23 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary reactive power+ (L1)=   {0:4d} VAr".format(p), end="\t")
            elif r[i+6]==24 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary reactive power- (L1)=   {0:4d} VAr".format(p), end="\t")
            elif r[i+6]==43 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary reactive power+ (L2)=   {0:4d} VAr".format(p), end="\t")
            elif r[i+6]==44 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary reactive power- (L2)=   {0:4d} VAr".format(p), end="\t")
            elif r[i+6]==63 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary reactive power+ (L3)=   {0:4d} VAr".format(p), end="\t")
            elif r[i+6]==64 and r[i+7]==7:
                p = 256*r[i+13] + r[i+14]
                print("Momentary reactive power- (L3)=   {0:4d} VAr".format(p), end="\t")
        print("{0:02x}".format(r[i]), end=" ")
    print("")
    etime2 = (time.time() - stime2)
    
