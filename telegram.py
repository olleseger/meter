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
    0x1d : ["var", 1],
    0x1e : ["kWh", 1000.0],
    0x20 : ["kvarh", 1000.0],
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
    0x00000100 : "Timestamp: {0:4d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}\t\t\t",
    0x01000107 : "Momentary active power+       = {0:4d} {1:s}\t\t",
    0x01000207 : "Momentary active power-       = {0:4d} {1:s}\t\t",
    0x01000307 : "Momentary reactive power+     = {0:4d} {1:s}\t",
    0x01000407 : "Momentary reactive power-     = {0:4d} {1:s}\t",
    0x01001f07 : "Momentary current (L1)        = {0:3.1f} {1:s}\t\t",
    0x01003307 : "Momentary current (L2)        = {0:3.1f} {1:s}\t\t",
    0x01004707 : "Momentary current (L3)        = {0:3.1f} {1:s}\t\t",
    0x01002007 : "Momentary voltage (L1)        = {0:3.1f} {1:s}\t\t",
    0x01003407 : "Momentary voltage (L2)        = {0:3.1f} {1:s}\t\t",
    0x01004807 : "Momentary voltage (L3)        = {0:3.1f} {1:s}\t\t",
    0x01001507 : "Momentary active power+ (L1)  = {0:4d} {1:s}\t\t",
    0x01001607 : "Momentary active power- (L1)  = {0:4d} {1:s}\t\t",
    0x01001707 : "Momentary reactive power+ (L1)= {0:4d} {1:s}\t",
    0x01001807 : "Momentary reactive power- (L1)= {0:4d} {1:s}\t",
    0x01002907 : "Momentary active power+ (L2)  = {0:4d} {1:s}\t\t",
    0x01002a07 : "Momentary active power- (L2)  = {0:4d} {1:s}\t\t",
    0x01002b07 : "Momentary reactive power+ (L2)= {0:4d} {1:s}\t",
    0x01002c07 : "Momentary reactive power- (L2)= {0:4d} {1:s}\t",
    0x01003d07 : "Momentary active power+ (L3)  = {0:4d} {1:s}\t\t",
    0x01003e07 : "Momentary active power- (L3)  = {0:4d} {1:s}\t\t",
    0x01003f07 : "Momentary reactive power+ (L3)= {0:4d} {1:s}\t",
    0x01004007 : "Momentary reactive power- (L3)= {0:4d} {1:s}\t",
    0x01000108 : "Cumulative active energy+     = {0:5.1f} {1:s}\t",
    0x01000208 : "Cumulative active energy-     = {0:5.1f} {1:s}\t",
    0x01000308 : "Cumulative reactive energy+   = {0:5.1f} {1:s}\t",
    0x01000408 : "Cumulative reactive energy-   = {0:5.1f} {1:s}\t",
}


class aidon(object):
    def __init__(self, serial_port = "/dev/ttyUSB0",
                 debug = False, verbose = False):

        def on_publish(client, userdata, mid):
            print("on_publish, mid={0:3}".format(mid))

        self.debug = debug
        self.verbose = verbose
        
        if not debug:
            self.ser = serial.Serial(port = serial_port,
                                     baudrate = 115200,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE,
                                     bytesize=serial.EIGHTBITS,
                                     timeout=5.1,
                                     rtscts=False,
                                     dsrdtr=False,
                                     xonxoff=False)

            try:
                from secrets import secrets
            except ImportError:
                print("MQTT secrets are kept in secrets.py!")
            
            self.client = mqtt.Client("Aidon")
            self.client.username_pw_set(username = secrets["username"],
                                        password = secrets["password"])
            #self.client.on_publish = on_publish # callback
            self.client.connect(secrets["hostname"])
            self.client.loop_start()

    ############################
    # try to read one frame
    # TODO: read flag first, then length and then the bytes
    ############################
    def read_frame(self):
        if self.debug:
            self.r = bytes(telegram)
        else:
            self.r = self.ser.read(N)
            M = len(self.r)
            if M == N:
                if self.verbose:
                    print("Read frame M={0:3}".format(M))
                return True
            else:
                if self.verbose:
                    print("Read error M={0:3}".format(M))
                return False

    ############################
    # Check flags
    # Check length
    # Check CRC
    ############################
    def check_frame(self):
        if self.r[0] != flag or self.r[-1] != flag:
            if self.verbose:
                print("Flags not OK! first= 0x{0:02x} last= 0x{1:02x}".format(self.r[0], self.r[-1]))
            return False

        # strip flags
        self.r = self.r[1:-1]
        
        packagelen = int.from_bytes(self.r[0:2], byteorder="big") & 0xfff
        
        if (packagelen) != len(self.r):
            if self.verbose:
                print("Length not OK! from header={0:4d} received={0:4d}".format(packagelen, len(self.r)))
            return False

        crc1 = libscrc.x25(self.r[0:-2])
        self.crc2 = int.from_bytes(self.r[-2:], byteorder="little")
    
        if crc1 != self.crc2:
            if self.verbose:
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
        str = ""
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
                    
                str += fmt.format(year, month, day, hour, min, sec)
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
                str += fmt.format(p, un)

            if self.debug:
                for i in range(N_line):
                    str += "{0:02x} ".format(self.r[i])

            str += "\n"
        
            self.r = self.r[N_line:]

        if self.debug:
            str += "CRC:\t\t\t\t\t\t{0:04x}\n".format(self.crc2)
            str += "Flag:\t\t\t\t\t\t{0:02x}".format(flag)

        if self.verbose:
            print(str)
        
        
    ############################
    # Publicera till MQTT
    ############################
    def publish_frame(self):
        if not self.debug:
            self.client.publish("meter/activepowerimp", self.measurements[0])
            self.client.publish("meter/activepowerexp", self.measurements[1])
            self.client.publish("meter/reactivepowerimp", self.measurements[2])
            self.client.publish("meter/reactivepowerexp", self.measurements[3])

            self.client.publish("meter/current1", self.measurements[4])
            self.client.publish("meter/current2", self.measurements[5])
            self.client.publish("meter/current3", self.measurements[6])

            self.client.publish("meter/voltage1", self.measurements[7])
            self.client.publish("meter/voltage2", self.measurements[8])
            self.client.publish("meter/voltage3", self.measurements[9])

            self.client.publish("meter/activepower1imp", self.measurements[10])
            self.client.publish("meter/activepower1exp", self.measurements[11])
            self.client.publish("meter/reactivepower1imp", self.measurements[12])
            self.client.publish("meter/reactivepower1exp", self.measurements[13])

            self.client.publish("meter/activepower2imp", self.measurements[14])
            self.client.publish("meter/activepower2exp", self.measurements[15])
            self.client.publish("meter/reactivepower2imp", self.measurements[16])
            self.client.publish("meter/reactivepower2exp", self.measurements[17])

            self.client.publish("meter/activepower3imp", self.measurements[18])
            self.client.publish("meter/activepower3exp", self.measurements[19])
            self.client.publish("meter/reactivepower3imp", self.measurements[20])
            self.client.publish("meter/reactivepower3exp", self.measurements[21])
        
            self.client.publish("meter/activeenergyimp", self.measurements[22])
            self.client.publish("meter/activeenergyexp", self.measurements[23])
            self.client.publish("meter/reactiveenergyimp", self.measurements[24])
            self.client.publish("meter/reactiveenergyexp", self.measurements[25])

            p = self.measurements[0] - self.measurements[1]
            q = self.measurements[2] - self.measurements[3]
            cosfi = round(p/math.sqrt(p*p + q*q), 2)
            self.client.publish("meter/cosfi", cosfi)