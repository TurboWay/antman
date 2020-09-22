#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/12 1:39
# @Author : way
# @Site : 
# @Describe:

import os
import numpy as np
import tensorflow as tf
from PIL import Image
from string import digits, ascii_lowercase


class Predict(object):
    def __init__(self):
        self.cnn = tf.keras.models.load_model('./model.h5')
        self.characters = list(digits + ascii_lowercase)

    def predict(self, image_path):
        # 以黑白方式读取图片
        img = Image.open(image_path).resize((140, 45)).convert('L')
        img_arr = np.reshape(img, (140, 45, 1)) / 255.0
        x = np.array([img_arr])

        # API refer: https://keras.io/models/model/
        y = self.cnn.predict(x)

        # 因为x只传入了一张图片，取y[0]即可
        # np.argmax()取得最大值的下标，即代表的数字
        print(image_path)
        print(y)
        print('        -> Predict digit', ''.join([self.characters[np.argmax(i)] for i in y[0]]))


if __name__ == "__main__":
    app = Predict()
    for path in os.listdir('./test'):
        app.predict(f'./test/{path}')
