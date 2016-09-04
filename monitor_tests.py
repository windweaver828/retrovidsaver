#!/usr/bin/env python

import struct
import time

if __name__ == "__main__":
    time.sleep(.1)
    try:
        input_devices = ["/dev/input/event4"]
        FORMAT = "llHHI"
        EVENT_SIZE = struct.calcsize(FORMAT)
        in_files = [open(x, "rb") for x in input_devices]
        events = list()
        for f in in_files:
            events.append(f.read(EVENT_SIZE))

        while True:
            for event in events[:]:
                events.remove(event)
                (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

                if type != 0 or code != 0 or value != 0:
                    print("Event type %u, code %u, value %u at %d.%d" % (type, code, value, tv_sec, tv_usec))
                else:
                    # Events with code, type and value == 0 are "separator" events
                    print("===========================================")

            for f in in_files:
                events.append(f.read(EVENT_SIZE))

    except KeyboardInterrupt:
        print("Exit detected, closing files")
        for f in in_files:
            f.close()
