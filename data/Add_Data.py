# -*- coding: utf-8 -*-
'''
兰大信息院2015级刘洪志
联系方式 724776196@qq.com 或者这个QQ
把之前做好的各手势的数据集文件和这个代码文件放在一个目录下，运行该程序会将所有csv文件合并为data.csv
2019.05.15
with python3.6.8 tensorflow1.2.1
'''
#%%

import os
import pandas as pd
import glob

csv_list = glob.glob('*.csv') #查看同文件夹下的csv文件数
print(u'共发现%s个CSV文件'% len(csv_list))
print(u'正在处理............')
for i in csv_list: #循环读取同文件夹下的csv文件
    fr = open(i,'rb').read()
    with open('data.csv','ab') as f: #将结果保存为result.csv
        f.write(fr)
print(u'合并完毕！')