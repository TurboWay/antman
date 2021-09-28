#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/27 20:33
# @Author : way
# @Site : 
# @Describe: 制作数据集

import os
from PIL import Image
import numpy as np

train_images, train_labels = [], []
test_images, test_labels = [], []

for i, img_path in enumerate(os.listdir('imgs')):
    # 标签
    label = img_path.split('_')[0]
    # 以黑白方式读取图片
    img = Image.open(f'imgs/{img_path}').convert('L')
    img_arr = 255 - np.asarray(img)

    # 每个 label 取 1000 个作为测试集
    if test_labels.count(label) < 1000:
        test_images.append(img_arr)
        test_labels.append(label)
    else:
        train_images.append(img_arr)
        train_labels.append(label)

# 保存数据集
np.savez_compressed('my_mnist.npz',
                    train_images=np.array(train_images,dtype='uint8'),
                    train_labels=np.array(train_labels,dtype='uint8'),
                    test_images=np.array(test_images,dtype='uint8'),
                    test_labels=np.array(test_labels,dtype='uint8'))

# 读取数据集
with np.load("my_mnist.npz") as f:
    train_images, train_labels = f['train_images'], f['train_labels']
    test_images, test_labels = f['test_images'], f['test_labels']
    print(len(train_labels), len(test_labels))
