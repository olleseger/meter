from telegram import aidon
import sys

if __name__ == "__main__":
    if len(sys.argv)>1:
        if str(sys.argv[1]) == "-d":
            print("debug")
            dbg = True
            vrb = True
        elif str(sys.argv[1]) == "-v":
            print("verbose")
            vrb = True
            dbg = False
    else:
        dbg = False
        vrb = False
        
    meter = aidon(debug=dbg, verbose=vrb)

    while True:
        meter.read_frame()
        if not meter.check_frame():
            continue

        meter.decode_frame()

        if dbg:
            break
        
        meter.publish_frame()
        
        

