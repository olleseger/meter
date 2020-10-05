from telegram3 import aidon
import sys

if __name__ == "__main__":
    if len(sys.argv)>1:
        if str(sys.argv[1]) == "-d":
            print("debug")
            dbg = True
    else:
        dbg = False

    meter = aidon(debug=dbg)

    while True:
        meter.read_frame()
        if not meter.check_frame():
            continue

        meter.parse_frame()

        if dbg:
            break
        
        meter.publish_frame()
        
        

