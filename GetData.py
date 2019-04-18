# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 20:04:06 2019

@author: LHZ
"""



import Leap, sys
import pandas as pd

'''
figer : Thumb Index Middle Ring Pinky
bone  : Distal Intermediate Proximal Metacarpal
'''
hand_plam=[]
t_d=[]
t_i=[]
t_p=[]
t_m=[]
i_d=[]
i_i=[]
i_p=[]
i_m=[]
m_d=[]
m_i=[]
m_p=[]
m_m=[]
r_d=[]
r_i=[]
r_p=[]
r_m=[]
p_d=[]
p_i=[]
p_p=[]
p_m=[]

data_name = raw_input("Please enter the dataname \n")
#frame_limit = input("Please enter the frame limit \n")
temp = raw_input( "Let's get data, if you are ready, press ENTER to continue.\nWhen you are in the scanning process, press ENTER to exit.")
frame_number = 0

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    


    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"


    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        global frame_number

        
        '''
        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        '''
        # Get hands
        for hand in frame.hands:
            
            frame_number = frame_number + 1
            print frame_number
            
            '''
            if frame_number == frame_limit:
                break
            '''
                
            

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s" % (handType, hand.id, hand.palm_position)
            hand_plam.append(hand.palm_position)
            
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

                print "    %s finger, id: %d, " % (
                    self.finger_names[finger.type],
                    finger.id)

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    bone_position = (bone.prev_joint + bone.next_joint)/2
                    print "      Bone: %s,  Position: %s" % (
                        self.bone_names[bone.type],
                        bone_position)
                    if self.finger_names[finger.type] == 'Thumb':
                        if self.bone_names[bone.type] == 'Distal':
                            t_d.append(bone_position)
                        elif self.bone_names[bone.type] == 'Proximal':
                            t_p.append(bone_position)
                    elif self.finger_names[finger.type] == 'Index':
                        if self.bone_names[bone.type] == 'Distal':
                            i_d.append(bone_position)
                        elif self.bone_names[bone.type] == 'Proximal':
                            i_p.append(bone_position)
                    elif self.finger_names[finger.type] == 'Middle':
                        if self.bone_names[bone.type] == 'Distal':
                            m_d.append(bone_position)
                        elif self.bone_names[bone.type] == 'Proximal':
                            m_p.append(bone_position)
                    elif self.finger_names[finger.type] == 'Ring':
                        if self.bone_names[bone.type] == 'Distal':
                            r_d.append(bone_position)
                        elif self.bone_names[bone.type] == 'Proximal':
                            r_p.append(bone_position)
                    elif self.finger_names[finger.type] == 'Pinky':
                        if self.bone_names[bone.type] == 'Distal':
                            p_d.append(bone_position)
                        elif self.bone_names[bone.type] == 'Proximal':
                            p_p.append(bone_position)
                            
                        
                        
                        

 

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

        dataframe = pd.DataFrame({'Hand_Plam': hand_plam,
                                  'Thumb_Distal':t_d,'Thumb_Proximal':t_p,
                                  'Index_Distal':i_d,'Index_Proximal':i_p,
                                  'Middle_Distal':m_d,'Middle_Proximal':m_p,
                                  'Ring_Distal':r_d,'Ring_Proximal':r_p,
                                  'Pinky_Distal':p_d,'Pinky_Proximal':p_p})
     
    #将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe.to_csv(data_name+".csv",index=False,sep=',')



if __name__ == "__main__":
    main()
