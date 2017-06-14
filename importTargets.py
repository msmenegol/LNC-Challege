import csv
import itertools as it
import copy
from datetime import datetime
import re
import time

st_time = time.time()

#IMPORT CSV INTO A LIST
target = []
with open('target', newline='') as csvfile:
    rdr= csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in rdr:
        target.append(row)

def check_all(ids,idlabel, data,label):
    identifier=''
    idlist = dict(ids)
    count = 0
    check = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if idlabel in data[i][j]:
                identifier = data[i][j+1]
            if label in data[i][j]:
                check = 1 #if there is a label
        if check:
            if identifier in idlist:
                del idlist[identifier]
                count = count + 1
        check = 0
    return count, idlist



san_target = copy.deepcopy(target)
#SANITARIZE target
#1 - change target labels to proper target
for i in range(len(san_target)):
    for j in range(len(san_target[i])):
        if san_target[i][j] == '{"page_type":':
            san_target[i][j] = 'page_type:'
        if san_target[i][j] in ('"event_type":', '{"event_type":'):
            san_target[i][j] = 'event_type:'
        if san_target[i][j] == '"source":':
            san_target[i][j] = 'source:'
        # if san_target[i][j] == '"timestamp":':
        #     san_target[i][j] = 'timestamp:'
        #     san_target[i][j+1] = datetime.strptime(san_target[i][j+1], '"%Y-%m-%d",' )
        # if san_target[i][j] == '{"date":':
        #     san_target[i][j] = 'timestamp:'
        #     san_target[i][j+1] = datetime.strptime(san_target[i][j+1], '"%Y-%m-%d",' )
        if san_target[i][j] == '"uid":':
            san_target[i][j] = 'uid:'
            san_target[i][j+1] = re.split('\"',san_target[i][j+1])[1]

print("Targets import finished in " + str(time.time()-st_time) + ' seconds')
