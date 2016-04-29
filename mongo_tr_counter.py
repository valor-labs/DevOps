#!/usr/bin/env python

import os
import time


ipt_cmd = "iptables -L INPUT -n -v -x | grep 27017"
stat_file = "/var/log/mongo_traffic_counter.txt"
dayly_file = "/var/log/mongo_traffic_dayly.txt"

saved_bytes = 0

previous_value = 0
current_value = 0
dayly_reported = False

if os.path.exists(stat_file):
    with open(stat_file, "r") as sf:
        res = sf.readline().strip()
        saved_bites = int(res)
        
while True:
    ss = os.popen(ipt_cmd)
    current_value = int(ss.read().split()[1])
    ss.close()
    delta = current_value - previous_value
    previous_value = current_value
    saved_bytes += delta
    with open(stat_file, "w") as sf:
        sf.write(str(saved_bytes))
    cur_time = time.localtime()
    if cur_time.tm_hour == 0 and cur_time.tm_min == 0 and not dayly_reported:
        with open(dayly_file, "a") as df:
            df.write("%s   %d\n" % (time.strftime("%D"), saved_bytes))
        dayly_reported = True
    elif cur_time.tm_hour != 0 or cur_time.tm_min != 0:
        dayly_reported = False
    time.sleep(10)
