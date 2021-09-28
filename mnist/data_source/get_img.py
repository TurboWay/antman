#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/27 19:19
# @Author : way
# @Site : 
# @Describe: 反向生成mnist原始图片

import os
from PIL import Image
from tensorflow.keras import datasets

if not os.path.exists('imgs'):
    os.mkdir('imgs')


def gen_image(index, arr, label):
    # 直接保存 arr，是黑底图片，255 - arr 是白底图片
    img = Image.fromarray(255 - arr)
    # 存储图片时，label_index的格式，方便在制作数据集时，从文件名即可知道label
    # img.show()
    img.save("imgs/{}_{}.png".format(label, index))


# mnist数据集存储的位置，如果不存在将自动下载
(x_train, y_train), (x_test, y_test) = datasets.mnist.load_data(path='minist.npz')

# 6万张训练集图片
for idx, (arr, label) in enumerate(zip(x_train, y_train), 1):
    gen_image(idx, arr, label)

# 1万张测试集图片
for idx, (arr, label) in enumerate(zip(x_test, y_test), 60001):
    gen_image(idx, arr, label)
