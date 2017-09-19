#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 18:35:40 2017

@author: frank

https://github.com/jakeret/tf_unet/issues/37

#IN:channels=1
#LN:layers=4
#L1:features_root=64
#OP:optimizer='adam'
#training_iters=30
#epochs=50
#OUT:n_class=2
---
input data:color->gray
mask data:->threshold
---
a_min=0
a_max=255
---
I think the size and number of network,that's,features_root and layers should
be increase according to the size of channel and image.
training_iters, optimizer, epochs should be set while testing.
---
After training,restart python
"""

from tf_unet import image_util
from tf_unet import unet

search_path = '/media/ubuntu/Investigation/DataSet/Image/UNet/DRIVE/training/merged/*'
data_provider = image_util.ImageDataProvider(search_path, data_suffix='_training.jpg', mask_suffix='_manual1.png')
#data_provider.n_class = 3
net = unet.Unet(channels=data_provider.channels, n_class=data_provider.n_class, layers=4, features_root=64)

trainer = unet.Trainer(net, optimizer='adam')#"momentum", opt_kwargs=dict(momentum=0.2))#, optimizer='adam')

path = trainer.train(data_provider, "./unet_trained", training_iters=30, epochs=50, display_step=2)