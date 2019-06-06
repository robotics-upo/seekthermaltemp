# seekthermaltemp
ROSpy node to obtain temperatures from raw data's thermal camera Seek thermal Compact

This node lets you know the temperature that the camera detects. It suscribes to thermal_camera/thermal_image_raw, converts the raw
data into temperature by loading the parameters from the yaml file (we observed that there is a linear regression between raw data
and temperature) and we publish the matrix on the Temperature topic.





In order to subscribe to the topic, you need to install ROS SeekThermal node and their libraries:   
https://github.com/ethz-asl/seekthermal_ros

