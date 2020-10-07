import serial
import paho.mqtt.client as mqtt
import libscrc
import math
import time

##############################################
# test telegram
##############################################
telegram = [
    0x7e,
    0xa2, 0x43, 0x41, 0x08, 0x83, 0x13, 0x85, 0xeb, 0xe6, 0xe7, 0x00,
    0x0f, 0x40, 0x00, 0x00, 0x00, 0x00,
    0x01, 0x1b,
    0x02, 0x02, 0x09, 0x06, 0x00, 0x00, 0x01, 0x00, 0x00, 0xff, 0x09, 0x0c, 0x07, 0xe3, 0x0c, 0x10, 0x01, 0x07, 0x3b, 0x28, 0xff, 0x80, 0x00, 0xff,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x01, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x04, 0x62, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1b,
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x02, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1b,
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x03, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x05, 0xe3, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1d,
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x04, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1d,
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x1f, 0x07, 0x00, 0xff, 0x10, 0x00, 0x00, 0x02, 0x02, 0x0f, 0xff, 0x16, 0x21,
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x33, 0x07, 0x00, 0xff, 0x10, 0x00, 0x4b, 0x02, 0x02, 0x0f, 0xff, 0x16, 0x21,
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x47, 0x07, 0x00, 0xff, 0x10, 0x00, 0x00, 0x02, 0x02, 0x0f, 0xff, 0x16, 0x21,		
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x20, 0x07, 0x00, 0xff, 0x12, 0x09, 0x03, 0x02, 0x02, 0x0f, 0xff, 0x16, 0x23,
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x34, 0x07, 0x00, 0xff, 0x12, 0x09, 0xc3, 0x02, 0x02, 0x0f, 0xff, 0x16, 0x23,
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x48, 0x07, 0x00, 0xff, 0x12, 0x09, 0x04, 0x02, 0x02, 0x0f, 0xff, 0x16, 0x23,		
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x15, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1b,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x16, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1b,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x17, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1d,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x18, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1d,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x29, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x04, 0x62, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1b,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x2a, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1b,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x2b, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x05, 0xe2, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1d,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x2c, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1d,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x3d, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1b,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x3e, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1b,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x3f, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1d,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x40, 0x07, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x00, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1d,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x01, 0x08, 0x00, 0xff, 0x06, 0x00, 0x99, 0x59, 0x86, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1e,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x02, 0x08, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x08, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x1e,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x03, 0x08, 0x00, 0xff, 0x06, 0x00, 0x64, 0xed, 0x4b, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x20,	
    0x02, 0x03, 0x09, 0x06, 0x01, 0x00, 0x04, 0x08, 0x00, 0xff, 0x06, 0x00, 0x00, 0x00, 0x05, 0x02, 0x02, 0x0f, 0x00, 0x16, 0x20,	
    0xbe, 0x40,
    0x7e
]

##############################################
# format of telegram
##############################################
flag = 0x7e
N = 581 # total length
N_header = 19 # length of header
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

# key : [nr_bytes signed]
values = {
    0x06 : [4, False],
    0x10 : [2, True],
    0x12 : [2, False]
}

# obis_key : format string
aidon_strings = {
    0x00000100 : "Timestamp: {0:4d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}\t\t",
    0x01000107 : "Momentary active power+       = {0:4d} {1:s}\t",
    0x01000207 : "Momentary active power-       = {0:4d} {1:s}\t",
    0x01000307 : "Momentary reactive power+     = {0:4d} {1:s}",
    0x01000407 : "Momentary reactive power-     = {0:4d} {1:s}",
    0x01001f07 : "Momentary current (L1)        = {0:3.1f} {1:s}\t",
    0x01003307 : "Momentary current (L2)        = {0:3.1f} {1:s}\t",
    0x01004707 : "Momentary current (L3)        = {0:3.1f} {1:s}\t",
    0x01002007 : "Momentary voltage (L1)        = {0:3.1f} {1:s}\t",
    0x01003407 : "Momentary voltage (L2)        = {0:3.1f} {1:s}\t",
    0x01004807 : "Momentary voltage (L3)        = {0:3.1f} {1:s}\t",
    0x01001507 : "Momentary active power+ (L1)  = {0:4d} {1:s}\t",
    0x01001607 : "Momentary active power- (L1)  = {0:4d} {1:s}\t",
    0x01001707 : "Momentary reactive power+ (L1)= {0:4d} {1:s}",
    0x01001807 : "Momentary reactive power- (L1)= {0:4d} {1:s}",
    0x01002907 : "Momentary active power+ (L2)  = {0:4d} {1:s}\t",
    0x01002a07 : "Momentary active power- (L2)  = {0:4d} {1:s}\t",
    0x01002b07 : "Momentary reactive power+ (L2)= {0:4d} {1:s}",
    0x01002c07 : "Momentary reactive power- (L2)= {0:4d} {1:s}",
    0x01003d07 : "Momentary active power+ (L3)  = {0:4d} {1:s}\t",
    0x01003e07 : "Momentary active power- (L3)  = {0:4d} {1:s}\t",
    0x01003f07 : "Momentary reactive power+ (L3)= {0:4d} {1:s}",
    0x01004007 : "Momentary reactive power- (L3)= {0:4d} {1:s}",
    0x01000108 : "Cumulative active energy+     = {0:5.1f} {1:s}",
    0x01000208 : "Cumulative active energy-     = {0:5.1f} {1:s}",
    0x01000308 : "Cumulative reactive energy+   = {0:5.1f} {1:s}",
    0x01000408 : "Cumulative reactive energy-   = {0:5.1f} {1:s}",
}


class aidon(object):
    def __init__(self, serial_port = "/dev/ttyUSB0",
                 debug = False):

        self.debug = debug

        if not debug:
            self.ser = serial.Serial(port = serial_port,
                                     baudrate = 115200,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE,
                                     bytesize=serial.EIGHTBITS,
                                     timeout=2.0)

            try:
                from secrets import secrets
            except ImportError:
                print("MQTT secrets are kept in secrets.py!")
                raise
            
            self.client = mqtt.Client("Aidon")
            self.client.username_pw_set(username = secrets["username"],
                                        password = secrets["password"])
            self.client.connect(secrets["hostname"])

    ############################
    # try to read one frame
    # TODO: read flag first, then length and then the bytes
    ############################
    def read_frame(self):
        if self.debug:
            self.r = bytes(telegram)
        else:
            while True:
                self.r = self.ser.read(N)
                M = len(self.r)
                if M == N:
                    break

    ############################
    # Check flags
    # Check length
    # Check CRC
    ############################
    def check_frame(self):
        if self.r[0] != flag or self.r[-1] != flag:
            print("Flags not OK! first= 0x{0:02x} last= 0x{1:02x}".format(self.r[0], self.r[-1]))
            return False

        # strip flags
        self.r = self.r[1:-1]
        
        packagelen = int.from_bytes(self.r[0:2], byteorder="big") & 0xfff
        
        if (packagelen) != len(self.r):
            print("Length not OK! from header={0:4d} received={0:4d}".format(packagelen, len(self.r)))
            return False

        crc1 = libscrc.x25(self.r[0:-2])
        self.crc2 = int.from_bytes(self.r[-2:], byteorder="little")
    
        if crc1 != self.crc2:
            print("CRC not OK! calculated= 0x{0:04x} sent= 0x{1:04x}".format(crc1, self.crc2))
            return False

        frameheader = self.r[3:12]
        dataheader = self.r[12:18]
        self.N_lines = self.r[N_header-1]

        if self.debug:
            print("Package length = {0:4d}".format(packagelen))
            print("Nr of registers = {0:4d}".format(self.N_lines))

            print("\nFlag:", end="\t\t\t\t\t\t")
            print("{0:02x}".format(flag), end=" ")
            print("\nHeader:", end="\t\t\t\t\t\t")
            for i in range(N_header):
                print("{0:02x}".format(self.r[i]), end=" ")
            print("")

        # strip header and trailer
        self.r = self.r[N_header:-2]

        return True

    ############################
    # Read Timestamp
    # Read 4 quadrants momentary power
    # Read 3 phases current
    # Read 3 phases voltage
    # Read 3x4 momentary powers
    # Read 4 quadrants of energy
    ############################
    def decode_frame(self):
        self.measurements = []
        for lines in range(self.N_lines):
            obis = int.from_bytes(self.r[4:8], byteorder="big")
            fmt = aidon_strings[obis]

            if fmt[:9] == "Timestamp":
                N_line = 12 + self.r[11]

                year = int.from_bytes(self.r[12:14], byteorder="big")
                month = self.r[14]
                day = self.r[15]
                # wd = self.r[16] # weekday
                hour = self.r[17]
                min = self.r[18]
                sec = self.r[19]

                if self.r[N_line-1] & 0x80:
                    hour += 1  # summer time
                print(fmt.format(year, month, day, hour, min, sec), end="\t")
            else:
                key = self.r[10]
                nr = values[key][0]
                pm = values[key][1]
            
                N_line = 11 + nr + 6

                key = self.r[N_line-1]
                dv = units[key][1]
                un = units[key][0]
        
                p = int.from_bytes(self.r[11:11+nr], byteorder="big", signed = pm)
                if dv != 1:
                    p = p/dv
                
                self.measurements.append(p)
                print(fmt.format(p, un), end="\t")

            if self.debug:
                #print("\n\nOBIS={0:d}-{1:d}:{2:d}.{3:d}.{4:d}.{5:d}".format(r[4], r[5], r[6], r[7], r[8], r[9]), end=" ")
                for i in range(N_line):
                    print("{0:02x}".format(self.r[i]), end=" ")
            print("")
        
            self.r = self.r[N_line:]

        if self.debug:
            print("CRC:", end="\t\t\t\t\t\t")
            print("{0:04x}".format(self.crc2))
            print("Flag:", end="\t\t\t\t\t\t")
            print("{0:02x}".format(flag))

        print("")

        
    ############################
    # Publicera till MQTT
    ############################
    def publish_frame(self):
        ap = self.measurements[0] - self.measurements[1]
        rp = self.measurements[2] - self.measurements[3]
        fi = 180*math.atan2(rp,ap)/math.pi

        ap1 = self.measurements[10] - self.measurements[11]
        rp1 = self.measurements[12] - self.measurements[13]
        fi1 = 180*math.atan2(rp1, ap1)/math.pi

        ap2 = self.measurements[14] - self.measurements[15]
        rp2 = self.measurements[16] - self.measurements[17]
        fi2 = 180*math.atan2(rp2, ap2)/math.pi

        ap3 = self.measurements[18] - self.measurements[19]
        rp3 = self.measurements[20] - self.measurements[21]
        fi3 = 180*math.atan2(rp3, ap3)/math.pi

        ae = self.measurements[22] - self.measurements[23]
        re = self.measurements[24] - self.measurements[25]
        fie = 180*math.atan2(re, ae)/math.pi

        if not self.debug:
            self.client.publish("meter/activepower", ap)
            self.client.publish("meter/fi", fi)
        
            self.client.publish("meter/current1", self.measurements[4])
            self.client.publish("meter/current2", self.measurements[5])
            self.client.publish("meter/current3", self.measurements[6])

            self.client.publish("meter/voltage1", self.measurements[7])
            self.client.publish("meter/voltage2", self.measurements[8])
            self.client.publish("meter/voltage3", self.measurements[9])

            self.client.publish("meter/activepower1", ap1)
            self.client.publish("meter/fi1", fi1)
            self.client.publish("meter/activepower2", ap2)
            self.client.publish("meter/fi2", fi2)
            self.client.publish("meter/activepower3", ap3)
            self.client.publish("meter/fi3", fi3)
        
            self.client.publish("meter/activeenergy", ae)
            self.client.publish("meter/fie", fie)

