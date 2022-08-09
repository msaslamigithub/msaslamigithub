import sys
import time
import signal
import threading as td
import headlessCalls as hl
import dutConfig as dut
exit_event = td.Event()

def display_usage():
    print("usage: headlsessTest <mode>, <tests> <duration> <cycles>, <debug>\n")
    print("\tmode: normal|ha|reboot\n\
    \ttests: basic=1,simring=2,escalation=4,consultransfer=8,all=15\n\
    \tduration: call duration in minutes\n\
    \tcycles: number of times to repeat the test\n\
    \tdebug: 1=enabled, 2=disabled\n")

def signal_handler(signum, frame):
    exit_event.set()

n = len(sys.argv)
if n < 6:
    display_usage()    
    exit(0)
 
mode = sys.argv[1]
test = int(sys.argv[2])
duration = int(sys.argv[3])
cycles = int(sys.argv[4])
debug = int(sys.argv[5])
if debug:
    print(f"mode={mode}, test={test}, duration={duration}, cycles={cycles}, debug={debug}")

#t1 = td.Thread(target=hl.headless_calls, args=(test, duration, cycles, debug))
#t1.start()

if mode == 'ha':
    #time.sleep(60)
    #t2 = td.Thread(target=dut.reboot_dut, args=(120, 2, debug))
    t2 = td.Thread(target=dut.reboot_dut, args=(10, 1, debug))
    t2.start()
    t2.join()

    #print(td.active_count())
    #print(td.enumerate())

#t1.join()

"""
for i in range(1, n):
    print(sys.argv[i])


for idx, arg in enumerate(sys.argv):
    if arg in ("--start", "-s"):
        starting_point = int(sys.argv[idex + 1])

fp = open(sys.arg[1], "r")
lines = fp.readlines()
print(lines)

import concurrent.futures
import time

start = time.perf_counter()
def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    print('Done sleeping...')

with concurrent.futures.ThreaPoolExecutor() as executor:
    secs = [5,4,3,2,1]
    results = executor.map(do_something, secs)
    for result in results:
        print(result
"""