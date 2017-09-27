# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 04:46:56 2017

@author: Frank
"""
import os,sys
from colorific import palette
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# Millisecond Time
def getCurrentTime():
    return int(round(time.time() * 1000))
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

# Get curdir
curdir = os.getcwd()

if __name__ == "__main__":
    print(sys.argv[1])
    full_path = resource_path(os.path.join(curdir,sys.argv[1]))
    p = palette.extract_colors(full_path)
    count = len(p.colors)
    
    img = mpimg.imread(full_path)   
    palette = np.empty((10,count*10,3))
    for i,c in enumerate(p.colors):
        start = i * 10
        end = (i + 1) * 10
        palette[:,start:end,0] = np.ones([10,10])*c.value[0]/255.0
        palette[:,start:end,1] = np.ones([10,10])*c.value[1]/255.0
        palette[:,start:end:,2] = np.ones([10,10])*c.value[2]/255.0
        
    fig = plt.figure()
    a=fig.add_subplot(1,2,1)
    imgplot = plt.imshow(img)
    a.set_title('Image')
    a=fig.add_subplot(1,2,2)
    imgplot = plt.imshow(palette)
    a.set_title('Palatte')
        #ax[i].imshow(img[0,...,0], aspect="auto")
    #fig.tight_layout()
    
