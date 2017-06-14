import csv
import itertools as it
import copy
from datetime import datetime
import re
import time

st_time = time.time()

#get all the values of a given label
def getLabels(d,lbl):
    labels = []
    for i in range(len(d)):
        if(lbl) in d[i]:
            lbl_val = d[i][d[i].index(lbl)+1]
            if lbl_val not in labels:
                labels.append(lbl_val)
    return labels

#get the n first indexes with val
def findWith(d,val,n):
    indexes = []
    for i in range(len(d)):
        for j in range(len(d[i])):
            if val in str(d[i][j]):
                indexes.append(i)
                break
        if len(indexes)>n:
            return indexes

#get all of the occurences with given label
def nOccur(d,lbl):
    values = {}
    for i in range(len(d)):
        if lbl in d[i]:
            val = d[i][d[i].index(lbl)+1]
            if val not in values:
                values.update({val : 1})
            else:
                values.update({val : values[val] + 1})
    return values


#IMPORT CSV INTO A LIST
data = []
with open('data', newline='') as csvfile:
    rdr= csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in rdr:
        data.append(row)

san_data = copy.deepcopy(data)
#SANITARIZE data
#1 - change data labels to proper data
for i in range(len(san_data)):
    for j in range(len(san_data[i])):
        if san_data[i][j] == '{"page_type":':
            san_data[i][j] = 'page_type:'
        if san_data[i][j] == '"event_type":':
            san_data[i][j] = 'event_type:'
        if san_data[i][j] == '"source":':
            san_data[i][j] = 'source:'
        # if san_data[i][j] == '"timestamp":':
        #     san_data[i][j] = 'timestamp:'
        #     san_data[i][j+1] = datetime.strptime(san_data[i][j+1]+','+san_data[i][j+2], '"%Y-%m-%d,%H:%M:%S",' )
        #     san_data[i][j+2] = 'REMOVE' #mark for removal
        # if san_data[i][j] == '{"date":':
        #     san_data[i][j] = 'timestamp:'
        #     san_data[i][j+1] = datetime.strptime(san_data[i][j+1]+','+san_data[i][j+2], '"%Y-%m-%d,%H:%M:%S",' )
        #     san_data[i][j+2] = 'REMOVE' #mark for removal
        if san_data[i][j] == '"gender":':
            san_data[i][j] = 'gender:'
            if 'F' in san_data[i][j+1]: #F is class 1
                san_data[i][j+1] = 1
            else:
                san_data[i][j+1] = 0 #not F (M) is 0
        if san_data[i][j] == '"uid":':
            san_data[i][j] = 'uid:'
            san_data[i][j+1] = re.split('\"',san_data[i][j+1])[1]

print("Data import finished in " + str(time.time()-st_time) + ' seconds')

# for i in range(len(san_data)):
#     test_labels.append(['uid', 'gen'])
#     test_set.append([0]*15 #source<NaN,Desktop,Mobile> pgType<cart,checkout,search,category,subcategory,confirm,home,brand_landing,other,product> purchase productIndex
#     for j in range(len(san_data[i])):
#         if san_data[i][j] == 'uid:':
#             tast_labels





#split intro training and test set
# splitRatio = 0.67
# trainSize = int(len(dataset) * splitRatio)
# trainSet = []



#2 - eliminate non-compliant datapoints
#san_data[:] = it.filterfalse(lambda x: x[0]!=san_data[0][0],san_data)

#SEPARATE DATA BY USER
#data_points = []
#cp_data = list(data) #copy of data
#for i in range(len(data)):
#    for
