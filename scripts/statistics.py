#!/usr/bin/env python

import os 
import numpy as np
import matplotlib.pylab as pl
import yaml

#rospkg for getting path
import rospkg

# Search the first number which is not zero on a decimal number
def contador(x,a):
    if(x<2.5):
        return contador(x*10,a+1)
    else:
        return a

#get package path 
rospack = rospkg.RosPack()
#rospack.list()
pkg_path = rospack.get_path('seekthermaltemp')
path = pkg_path + '/txt'

#1) Search for txt in specific folder 
#path='/home/sergiod/catkin_ws/src/firetemp/txt'
filelist=os.listdir(path)
filetxt=[]
filesnumber=0

for file in filelist:
    if(file.endswith(".txt")):
        filesnumber+=1
        filetxt.append(file)

data=np.ones((filesnumber,2))

#2) Obtain information and store it in data matrix
for file in filetxt:
    dataraw,temp=np.loadtxt(os.path.join(path,file),skiprows=1,unpack=True)
    freq,bins=np.histogram(dataraw,bins=50)
    filetxt.index(file)

    #Vectorization of pixels
    pixels=(bins[0:-1]+bins[1::])/2

    if(temp[0]>37.0):
        searchfreq=np.where((freq>1000) & (pixels>0))
        #This conditions acts when the tuple searcher is not empty
        if(any(map(len,searchfreq))):
            desfreq=max(freq[searchfreq])
            searchpixel=np.where(freq==desfreq)
            bestpixel=pixels[searchpixel]
        else:
            bestpixel=-999.99
            temp[0]=-999.99   
    else:
        #Search the coldest object and if it is not found we store data associated to
        #  the background
        searchfreq=np.where((freq>1000) & (pixels<-700.0))
        if(any(map(len,searchfreq))):
            desfreq=max(freq[searchfreq])
            searchpixel=np.where(freq==desfreq)
            bestpixel=pixels[searchpixel]
        else:
            searchfreq=np.where(freq==max(freq))
            bestpixel=pixels[searchfreq]       
    #In order to see the histograms
    #pl.hist(dataraw,bins=50)
    #pl.title('Histogram of '+str(file))
    #pl.show()

    data[filetxt.index(file),:]=bestpixel,temp[0]

#3) Plot data (not -999)
logicop=np.where(data[:,1]>-300)
x=data[logicop]
#print x

#4) Least minimum squares and plot
p,V=np.polyfit(x[:,0],x[:,1],1,cov=True)
print("Pendiente: {} +/- {}".format(p[0],np.sqrt(V[0,0])))
print("Ordenada : {} +/- {}".format(p[1],np.sqrt(V[1,1])))
xval=np.linspace(-1000,3000)
yval=xval*p[0]+p[1]

pl.plot(xval,yval,'r')
pl.plot(x[:,0],x[:,1],'ob')
pl.xlabel('Mean raw data')
pl.ylabel("Temperature")
pl.show()

#Significant digits (figures)
p[0]=round(p[0],contador(np.sqrt(V[0,0]),0))
p[1]=round(p[1],contador(np.sqrt(V[1,1]),0))

dictio=dict(Slope=p.tolist()[0],
        Term=p.tolist()[1],
)

#5) Save parameters to yaml file and then a ros node to subscribe to the data raw,charge yaml
#file and obtain direct temperatures
yaml.dump(dictio,open('regresion.yaml','w'))
