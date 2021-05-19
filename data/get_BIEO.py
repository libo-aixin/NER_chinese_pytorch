#/usr/bin/env python
'''
created on 5/15 2021
@author = libo
'''

import json
import pandas as pd


#use the script to convert the original text into a dataset in BIEO format
data=[]
with open(r'/mnt/public/libo/github/rnn/chinese_NER_pytorch/data/train.json', 'r', encoding='utf8') as inp:
    for line in inp.readlines():
        data.append(json.loads(line.strip().split('\n')[0]))
        print(line.split('\n'))
data_all=[]
for i in range(len(data)):
    dict={}
    for key in data[i]['label']:
        dict[key]=[]
        for key1 in data[i]['label'][key]:
            dict[key].append(data[i]['label'][key][key1][0])
#stored is the location information of each name corresponding to each row
    data_all.append(dict)
index_all=[] #store the value of each sentence length
for i in range(len(data_all)):
    d=data[i]['text']
    index_1=[]
    for j in range(len(d)):
        index_1.append(j)
    index_all.append(index_1)
def rm(dict,data):
    for key in dict:
        for i in dict[key]:
            for j in range(i[0],i[1]+1):
                data.remove(j)
    return data
#delete the value of corresponding index number,and the rest is the correspond other part,which is marked as O
for i in range(len(data_all)):
    if i!=1506:
        rm(data_all[i],index_all[i])
def sp_b(d,index,key):
    return d[index]+" "+"B-"+key+'\n'
def sp_m(d,index,key):
    return d[index]+" "+"I-"+key+'\n'
def sp_e(d,index,key):
    return d[index]+" "+"E-"+key+'\n'
def sp_O(d,index):
    return str(d[index])+" O"+'\n'
def oth(dict,d):
    data1=[]
    for i in range(len(d)):
        data1.append(i)
    for key in dict:
        for i in dict[key]:
            for j in range(i[0],i[1]+1):
                data1.remove(j)
    return data1
#add the marked content after the corresponding text,and store it in the dict format
def ind(data_all,data,index):
    dict=data_all[index]
    d=data[index]['text']
    dict_1={}
    for key in dict:
         for i in dict[key]:
                for j in range(i[0],i[1]+1):
                    if(j==i[0]):
                        dict_1[j]=sp_b(d,j,key)
                    elif(j==i[1]):
                        dict_1[j]=sp_e(d,j,key)
                    else:
                        dict_1[j]=sp_m(d,j,key)
    return dict_1
data_dic=[]
for i in range(len(data)):
    data_dic.append(ind(data_all,data,i))
for j in range(len(index_all)):
    for i in index_all[j]:
        d=data[j]['text']
        data_dic[j][i]=sp_O(d,i)
#in order to ensure that the order does not change when connecting,sort according to the key of the dict
for i in range(len(data)):
     data_dic[i]=sorted(data_dic[i].items(),key=lambda d:d[0])
#connect all sentences together and separate them with 'end' marked
data_f=[]
for i in range(len(data)):
    str1=""
    for j in range(len(data_dic[i])):
        str1=str1+""+data_dic[i][j][1]
    data_f.append(str1)
with open(r'NER_train', 'w', encoding='utf8') as f:
    for line in data_f:
        f.write(line+"end\n")
