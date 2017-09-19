#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 18:37:57 2017

@author: ubuntu
"""
from tf_unet import image_util
from tf_unet import unet
import matplotlib.pyplot as plt

testpath="/media/ubuntu/Investigation/DataSet/Image/UNet/DRIVE/test/merged/*"
data_provider = image_util.ImageDataProvider(testpath, data_suffix='_test.jpg', mask_suffix='_manual1.png')
#data_provider.n_class = 3
net = unet.Unet(channels=1, n_class=2, layers=4, features_root=64)
#
test_number=20

import tensorflow as tf
import numpy as np

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    net.restore(sess,"./unet_trained/model.cpkt")
    
    for i in range(1,test_number):
        x_test, y_test = data_provider(i)
        y_dummy = np.empty((x_test.shape[0], x_test.shape[1], x_test.shape[2], net.n_class))
        prediction = sess.run(net.predicter, feed_dict={net.x: x_test, net.y: y_dummy, net.keep_prob: 1.})
        
        fig, ax = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(12,5))
        ax[0].imshow(x_test[0,...,0], aspect="auto")
        ax[1].imshow(y_test[0,...,1], aspect="auto")
        mask = prediction[0,...,1] > 0.9
        ax[2].imshow(mask, aspect="auto")
        ax[0].set_title("Input")
        ax[1].set_title("Ground truth")
        ax[2].set_title("Prediction")
        fig.tight_layout()
        fig.savefig("prediction.png")