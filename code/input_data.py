# -*- coding: utf-8 -*-
'''
兰大信息院2015级刘洪志
联系方式 724776196@qq.com 或者这个QQ
此部分代码用于读取tfrecord文件，可以不用改
2019.05.15
with python3.6.8 tensorflow1.2.1
'''
#%%
import tensorflow as tf
import numpy as np
import os

#%% Reading data

def read_data(data_dir, is_train, batch_size, shuffle, test=0, n_test=100):
	"""Read CIFAR10
	
	Args:
		data_dir: the directory of CIFAR10
		is_train: boolen
		batch_size:
		shuffle:	   
	Returns:
		label: 1D tensor, tf.int32
		image: 4D tensor, [batch_size, height, width, 3], tf.float32
	
	"""
	
	
	with tf.name_scope('input'):
		
		if is_train:
			filenames = data_dir+'/train.tfrecords'
		else:
			filenames = data_dir+"/val.tfrecords"
		if test == 1:
			filenames = data_dir+"/index_test.tfrecords"
		filename_queue = tf.train.string_input_producer([filenames])
		reader = tf.TFRecordReader()

		_, serialized_example = reader.read(filename_queue)
		features = tf.parse_single_example (serialized_example,
											features={
												'label': tf.FixedLenFeature([], tf.int64),
												'data' : tf.FixedLenFeature([30], tf.float32),
												}
											)
		
		label = tf.cast(features['label'], tf.int32)
		data = tf.cast(features['data'], tf.float32)



		if test==1:
			data, label_batch = tf.train.shuffle_batch(
									[data, label], 
									batch_size = batch_size,
									num_threads = 64,
									capacity= 7000) 
		elif shuffle:
			data, label_batch = tf.train.shuffle_batch(
									[data, label], 
									batch_size = batch_size,
									num_threads= 64,
									capacity = 20000, 
									min_after_dequeue = 2000)  #越大随机性越强，可能导致读取时间变长
		else:
			data, label_batch = tf.train.batch(
									[data, label],
									batch_size = batch_size,
									num_threads = 64,
									capacity= n_test)
		## ONE-HOT
		

		n_classes = 3
		label_batch = tf.one_hot(label_batch, depth= n_classes)
		label_batch = tf.cast(label_batch, dtype=tf.int32)
		label_batch = tf.reshape(label_batch, [batch_size, n_classes])
		
		return data, label_batch
#%%




