import csv
import itertools as it
import copy
from datetime import datetime
import re
import time

st_time = time.time()


#IMPORT CSV INTO A LIST
catalog_raw = []
with open('catalog', newline='') as csvfile:
    rdr= csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in rdr:
        catalog_raw.append(row)

san_catalog=[]

for i in range(len(catalog_raw)):
    san_catalog.append(re.split(',',catalog_raw[i][0]))

pIndex={}

for i in range(1,len(san_catalog)):
    if san_catalog[i][0] not in pIndex:
        pIndex.update({san_catalog[i][0] : [0,0]})

print("Cat import finished in "+ str(time.time()-st_time) + ' seconds')

# san_data = copy.deepcopy(data)
# #SANITARIZE data
# #1 - change data labels to proper data
# for i in range(len(san_data)):
#     for j in range(len(san_data[i])):
#         if san_data[i][j] == '{"page_type":':
#             san_data[i][j] = 'page_type:'
#         if san_data[i][j] == '"event_type":':
#             san_data[i][j] = 'event_type:'
#         if san_data[i][j] == '"source":':
#             san_data[i][j] = 'source:'
#         if san_data[i][j] == '"timestamp":':
#             san_data[i][j] = 'timestamp:'
#             san_data[i][j+1] = datetime.strptime(san_data[i][j+1]+','+san_data[i][j+2], '"%Y-%m-%d,%H:%M:%S",' )
#             san_data[i][j+2] = 'REMOVE' #mark for removal
#         if san_data[i][j] == '{"date":':
#             san_data[i][j] = 'timestamp:'
#             san_data[i][j+1] = datetime.strptime(san_data[i][j+1]+','+san_data[i][j+2], '"%Y-%m-%d,%H:%M:%S",' )
#             san_data[i][j+2] = 'REMOVE' #mark for removal
#         if san_data[i][j] == '"gender":':
#             san_data[i][j] = 'gender:'
#             if 'F' in san_data[i][j+1]: #F is class 1
#                 san_data[i][j+1] = 1
#             else:
#                 san_data[i][j+1] = 0 #not F (M) is 0
#         if san_data[i][j] == '"uid":':
#             san_data[i][j] = 'uid:'
#             san_data[i][j+1] = re.split('\"',san_data[i][j+1])[1]



#2 - eliminate non-compliant datapoints
#san_data[:] = it.filterfalse(lambda x: x[0]!=san_data[0][0],san_data)

#SEPARATE DATA BY USER
#data_points = []
#cp_data = list(data) #copy of data
#for i in range(len(data)):
#    for
