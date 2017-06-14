import csv
import itertools as it
import copy
from datetime import datetime
import re
import time

st_time = time.time()

exec(open('importData.py').read())
exec(open('importTargets.py').read())
exec(open('importCat.py').read())

# data_labels = {}
# for i in range(len(san_data)):
#     for j in range(len(san_data[i])):
#         if 'uid:' in san_data[i][j]:
#             uid = san_data[i][j+1]
#         if 'gender:' in san_data[i][j]:
#             gender = san_data[i][j+1]
#     if uid not in data_labels:
#         data_labels.update({uid : gender})

#build pIndex
for i in range(len(san_data)):
    pid = []
    for j in range(len(san_data[i])):
        if ("pid" in str(san_data[i][j])):
            pid.append(san_data[i][j+1][1:-2])
        if 'gender:' in str(san_data[i][j]):
            gender = san_data[i][j+1]
    for k in range(len(pid)):
        if pid[k] in pIndex:
            if gender>0.5: #if female
                pIndex.update({pid[k] : [pIndex[pid[k]][0] + 1, pIndex[pid[k]][1] + 1]})
            else:
                pIndex.update({pid[k] : [pIndex[pid[k]][0] - 1, pIndex[pid[k]][1] + 1]})

for p in pIndex.keys():
    if pIndex[p][1] < 1: #if this product was not in the dataset
        pIndex.update({p : 0})
    else:
        pIndex.update({p : pIndex[p][0]/(pIndex[p][1])})

#data_ids = []
#data_labels = []
data_set = []
data_dic={}

for i in range(len(san_data)):
    uid = 0
    gender = 0
    source = [0]*2
    page_type = [0]*10
    purchase = 0
    products = []
    productIndex = 0
    #labels: source<Desktop,Mobile> pgType<cart,checkout,search,category,subcategory,confirm,home,brand_landing,other,product> purchase productIndex
    for j in range(len(san_data[i])):
        if 'uid' in str(san_data[i][j]):
            uid = san_data[i][j+1]
        if 'gender' in str(san_data[i][j]):
            gender = san_data[i][j+1]
        if 'source' in str(san_data[i][j]):
            source_str = san_data[i][j+1]
            if 'desktop' in source_str:
                source = [1,0]
            if 'mobile' in source_str:
                source = [0,1]
        if 'page_type' in str(san_data[i][j]):
            page_type_str = san_data[i][j+1]
            if 'cart' in page_type_str:
                page_type = [1]+[0]*9
            if 'checkout' in page_type_str:
                page_type = [0]+[1]+[0]*8
            if 'search' in page_type_str:
                page_type = [0]*2+[1]+[0]*7
            if '"category' in page_type_str:
                page_type = [0]*3+[1]+[0]*6
            if 'subcategory' in page_type_str:
                page_type = [0]*4+[1]+[0]*5
            if 'confirm' in page_type_str:
                page_type = [0]*5+[1]+[0]*4
            if 'home' in page_type_str:
                page_type = [0]*6+[1]+[0]*3
            if 'brand' in page_type_str:
                page_type = [0]*7+[1]+[0]*2
            if 'other' in page_type_str:
                page_type = [0]*8+[1]+[0]
            if 'product' in page_type_str:
                page_type = [0]*9+[1]
        if 'purchase' in str(san_data[i][j]):
            purchase = 1
        if '"pid"' in str(san_data[i][j]):
            products.append([san_data[i][j+1][1:-2], float(san_data[i][j+3][:-3])])
    n_p=0
    for k in range(len(products)):
        productIndex = productIndex + products[k][1]*pIndex[products[k][0]]
        n_p = n_p + products[k][1]
    if n_p>0:
        productIndex = productIndex/n_p
    #data_ids.append(uid)
    if uid not in data_dic:
        data_dic.update({uid : [source+page_type+[purchase]+[productIndex]+[gender]]})
    else:
        instances = data_dic[uid]
        instances.append(source+page_type+[purchase]+[productIndex]+[gender])
        data_dic.update({uid : instances})

for key, value in data_dic.items():
    data_point = [0]*14
    p=0
    for i in range(len(value)):
        p = p + value[i][-3] #how many purchases were made
        data_point = [sum(x) for x in zip(data_point,[y/len(value) for y in value[i][:-1]])]
    if p>0:
        data_set.append([key]+[len(value)/100]+data_point+[value[0][-1]])

del data_dic
del san_data
del data

target_set = []
target_dic={}

for i in range(len(san_target)):
    uid = 0
    source = [0]*2
    page_type = [0]*10
    purchase = 0
    products = []
    productIndex = 0
    #labels: source<Desktop,Mobile> pgType<cart,checkout,search,category,subcategory,confirm,home,brand_landing,other,product> purchase productIndex
    for j in range(len(san_target[i])):
        if 'uid' in str(san_target[i][j]):
            uid = san_target[i][j+1]
        if 'source' in str(san_target[i][j]):
            source_str = san_target[i][j+1]
            if 'desktop' in source_str:
                source = [1,0]
            if 'mobile' in source_str:
                source = [0,1]
        if 'page_type' in str(san_target[i][j]):
            page_type_str = san_target[i][j+1]
            if 'cart' in page_type_str:
                page_type = [1]+[0]*9
            if 'checkout' in page_type_str:
                page_type = [0]+[1]+[0]*8
            if 'search' in page_type_str:
                page_type = [0]*2+[1]+[0]*7
            if '"category' in page_type_str:
                page_type = [0]*3+[1]+[0]*6
            if 'subcategory' in page_type_str:
                page_type = [0]*4+[1]+[0]*5
            if 'confirm' in page_type_str:
                page_type = [0]*5+[1]+[0]*4
            if 'home' in page_type_str:
                page_type = [0]*6+[1]+[0]*3
            if 'brand' in page_type_str:
                page_type = [0]*7+[1]+[0]*2
            if 'other' in page_type_str:
                page_type = [0]*8+[1]+[0]
            if 'product' in page_type_str:
                page_type = [0]*9+[1]
        if 'purchase' in str(san_target[i][j]):
            purchase = 1
        if '"pid"' in str(san_target[i][j]):
            products.append([san_target[i][j+1][1:-2], float(san_target[i][j+3][:-3])])
    n_p=0
    for k in range(len(products)):
        productIndex = productIndex + products[k][1]*pIndex[products[k][0]]
        n_p = n_p + products[k][1]
    if n_p>0:
        productIndex = productIndex/n_p
    #data_ids.append(uid)
    if uid not in target_dic:
        target_dic.update({uid : [source+page_type+[purchase]+[productIndex]]})
    else:
        instances = target_dic[uid]
        instances.append(source+page_type+[purchase]+[productIndex])
        target_dic.update({uid : instances})

for key, value in target_dic.items():
    data_point = [0]*14
    p=0
    for i in range(len(value)):
        p = p + value[i][-2] #how many purchases were made
        data_point = [sum(x) for x in zip(data_point,[y/len(value) for y in value[i][:]])]
    if p>0:
        target_set.append([key]+[len(value)/100]+data_point)

print('Data processing finished in '+ str(time.time()-st_time) + ' seconds')
