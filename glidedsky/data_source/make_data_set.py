#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/12 20:06
# @Author : way
# @Site : 
# @Describe:

import os
import h5py
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split

images = []
labels = []

for path in os.listdir('./imgs'):
    label = int(path.split('_')[0])
    label_one_hot = [0 if i != label else 1 for i in range(10)]
    labels.append(label_one_hot)

    img = Image.open('./imgs/' + path).resize((20, 20)).convert('L')
    img_arr = np.reshape(img, 20 * 20)
    images.append(img_arr)

# 拆分训练集、测试集
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.1, random_state=0)

with h5py.File('./data.h5', 'w') as f:
    f.create_dataset('train_images', data=np.array(train_images))
    f.create_dataset('train_labels', data=np.array(train_labels))
    f.create_dataset('test_images', data=np.array(test_images))
    f.create_dataset('test_labels', data=np.array(test_labels))
