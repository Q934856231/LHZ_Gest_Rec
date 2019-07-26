# -*- coding: utf-8 -*-
'''
兰大信息院2015级刘洪志
联系方式 724776196@qq.com 或者这个QQ
此部分代码用于单独制作测试集，具体方法为在命令行中输入>>>python record.py 文件名.csv
制作训练用的测试机和训练集请使用record_train.py文件
注意：使用这个会将原有测试集文件覆盖
2019.05.15
with python3.6.8 tensorflow1.2.1
'''
#%%
import os 
import tensorflow as tf 
from PIL import Image
import matplotlib.pyplot as plt 
import numpy as np
import json
import operator
import random
from PIL import ImageFile
import sys


count = 0
count2 = 0
os.remove("./val.tfrecords")
writer2= tf.python_io.TFRecordWriter("./val.tfrecords")

file = open(sys.argv[1], 'r') #获取后接文件名
line = file.readlines()
random.shuffle(line)
count = 0
count1 = 0
count2 = 0

maxx = [50.16552734, 65.6835022, 42.82162476, 35.6002388, 44.68052673, 45.67756653, 84.26382446, 83.5309906, 45.03229523, 45.54312134, 44.41134644, 30.45932007, 87.94572449, 88.70004272, 20.55984497, 40.80511475, 41.6133728, 9.271935463, 87.27183533, 84.78593445, 32.03580475, 42.0705452, 38.69861603, 7.452250481, 78.83547974, 70.18112183, 26.50528336, 49.85293198, 38.27700806, 27.86437988]
minn = [-86.09602356, -54.13500214, -75.97263336, -52.22180939, -47.3949585, -20.23625183, -87.7742691, -75.20361328, -90.21035004, -47.17438507, -43.28884888, -44.55815887, -84.28627014, -77.19732666, -94.46350861, -38.21066284, -36.4724884, -42.89574814, -74.51626587, -75.99629211, -84.53527832, -29.50695992, -39.58595276, -38.56386566, -61.74092102, -67.54748535, -78.53426361, -42.40896606, -42.94207001, -44.85429764]

for i in line:
    ll = i.replace('\n','').split(',')
    data = []
    label = []
    for j in range(30):
        n = float(ll[j])
        data.append( (n-minn[j]) / (maxx[j]-minn[j]) )
    if( int(ll[30]) == 1):
        label = [0]
    elif( int(ll[31]) == 1):
        label = [1]
    else:
        label = [2]

    example = tf.train.Example(features=tf.train.Features(feature={"label": tf.train.Feature(int64_list=tf.train.Int64List(value=label)),'data': tf.train.Feature(float_list=tf.train.FloatList(value=data))} ))
    writer2.write(example.SerializeToString())
    count2 +=1
    count += 1

    if(count % 100 ==0):
        print (count, label)

print (count, count1, count2)

writer2.close()
