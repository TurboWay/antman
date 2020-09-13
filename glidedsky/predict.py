#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/12 1:39
# @Author : way
# @Site : 
# @Describe:

import numpy as np
import tensorflow as tf
from PIL import Image

class Predict(object):
    def __init__(self):
        self.cnn = tf.keras.models.load_model('./model.h5')

    def predict(self, image_path):
        # 以黑白方式读取图片
        img = Image.open(image_path).resize((20, 20)).convert('L')
        img_arr = 1 - np.reshape(img, (20, 20, 1)) / 255.0
        x = np.array([img_arr])

        # API refer: https://keras.io/models/model/
        y = self.cnn.predict(x)

        # 因为x只传入了一张图片，取y[0]即可
        # np.argmax()取得最大值的下标，即代表的数字
        print(image_path)
        print(y[0])
        print('        -> Predict digit', np.argmax(y[0]))

if __name__ == "__main__":
    app = Predict()
    app.predict('./test/0.png')
    app.predict('./test/3.png')
    app.predict('./test/4.png')
    app.predict('./test/7.png')
    app.predict('./test/9.png')
