# -*- coding: utf-8 -*-
'''
兰大信息院2015级刘洪志
联系方式 724776196@qq.com 或者这个QQ
展示用，直接打开文件是个锤子剪刀布，在后面加上数字是返回这么多帧内最有可能的手势，即精确识别功能
例如：
锤子剪刀布（返回图片是相反的）：>>>python Func_Show.py
精确识别：>>> python Func_Show.py 帧数
2019.05.15
with python3.6.8 tensorflow1.2.1
'''
#%%
import sys,Leap

import numpy as np
import tensorflow as tf
import cv2 as cv
import time
import FNET

#%%

N_CLASSES = 3
BATCH_SIZE = 100
IS_PRETRAIN = True
    
maxx = [50.16552734, 65.6835022, 42.82162476, 35.6002388, 44.68052673, 45.67756653, 84.26382446, 83.5309906, 45.03229523, 45.54312134, 44.41134644, 30.45932007, 87.94572449, 88.70004272, 20.55984497, 40.80511475, 41.6133728, 9.271935463, 87.27183533, 84.78593445, 32.03580475, 42.0705452, 38.69861603, 7.452250481, 78.83547974, 70.18112183, 26.50528336, 49.85293198, 38.27700806, 27.86437988]
minn = [-86.09602356, -54.13500214, -75.97263336, -52.22180939, -47.3949585, -20.23625183, -87.7742691, -75.20361328, -90.21035004, -47.17438507, -43.28884888, -44.55815887, -84.28627014, -77.19732666, -94.46350861, -38.21066284, -36.4724884, -42.89574814, -74.51626587, -75.99629211, -84.53527832, -29.50695992, -39.58595276, -38.56386566, -61.74092102, -67.54748535, -78.53426361, -42.40896606, -42.94207001, -44.85429764]

function_list = ['Rock','Paper','Scissor']
pic1=cv.imread('Rock.png')
pic2=cv.imread('Paper.png')
pic3=cv.imread('Scissor.png')

gesture_temp=0
ges_flag_1=0
ges_flag_2=0
ges_flag_3=0
ges_mode=0
mode = 1
x_flag=0
y_flag=0
z_flag=0
x_posflag = 0
x_negflag = 0
y_posflag = 0
y_negflag = 0
z_posflag = 0
z_negflag = 0

if len(sys.argv) == 1:
    mode = 0
    ges_limit = 0
else:
    ges_limit = eval(sys.argv[1])



#%%

class MyListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print ("Initialized")

    def on_connect(self, controller):
        print ("Connected")


    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print ("Disconnected")

    def on_exit(self, controller):
        print ("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information 

        frame = controller.frame()
        previous = controller.frame(1)

        '''
        print ("Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        '''
        
        # Get hands
        for hand in frame.hands:
        
            global gesture_temp,ges_flag_1,ges_flag_2,ges_flag_3,ges_mode,mode, ges_limit
            global x_posflag,x_negflag,y_posflag,y_negflag,z_posflag,z_negflag
            temp=[]
            '''
            #这个功能是返回手掌的方向向量，做动态手势识别的时候用的
            prev_hand = previous.hands.rightmost
            hand_x = hand.palm_position[0]-prev_hand.palm_position[0]
            hand_y = hand.palm_position[1]-prev_hand.palm_position[1]
            hand_z = hand.palm_position[2]-prev_hand.palm_position[2]
            if hand_x > 0:
                x_symbol = 1
                x_posflag = x_posflag+1
            else: 
                x_symbol = -1
                x_negflag = x_negflag+1
            if hand_y > 0:
                y_symbol = 1
                y_posflag = y_posflag+1
            else: 
                y_symbol = -1
                y_negflag = y_negflag+1
            if hand_z > 0:
                z_symbol = 1
                z_posflag = z_posflag+1
            else: 
                z_symbol = -1
                z_negflag = z_negflag+1
                
            position_symbol = [x_symbol,y_symbol,z_symbol]
            print(position_symbol)
            if x_posflag + x_negflag >= ges_limit:
                if max(x_flag,y_flag,z_flag) == x_flag:
                    ges_mode = 1
                elif max(x_flag,y_flag,z_flag) == x_flag_2:
                    ges_mode = 2
                else:
                    ges_mode = 3
                ges_flag_1 = ges_flag_2 = ges_flag_3 = 0
            '''
            
            # Get fingers
            for finger in hand.fingers:
                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    bone_position = (bone.prev_joint + bone.next_joint)/2
                    relative_coordinates = bone_position - hand.palm_position

                    if self.bone_names[bone.type] == 'Distal':
                            temp.append(round(relative_coordinates[0],4))
                            temp.append(round(relative_coordinates[1],4))
                            temp.append(round(relative_coordinates[2],4))
                    elif self.bone_names[bone.type] == 'Proximal':
                            temp.append(round(relative_coordinates[0],4))
                            temp.append(round(relative_coordinates[1],4))
                            temp.append(round(relative_coordinates[2],4))
            
            
            use(temp) 
            if use(temp)==1:
                ges_flag_1 = ges_flag_1 + 1
            elif use(temp)==2:
                ges_flag_2 = ges_flag_2 + 1
            elif use(temp)==3:
                ges_flag_3 = ges_flag_3 + 1
            
            if ges_flag_1 + ges_flag_2 + ges_flag_3 >= ges_limit:
                if max(ges_flag_1, ges_flag_2, ges_flag_3) == ges_flag_1:
                    ges_mode = 1
                elif max(ges_flag_1, ges_flag_2, ges_flag_3) == ges_flag_2:
                    ges_mode = 2
                else:
                    ges_mode = 3
                ges_flag_1 = ges_flag_2 = ges_flag_3 = 0
                
            if ges_mode==gesture_temp:
                pass
            else: 
                gesture_temp = ges_mode
                cv.destroyAllWindows()
                if ges_mode==3:
                    cv.namedWindow('input_image', cv.WINDOW_AUTOSIZE)
                    if mode ==0:
                        cv.imshow('input_image', pic1)
                    else:
                        cv.imshow('input_image', pic3)
                    cv.waitKey(1)
                if ges_mode==1:
                    cv.namedWindow('input_image', cv.WINDOW_AUTOSIZE)
                    if mode ==0:
                        cv.imshow('input_image', pic2)
                    else:
                        cv.imshow('input_image', pic1)
                    cv.waitKey(1)
                if ges_mode==2:
                    cv.namedWindow('input_image', cv.WINDOW_AUTOSIZE)
                    if mode ==0:
                        cv.imshow('input_image', pic3)
                    else:
                        cv.imshow('input_image', pic2)
                    cv.waitKey(1)    
                    
            

#%%

    
    
                
#%%

def use(a):
    with tf.Graph().as_default(): #实例一个默认计算图
        
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
                saver.restore(sess, ckpt.model_checkpoint_path)
                #print('Loading success, global_step is %s' % global_step)
                print('Loading success')
            else:
                print('No checkpoint file found')
                return
        
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess = sess, coord = coord)
            
            try:
                print('Put your hand on the Leap Motion')
                data = []
                for i in range(30):
                    data.append((a[i]-minn[i])/(maxx[i] - minn[i]))
                data = np.array(data)
                tensor_data = tf.convert_to_tensor(data)
                tensor_data = tf.cast(tensor_data, dtype=tf.float32)
                datain = tf.reshape(tensor_data, [30])

                tra_images = sess.run([datain])
                llg= sess.run([logits],feed_dict={x:tra_images})
                llgnp=llg[0]
                llglist = llgnp.tolist()
                #print(llg)
                #print("gesture1:%f, gesture2:%f, gesture3:%f"%(llglist[0][0],llglist[0][1],llglist[0][2]))
                if(llglist[0][0] > llglist[0][1] and llglist[0][0] > llglist[0][2]):
                    print(function_list[0])
                    return(1)
                elif(llglist[0][1] >= llglist[0][2]):
                    print(function_list[1])
                    return(2)
                else:
                    print(function_list[2])
                    return(3)
            except Exception as e:
                coord.request_stop(e)
            finally:
                coord.request_stop()
                coord.join(threads)             
                
#%%

def Show_Main():
    # Create a sample listener and controller
    listener = MyListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print ("Press Enter to quit...")  
        
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

#%%

if __name__ == "__main__":

    Show_Main()


