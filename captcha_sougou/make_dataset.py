#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/22 20:06
# @Author : way
# @Site : 
# @Describe:

import os
import h5py
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from string import digits, ascii_lowercase

images = []
labels = []

# 输入：图片尺寸为 140 * 44
# img = Image.open(r"D:\data\sougou_com_Trains\1a1c63_d06b8c3fd606c4ca633c523ac408afc7.jpg")
# print(img.width, img.height)
# img = img.convert('L')
# img.show()

# 输出：6个字母数字，不区分大小写 6 * 36
characters = list(digits + ascii_lowercase)
# print(len(characters), characters)

dir_path = r'D:\data\sougou_com_Trains'
for path in os.listdir(dir_path):
    label = []
    for character in list(path.split('_')[0]):
        character_one_hot = [0 if i != characters.index((character.lower())) else 1 for i in range(36)]
        label.append(character_one_hot)
    labels.append(label)

    img = Image.open(dir_path + '\\' + path).resize((140, 45)).convert('L')
    img_arr = np.reshape(img, 140 * 45)
    images.append(img_arr)

# 拆分训练集、测试集
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.1, random_state=0)

with h5py.File('./data.h5', 'w') as f:
    f.create_dataset('train_images', data=np.array(train_images))
    f.create_dataset('train_labels', data=np.array(train_labels))
    f.create_dataset('test_images', data=np.array(test_images))
    f.create_dataset('test_labels', data=np.array(test_labels))
