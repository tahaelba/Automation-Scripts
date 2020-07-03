#!/usr/bin/env python3
import csv
import re
import operator

error = {}
per_user = {}

with open("syslog.log", "r") as f:
    lines = f.readlines()
    for line in lines:
        infomatch = re.search(r"ticky: INFO ([\w ]*) ", line)
        errormatch = re.search(r"ticky: ERROR ([\w ]*) ", line)
        username = re.search(r"\((.*)\)", line)
        #print(username.group(1))
        if infomatch:
            check = per_user.get(username.group(1), -1)
            if check == -1:
                per_user[username.group(1)] = [0,0]
                per_user[username.group(1)][0] += 1
            else:
                per_user[username.group(1)][0] += 1
        if errormatch:
            print(errormatch.group(1))
            check = per_user.get(username.group(1), -1)
            check_error = error.get(errormatch.group(1), -1)
            if check_error == -1:
                error[errormatch.group(1)] = 1
            else:
                error[errormatch.group(1)] += 1
                if check == -1:
                    per_user[username.group(1)] = [0,0]
                    per_user[username.group(1)][1] += 1
                else:
                    per_user[username.group(1)][1] += 1
print(error)
error = sorted(error.items(), key=operator.itemgetter(1), reverse=True)
per_user = sorted(per_user.items(), key=operator.itemgetter(0))
print(per_user)
print(error)
with open("error_message.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Error', 'Count'])
    for row in error:
        writer.writerow(row)
with open("user_statistics.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Username', 'INFO', 'ERROR'])
    for row in per_user:
        new_row = (row[0], row[1][0], row[1][1])
        writer.writerow(new_row)
