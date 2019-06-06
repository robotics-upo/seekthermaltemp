#!/usr/bin/env python

#Rospython
import rospy

import numpy as np
import yaml
import os

#Type of msg to subscribe
from seekthermal_ros.msg import ThermalImage
from sensor_msgs.msg import ChannelFloat32
from sensor_msgs.msg import Image

#Type of msg to publish
from rospy_tutorials.msg import Floats

class Node(object):
    def __init__(self):
        #Frecuency of publications
        self.loop_rate=rospy.Rate(10)

        #Publisher
        self.pub=rospy.Publisher("Temperature",Floats,queue_size=10)

        #Suscriber
        rospy.Subscriber("thermal_camera/thermal_image_raw/",ThermalImage,self.calibrate)

        #Ros params
        rospy.set_param('~path','/home/sergiod/catkin_ws/src/firetemp/tempsiar/regresion.yaml')


    #Obtain the parameters from the regresion yaml file and use it on the data
    def calibrate(self,msg):
        cfg=yaml.load(open(rospy.get_param('~path'),'r'),Loader=yaml.FullLoader)
        reg=cfg.values()
        datatemp=np.asarray(msg.data_raw).reshape(msg.height,msg.width)*reg[0]+reg[1]
        print datatemp
        #rospy.loginfo("Publish data on temperature topic")
        self.pub.publish(datatemp)
        self.loop_rate.sleep()


    def startnode(self):
        rospy.loginfo("Node started")
        rospy.spin()


if __name__=="__main__":
    try:
        rospy.init_node("tempdata")
        my_node=Node()
        my_node.startnode()
    except rospy.ROSInterruptException:
        pass
