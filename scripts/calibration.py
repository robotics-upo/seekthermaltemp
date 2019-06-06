#!/usr/bin/env python

#ROS PYTHON
import rospy
import numpy as np
import matplotlib.pylab as pl

#Import all the messages included in ThermalImage
from seekthermal_ros.msg import ThermalImage
#Needed to do operations on images and data
from sensor_msgs.msg import Image
from sensor_msgs.msg import ChannelFloat32

#CV module and route
import cv2

#Convert cv file ros files
from cv_bridge import CvBridge

#Save files
import os

def processimage(msg):
    #Default common parameters
    rospy.set_param('~path','/home/sergiod/catkin_ws/src/firetemp/txt')    
    rospy.set_param('~save',1)
    rospy.set_param('~threshval',80)
    
    #1) Confirm message and convert to opencv message
    img=CvBridge().imgmsg_to_cv2(msg.image_colored,"bgr8")
    #showImg(img,1)

    #2) Convert to single channel image and then to binary image
    ret,thresh = cv2.threshold(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),rospy.get_param('~threshval'), 255, cv2.THRESH_BINARY)      

    #3) Detect
    imc,contours,h=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if(contours==[]):
        ima=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        maxC=max(contours,key=lambda c: cv2.contourArea(c))
        ima=cv2.drawContours(cv2.cvtColor(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY),cv2.COLOR_GRAY2BGR),[maxC],-1,(0,0,255),1)
    showImg(ima,3)

    #4) Asssociate image to raw data from data raw
    rows,cols=np.where(thresh>0)
    data_raw=np.asarray(msg.data_raw).reshape(msg.height,msg.width)
    xval=np.ones(rows.size)

    for k in np.arange(rows.size):
        x=rows[k]
        y=cols[k]
        xval[k]=data_raw[x,y]

    #5) Save data
    if(rospy.get_param('~save')==1):
        number=input('Temp value:' )
        temp=number*np.ones(rows.size)
        string='cal'+str(number)+'.txt'
        string2='cal'+str(number)+'.jpg'
        np.savetxt(os.path.join(rospy.get_param('~path'),string),np.transpose([xval,temp]),fmt='%e',header="Rawdata Temp(Celsius)")
        cv2.imwrite(os.path.join(rospy.get_param('~path'),string2),ima)


#Show images in different displays
def showImg(img,number):
    string='fire'+str(number)
    cv2.imshow(string,img)
    cv2.waitKey(1)

def calibrate():
    rospy.init_node("calibrate")
    rospy.loginfo('node started')
    rospy.Subscriber("thermal_camera/thermal_image_raw",ThermalImage,processimage)
    rospy.spin()

if __name__=="__main__":
    try:
        calibrate()
    except rospy.ROSInterruptException:
        pass
