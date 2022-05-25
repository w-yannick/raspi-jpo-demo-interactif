#!/usr/bin/python3
import subprocess
import psutil
import time
import os


def hot():
    ret = False
    temps = psutil.sensors_temperatures()
    for name, entries in temps.items():
        for entry in entries:
            print(entry.current, end='\t')
            if entry.critical and entry.current >= entry.critical:
                ret = True
    print()

    return ret


if __name__ == '__main__':
    temps = psutil.sensors_temperatures()
    for name, entries in temps.items():
        for entry in entries:
            print(entry.label or name, end='\t')
    print()
    start = time.time()
    FNULL = open(os.devnull, 'w')
    p_ui = subprocess.Popen(["../jpo"], stdout=FNULL)
    p_ws = subprocess.Popen(["../webserver"], stdout=FNULL)
    while True:
        stop = time.time()
        time.sleep(2)
        if hot():
            break

    print("ran for {} seconds".format(stop - start))
    p_ui.kill()
    p_ws.kill()
