# -*- coding: utf-8 -*-
'''
兰大信息院2015级刘洪志
联系方式 724776196@qq.com 或者这个QQ
此部分代码是用于制作训练集和测试集的tfrecord文件
将数据集命名为data.csv，在同目录下可使用
使用后会将其随机分为训练集：测试集=9：1的两个文件
在输出界面将显示对应的minn和maxx，之后那两个值需要在其他程序中调用
2019.05.15
with python3.6.8 tensorflow1.2.1
'''
#%%
import os 
import tensorflow as tf 
import numpy as np
import json
import operator
import random

#%%

x_range = 30 #特征点个数
y_range = 3 #标签个数

count = 0
count2 = 0
writer1= tf.python_io.TFRecordWriter("./train.tfrecords")
writer2= tf.python_io.TFRecordWriter("./val.tfrecords")

file = open('./data.csv', 'r') #做好的数据集名字在这边改
line = file.readlines()
random.shuffle(line)
count = 0
count1 = 0
count2 = 0

minn = x_range*[1000000.]
maxx = x_range*[-1000000.]

#%%
for i in line:
	ll = i.replace('\n','').split(',')
	for j in range(x_range):
		n = float(ll[j])
		if(n > maxx[j]):
			maxx[j] = n
		if(n<minn[j]):
			minn[j] = n


for i in line:
	ll = i.replace('\n','').split(',')
	data = []
	label = []
	for j in range(x_range):
		n = float(ll[j])
		data.append( (n-minn[j]) / (maxx[j]-minn[j]) )
	if( int(ll[x_range]) == 1):  #增加手势的话从这边开始改标签，加几个else就行
		label = [0]
	elif( int(ll[x_range+1]) == 1):
		label = [1]
	else:
		label = [2]

	if(count % 10 != 1):
		example = tf.train.Example(features=tf.train.Features(feature={
            "label": tf.train.Feature(int64_list=tf.train.Int64List(value=label)),
            'data': tf.train.Feature(float_list=tf.train.FloatList(value=data))
            }))
		writer1.write(example.SerializeToString())
		count1 +=1
	
	else:
		example = tf.train.Example(features=tf.train.Features(feature={
            "label": tf.train.Feature(int64_list=tf.train.Int64List(value=label)),
            'data': tf.train.Feature(float_list=tf.train.FloatList(value=data))
            }))
		writer2.write(example.SerializeToString())
		count2 +=1
	count += 1

	if(count % 100 ==0):
		print (count, label)

print (count, count1, count2)
print (minn)
print (maxx)

writer1.close()
writer2.close()