# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 03:52:24 2017

@author: Frank

ref: https://github.com/ArunMichaelDsouza/tensorflow-image-detection
     https://github.com/pyinstaller/pyinstaller
     https://pyinstaller.readthedocs.io/en/latest/usage.html
     https://irwinkwan.com/2013/04/29/python-executables-pyinstaller-and-a-48-hour-game-design-compo/
usage: pyinstaller classify.py
       pyinstaller classify.spec
       
"""
import tensorflow as tf
import sys
import os
#import cv2

# Get curdir
curdir = os.getcwd()

# Code for pyInstaller
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

image_path = sys.argv[1]

# Read the image_data
image_data = tf.gfile.FastGFile(resource_path(os.path.join(curdir,image_path)), 'rb').read()#cv2.imread(r'test/42.jpg')#
#cv2.imshow("test",image_data)
#cv2.waitKey(1000)

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile(resource_path(os.path.join(curdir,"tf_files/retrained_labels.txt")))]


# Unpersists graph from file
with tf.gfile.FastGFile(resource_path(os.path.join(curdir,"tf_files/retrained_graph.pb")), 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})
    
    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        print('%s (score = %.5f)' % (human_string, score))