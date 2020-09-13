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

images = []
labels = []

for path in os.listdir('./imgs'):
    label = int(path.split('_')[0])
    label_one_hot = [0 if i != label else 1 for i in range(10)]
    labels.append(label_one_hot)

    img = Image.open('./imgs/' + path).resize((20, 20)).convert('L')
    img_arr = 1 - np.reshape(img, 20 * 20) / 255.0
    images.append(img_arr)


with h5py.File('./data.h5', 'w') as f:
    f.create_dataset('images', data=np.array(images))
    f.create_dataset('labels', data=np.array(labels))
