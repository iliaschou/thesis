import os
import sys
import time


def contains_namespace(x):
    if sys.argv[1] in x:
        return True
    else:
        return False


while(True):
    prev_logs = []

    r_file = open('logs.txt', 'r')
    for line in r_file:
        prev_logs.append(line[:-1])
    r_file.close()

    current_logs = [x for x in os.listdir('/var/log/containers') if contains_namespace(x)]

    if (current_logs != prev_logs):

        w_file = open('logs.txt', 'w')
        for x in current_logs:
            w_file.write(x + "\n")
        w_file.close()

        if (len(prev_logs) == 0):
            continue

        break

    time.sleep(1)

