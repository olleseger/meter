from telegram3 import aidon
import sys

if __name__ == "__main__":
    if len(sys.argv)>1:
        if str(sys.argv[1]) == "-d":
            print("debug")
            debug = True
        else:
            debug = False

    meter = aidon(debug=True)

    while True:
        meter.read_frame()
        if not meter.check_frame():
            continue

        meter.parse_frame()

        if debug:
            break
        
        meter.publish_frame()
        
        

