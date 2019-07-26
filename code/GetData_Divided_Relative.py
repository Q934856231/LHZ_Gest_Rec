# -*- coding: utf-8 -*-
'''
兰大信息院2015级刘洪志
联系方式 724776196@qq.com 或者这个QQ
此部分代码用于制作数据集，核心思路是把对应的特征点全部保存在数组中，然后用pandas写入csv文件
打开文件后根据引导使用即可，会将做好的数据集文件放在当前文件夹下
2019.05.15
with python3.6.8 tensorflow1.2.1
'''

#%%
import Leap, sys, os
import pandas as pd

#%%
hand_palm_x=[]
hand_palm_y=[]
hand_palm_z=[]
t_d_x=[]
t_d_y=[]
t_d_z=[]
t_p_x=[]
t_p_y=[]
t_p_z=[]
i_d_x=[]
i_d_y=[]
i_d_z=[]
i_p_x=[]
i_p_y=[]
i_p_z=[]
m_d_x=[]
m_d_y=[]
m_d_z=[]
m_p_x=[]
m_p_y=[]
m_p_z=[]
r_d_x=[]
r_d_y=[]
r_d_z=[]
r_p_x=[]
r_p_y=[]
r_p_z=[]
p_d_x=[]
p_d_y=[]
p_d_z=[]
p_p_x=[]
p_p_y=[]
p_p_z=[]
xxx_Gesture1=[]
xxx_Gesture2=[]
xxx_Gesture3=[]

#%%

data_name = input("Enter the dataname \n")
gesture_name = input("What gesture's data do you want to record?\n 1:Rock\n 2:Paper\n 3:Scissor\n")
frame_number = 0
frame_limit = eval(input("Maximum number of frames recorded?\n"))
#%%

#要使用Leap Motion SDK，要先声明这个类，之后打开监听器后就会调用这里的内容

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
        global frame_number
        global gesture_name
        global frame_limit
        gesture_mode = ''
        
        '''
        print ("Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        '''
        
        # Get hands
        for hand in frame.hands:
            
            frame_number = frame_number + 1
            print ('\nFrame:%d'%(frame_number))
            

            if gesture_name=='1':
                gesture_mode = 'Rock'
                xxx_Gesture1.append('1')
                xxx_Gesture2.append('0')
                xxx_Gesture3.append('0')
            elif gesture_name=='2':
                gesture_mode = 'Paper'
                xxx_Gesture1.append('0')
                xxx_Gesture2.append('1')
                xxx_Gesture3.append('0')
            elif gesture_name=='3':
                gesture_mode = 'Scissor'
                xxx_Gesture1.append('0')
                xxx_Gesture2.append('0')
                xxx_Gesture3.append('1')
                
            print ('Your gesture mode is ' + gesture_mode)
            '''
            print ("  %s, id %d, position: %s" % (handType, hand.id, hand.palm_position))
            hand_palm_x.append(hand.palm_position[0])
            hand_palm_y.append(hand.palm_position[1])
            hand_palm_z.append(hand.palm_position[2])
            '''
        
            '''
            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            arm = hand.arm
            print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
                arm.direction,
                arm.wrist_position,
                arm.elbow_position)
            '''
            # Get fingers
            for finger in hand.fingers:

                print ("    %s finger, id: %d, " % (
                    self.finger_names[finger.type],
                    finger.id))

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    bone_position = (bone.prev_joint + bone.next_joint)/2
                    relative_coordinates = bone_position - hand.palm_position
                    print ("      Bone: %s,  Relative Position: %s" % (
                        self.bone_names[bone.type],
                        relative_coordinates))
                    if self.finger_names[finger.type] == 'Thumb':
                        if self.bone_names[bone.type] == 'Distal':
                            t_d_x.append(round(relative_coordinates[0],4))
                            t_d_y.append(round(relative_coordinates[1],4))
                            t_d_z.append(round(relative_coordinates[2],4))
                        elif self.bone_names[bone.type] == 'Proximal':
                            t_p_x.append(round(relative_coordinates[0],4))
                            t_p_y.append(round(relative_coordinates[1],4))
                            t_p_z.append(round(relative_coordinates[2],4))
                    elif self.finger_names[finger.type] == 'Index':
                        if self.bone_names[bone.type] == 'Distal':
                            i_d_x.append(round(relative_coordinates[0],4))
                            i_d_y.append(round(relative_coordinates[1],4))
                            i_d_z.append(round(relative_coordinates[2],4))
                        elif self.bone_names[bone.type] == 'Proximal':
                            i_p_x.append(round(relative_coordinates[0],4))
                            i_p_y.append(round(relative_coordinates[1],4))
                            i_p_z.append(round(relative_coordinates[2],4))
                    elif self.finger_names[finger.type] == 'Middle':
                        if self.bone_names[bone.type] == 'Distal':
                            m_d_x.append(round(relative_coordinates[0],4))
                            m_d_y.append(round(relative_coordinates[1],4))
                            m_d_z.append(round(relative_coordinates[2],4))
                        elif self.bone_names[bone.type] == 'Proximal':
                            m_p_x.append(round(relative_coordinates[0],4))
                            m_p_y.append(round(relative_coordinates[1],4))
                            m_p_z.append(round(relative_coordinates[2],4))
                    elif self.finger_names[finger.type] == 'Ring':
                        if self.bone_names[bone.type] == 'Distal':
                            r_d_x.append(round(relative_coordinates[0],4))
                            r_d_y.append(round(relative_coordinates[1],4))
                            r_d_z.append(round(relative_coordinates[2],4))
                        elif self.bone_names[bone.type] == 'Proximal':
                            r_p_x.append(round(relative_coordinates[0],4))
                            r_p_y.append(round(relative_coordinates[1],4))
                            r_p_z.append(round(relative_coordinates[2],4))
                    elif self.finger_names[finger.type] == 'Pinky':
                        if self.bone_names[bone.type] == 'Distal':
                            p_d_x.append(round(relative_coordinates[0],4))
                            p_d_y.append(round(relative_coordinates[1],4))
                            p_d_z.append(round(relative_coordinates[2],4))
                        elif self.bone_names[bone.type] == 'Proximal':
                            p_p_x.append(round(relative_coordinates[0],4))
                            p_p_y.append(round(relative_coordinates[1],4))
                            p_p_z.append(round(relative_coordinates[2],4))
                            
            if frame_number >= frame_limit:
                print ('\nFinished')
                Write_Data()
                os._exit(0)
  
#%%                          
def Write_Data():
    
    dataframe = pd.DataFrame({'Thumb_Distal_x':t_d_x,
                              'Thumb_Distal_y':t_d_y,
                              'Thumb_Distal_z':t_d_z,
                              'Thumb_Proximal_x':t_p_x,
                              'Thumb_Proximal_y':t_p_y,
                              'Thumb_Proximal_z':t_p_z,
                              'Index_Distal_x':i_d_x,
                              'Index_Distal_y':i_d_y,
                              'Index_Distal_z':i_d_z,
                              'Index_Proximal_x':i_p_x,
                              'Index_Proximal_y':i_p_y,
                              'Index_Proximal_z':i_p_z,
                              'Middle_Distal_x':m_d_x,
                              'Middle_Distal_y':m_d_y,
                              'Middle_Distal_z':m_d_z,
                              'Middle_Proximal_x':m_p_x,
                              'Middle_Proximal_y':m_p_y,
                              'Middle_Proximal_z':m_p_z,
                              'Ring_Distal_x':r_d_x,
                              'Ring_Distal_y':r_d_y,
                              'Ring_Distal_z':r_d_z,
                              'Ring_Proximal_x':r_p_x,
                              'Ring_Proximal_y':r_p_y,
                              'Ring_Proximal_z':r_p_z,
                              'Pinky_Distal_x':p_d_x,
                              'Pinky_Distal_y':p_d_y,
                              'Pinky_Distal_z':p_d_z,
                              'Pinky_Proximal_x':p_p_x,
                              'Pinky_Proximal_y':p_p_y,
                              'Pinky_Proximal_z':p_p_z,
                              'Geture:Rock':xxx_Gesture1,
                              'Geture:Paper':xxx_Gesture2,
                              'Geture:Scissor':xxx_Gesture3
                              })

    #将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv(data_name+"_Relative.csv",index=False,header=None,sep=',') #header=True可以加入特征点的名称，建议不要加，除非是展示

#%%
def GetData_main():
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
        Write_Data()

#%%
if __name__ == "__main__":
    GetData_main()

