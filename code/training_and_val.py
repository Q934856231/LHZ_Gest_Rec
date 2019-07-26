# -*- coding: utf-8 -*-
'''
兰大信息院2015级刘洪志
联系方式 724776196@qq.com 或者这个QQ
此部分代码是用于有三个功能，可以单独复制出来使用
具体超参数可以自己修改。maxx和minn的值来源于record_train.py的输出结果。
1：训练，首先需要使用record_train.py将数据集转化为tfrecord文件后使用，使用后将在log文件夹下生成模型。
2：评估，可以将任意数据集使用record.py单独生成val.tfrecord文件，或是评估已有的val.tfrecord文件，使用目前的模型取得测试集准确率
3：使用，输入一个传感器得到的数据数组就可以得出识别结果，可以复制出来嵌入其他程序
2019.05.15
with python3.6.8 tensorflow1.2.1
'''
#%%
import sys
import os
import os.path

import numpy as np
import tensorflow as tf

import input_data
import FNET
import tools

#%%
X_RANGE = 30
N_CLASSES = 3
BATCH_SIZE = 100
learning_rate = 0.01
MAX_STEP = 10000   
IS_PRETRAIN = True
if(len(sys.argv) == 1):
    n_test = 100
else:
    n_test = int(sys.argv[1])
maxx = [50.16552734, 65.6835022, 42.82162476, 35.6002388, 44.68052673, 45.67756653, 84.26382446, 83.5309906, 45.03229523, 45.54312134, 44.41134644, 30.45932007, 87.94572449, 88.70004272, 20.55984497, 40.80511475, 41.6133728, 9.271935463, 87.27183533, 84.78593445, 32.03580475, 42.0705452, 38.69861603, 7.452250481, 78.83547974, 70.18112183, 26.50528336, 49.85293198, 38.27700806, 27.86437988]
minn = [-86.09602356, -54.13500214, -75.97263336, -52.22180939, -47.3949585, -20.23625183, -87.7742691, -75.20361328, -90.21035004, -47.17438507, -43.28884888, -44.55815887, -84.28627014, -77.19732666, -94.46350861, -38.21066284, -36.4724884, -42.89574814, -74.51626587, -75.99629211, -84.53527832, -29.50695992, -39.58595276, -38.56386566, -61.74092102, -67.54748535, -78.53426361, -42.40896606, -42.94207001, -44.85429764]
#%%   Training
def train():
    
    data_dir = '.'
    train_log_dir = './logs/train/'
    val_log_dir = './logs/val/'
    
    with tf.name_scope('input'):
        tra_data_batch, tra_label_batch = input_data.read_data(data_dir=data_dir,
                                                 is_train=True,
                                                 batch_size= BATCH_SIZE,
                                                 shuffle=True)
        val_data_batch, val_label_batch = input_data.read_data(data_dir=data_dir,
                                                 is_train=False,
                                                 batch_size= BATCH_SIZE,
                                                 shuffle=False)
        
    x = tf.placeholder(tf.float32, shape=[BATCH_SIZE, 30])
    y_ = tf.placeholder(tf.int16, shape=[BATCH_SIZE, N_CLASSES]) 
    
    logits = FNET.FNET(x, N_CLASSES, IS_PRETRAIN, train = True, droprate = 0.6 )
    loss = tools.loss(logits, y_)
    accuracy = tools.accuracy(logits, y_)
    
    my_global_step = tf.Variable(0, name='global_step', trainable=False) 
    train_op = tools.optimize(loss, learning_rate, my_global_step)   
    
    saver = tf.train.Saver(tf.global_variables())
    #summary_op = tf.summary.merge_all()   
       
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)


    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)    
    #tra_summary_writer = tf.summary.FileWriter(train_log_dir, sess.graph)
    #val_summary_writer = tf.summary.FileWriter(val_log_dir, sess.graph)
    numk = 3000/100
    numk = int(numk)
    bestaka = 0
    try:
        for step in np.arange(MAX_STEP):
            if coord.should_stop():
                    break
                
            tra_images,tra_labels = sess.run([tra_data_batch, tra_label_batch])
            _, tra_loss, tra_acc ,llg= sess.run([train_op, loss, accuracy, logits],
                                            feed_dict={x:tra_images, y_:tra_labels})            
            if step % 20 == 0 or (step + 1) == MAX_STEP:                 
                print ('Step: %d, loss: %.4f, accuracy: %.4f%%' % (step, tra_loss, tra_acc))
                #summary_str = sess.run(summary_op)
                #tra_summary_writer.add_summary(summary_str, step)
                
            if step % 400 == 0 or (step + 1) == MAX_STEP:
                val_images, val_labels = sess.run([val_data_batch, val_label_batch])
                val_loss, val_acc = sess.run([loss, accuracy], feed_dict={x:val_images,y_:val_labels})
                print('**  Step %d, val loss = %.2f, val accuracy = %.2f%%  **' %(step, val_loss, val_acc))

                #summary_str = sess.run(summary_op)
                #val_summary_writer.add_summary(summary_str, step)
            
            if step % 400 == 0:
                for i in llg:
                    print (i)

            if step % 800 == 0 or (step + 1) == MAX_STEP and step != 0:
                checkpoint_path = os.path.join(train_log_dir, 'model.ckpt')
                saver.save(sess, checkpoint_path, global_step=step)
            if step % 600 == 0 and step != 0:
                aka = 0
                for ii in range(numk):
                    val_images, val_labels = sess.run([val_data_batch, val_label_batch])
                    val_loss, val_acc = sess.run([loss, accuracy], feed_dict={x:val_images, y_:val_labels})
                    aka += val_acc
                aka = aka / numk
                print ('*****test accuracy = %.3f%% ***'  % (aka))
                if(aka > bestaka):
                    bestaka = aka
                    checkpoint_path = os.path.join("./logs/train_best", 'model.ckpt')
                    saver.save(sess, checkpoint_path, global_step=step)

            if step  == int(0.08*MAX_STEP):
                train_op = tools.optimize(loss, 0.002, my_global_step)
            if step == int(0.24*MAX_STEP):
                train_op = tools.optimize(loss, 0.0004, my_global_step)
            if step == int(0.4*MAX_STEP):
                train_op = tools.optimize(loss, 0.0001, my_global_step)
            if step == int(0.6*MAX_STEP):
                train_op = tools.optimize(loss, 0.00001, my_global_step)
    except tf.errors.OutOfRangeError:
        print('Done training -- epoch limit reached')
    finally:
        coord.request_stop()
        
    coord.join(threads)
    sess.close()





    
#%%   Test the accuracy on test dataset. got about 85.69% accuracy.
import math
def evaluate():
    with tf.Graph().as_default():
        
#        log_dir = 'C://Users//kevin//Documents//tensorflow//VGG//logsvgg//train//'
        log_dir = './logs/train/'
        test_dir = '.'
                
        data, labels = input_data.read_data(data_dir=test_dir,
                                                    is_train=False,
                                                    batch_size= BATCH_SIZE,
                                                    shuffle=False,
                                                    n_test=n_test)

        logits = FNET.FNET(data, N_CLASSES, IS_PRETRAIN, train = False, droprate = 1)
        correct = tools.num_correct_prediction(logits, labels)
        saver = tf.train.Saver(tf.global_variables())
        
        with tf.Session() as sess:
            
            print("Reading checkpoints...")
            ckpt = tf.train.get_checkpoint_state(log_dir)
            if ckpt and ckpt.model_checkpoint_path:
                global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                saver.restore(sess, ckpt.model_checkpoint_path)
                print('Loading success, global_step is %s' % global_step)
            else:
                print('No checkpoint file found')
                return
        
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess = sess, coord = coord)
            
            try:
                print('\nEvaluating......')
                num_step = int(math.floor(n_test / BATCH_SIZE))
                num_sample = num_step*BATCH_SIZE
                step = 0
                total_correct = 0
                while step < num_step and not coord.should_stop():
                    batch_correct = sess.run(correct)
                    total_correct += np.sum(batch_correct)
                    step += 1
                print('Total testing samples: %d' %num_sample)
                print('Total correct predictions: %d' %total_correct)
                print('Average accuracy: %.2f%%' %(100*total_correct/num_sample))
            except Exception as e:
                coord.request_stop(e)
            finally:
                coord.request_stop()
                coord.join(threads)
                
#%%


def use():
    with tf.Graph().as_default():
        
#        log_dir = 'C://Users//kevin//Documents//tensorflow//VGG//logsvgg//train//'
        log_dir = './logs/train/'
        test_dir = '.'
        
        x = tf.placeholder(tf.float32, shape=[1, 30])

        logits = FNET.FNET(x, N_CLASSES, IS_PRETRAIN, train = False, droprate = 1)
        saver = tf.train.Saver(tf.global_variables())
        global maxx
        global minn 
        with tf.Session() as sess:
            
            print("Reading checkpoints...")
            ckpt = tf.train.get_checkpoint_state(log_dir)
            if ckpt and ckpt.model_checkpoint_path:
                global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                saver.restore(sess, ckpt.model_checkpoint_path)
                print('Loading success, global_step is %s' % global_step)
            else:
                print('No checkpoint file found')
                return
        
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess = sess, coord = coord)
            
            try:
                while (True):
                    print('Please input your data, 30 float numbers which splited by , ')
                    a = (input()).split(',')
                    data = []
                    for i in range(30):
                        data.append((eval(a[i])-minn[i])/(maxx[i] - minn[i]))
                    data = np.array(data)
                    tensor_data=tf.convert_to_tensor(data)
                    tensor_data = tf.cast(tensor_data, dtype=tf.float32)
                    datain = tf.reshape(tensor_data, [ 30])

                    tra_images = sess.run([datain])
                    llg= sess.run([logits],feed_dict={x:tra_images})
                    llgnp=llg[0]
                    llglist = llgnp.tolist()
                    if(llglist[0][0] > llglist[0][1] and llglist[0][0] > llglist[0][2]):
                        print('Rock')
                    elif(llglist[0][1] >= llglist[0][2]):
                        print('Paper')
                    else:
                        print('Scissor')
            except Exception as e:
                coord.request_stop(e)
            finally:
                coord.request_stop()
                coord.join(threads)
                
#%%
'''
def runtest():
    with tf.Graph().as_default():
        f = open('t.txt', 'a')
#        log_dir = 'C://Users//kevin//Documents//tensorflow//VGG//logsvgg//train//'
        log_dir = './logs/train/'
        test_dir = '.'
        n_test = 7000
                
        images, labels = input_data.read_data(data_dir=test_dir,
                                                    is_train=False,
                                                    batch_size= BATCH_SIZE,
                                                    shuffle=False,
                                                    test = 1)

        logits = VGG.VGG16N(images, N_CLASSES, IS_PRETRAIN, train = False, droprate = 1)
        correct = tools.num_correct_prediction(logits, labels)
        saver = tf.train.Saver(tf.global_variables())
        
        with tf.Session() as sess:
            
            print("Reading checkpoints...")
            ckpt = tf.train.get_checkpoint_state(log_dir)
            if ckpt and ckpt.model_checkpoint_path:
                global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                saver.restore(sess, ckpt.model_checkpoint_path)
                print('Loading success, global_step is %s' % global_step)
            else:
                print('No checkpoint file found')
                return
        
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess = sess, coord = coord)
            number = []
            output = []
            try:
                print('\nEvaluating......')
                num_step = int(math.floor(n_test / BATCH_SIZE))+1
                step = 0
                while step < num_step and not coord.should_stop():
                    numb,outp = sess.run([labels, logits])
                    if step == 0:
                        number =  numb
                        output = np.argmax(outp, axis=1)
                    else:
                        number = np.concatenate((number,numb))
                        output = np.concatenate((output, np.argmax(outp, axis=1)))
                    step += 1
                for i in range(len(number)):
                    aa = number[i]
                    bb = output[i]+1
                    print (aa,bb, file = f)
            except Exception as e:
                coord.request_stop(e)
            finally:
                coord.request_stop()
                coord.join(threads)
 '''               


while(1):
    print('please input:\n 1:training\n 2:evaluate \n 3:use\n 4:exit\n')
    a = input()
    a = int(a)
    if(a == 1):
        print("it will run train step for " , MAX_STEP , " at most\n")
        train();
    elif(a == 2):
        print("it will test the test batch. \n")
        evaluate();
    elif(a==3):
        print("now you can input your data. \n")
        use();
    elif(a==4):
        #print("it will run test set. \n")
        #runtest();
        sys.exit()
    else:
        print("1 is train and 2 is test\n")
    
