#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/12 0:29
# @Author : way
# @Site : 
# @Describe:

import os
import tensorflow as tf
import tensorflow.keras.models
import tensorflow.keras.losses
import tensorflow.keras.metrics
import tensorflow.keras.optimizers
import tensorflow.keras.activations

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'  # 只显示 warning 和 Error
tf.add(1, 2).numpy()
hello = tf.constant('Hello, TensorFlow!')
print(hello.numpy().decode())
