# -*- coding: utf-8 -*-
'''
兰大信息院2015级刘洪志
联系方式 724776196@qq.com 或者这个QQ
此部分代码用于设置网络结构，参数定义在tools.py中
这个结构一看就明白了
2019.05.15

with python3.6.8 tensorflow1.2.1
'''
#%%

import tensorflow as tf
import tools

#%%
def FNET(x, n_classes, is_pretrain=False, train = True, droprate = 0.5):
    
    with tf.name_scope('FNET'):
        x = tools.FC_layer('fc1', x, out_nodes=300)
        #print(x)
        with tf.name_scope('batch_norm1'):
            x =  tf.nn.dropout(x, droprate)
        x = tools.FC_layer('fc2', x, out_nodes=300)
        with tf.name_scope('batch_norm2'):
            x =  tf.nn.dropout(x, droprate)
        #print(x)
        x = tools.FC_layer('fc3', x, out_nodes=300)
        #print(x)
        x = tools.FC_layer('fc4', x, out_nodes=n_classes)
        #print(x)

        return x



#%%







            
