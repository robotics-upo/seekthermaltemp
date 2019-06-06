# seekthermaltemp
ROSPY node to obtain temperatures from raw data's thermal camera Seek thermal Compact

This node lets you know the temperature, in Celsius degrees, that the camera detects. It suscribes to thermal_camera/thermal_image_raw, converts the raw data into temperature by loading the parameters from the yaml file (we observed that there is a linearity between the raw data and temperature) and we publish the matrix on the Temperature topic. The script siar_temps.py does that.

We include 2 scripts more: statistics.py and calibration.py. We also include on txt folder the images and text files we obtained and/or used to achieve the parameters in the yaml file.

The script calibration.py saves a picture of what the camera sees (in a jpg file) and the raw data (in a txt file).

The statistics.py:
   1) Loads the data from txt files 
   2) Makes a histogram of every txt
   3) Obtains the value we are interested in, taking into account that objects with a different temperature from  
   the background makes a "bell" curve on the histogram. In fact, the own background makes also a "bell" curve.
   4) Save the data in a matrix.First column contains mean value from the borders of the bar of the histogram which corresponds to the maximum frecuency value of the "bell" curve of the measured object. Second column contains the associated temperature.
   5) Makes linear regression. 
   6) Save the parameters to the yaml file.

In order to subscribe to the topic, you need to install ROS SeekThermal node and their libraries:   
https://github.com/ethz-asl/seekthermal_ros

Note: If you want to do calibrations with your own camera, you should change the private ROS parameter path to the path that you are interested in.
