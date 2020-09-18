#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/12 1:09
# @Author : way
# @Site : 
# @Describe:

import os
import h5py
import tensorflow as tf
from tensorflow.keras import layers, models


class Train:
    def __init__(self):
        # 最终模型存放路径
        self.modelpath = './model.h5'

        # 定义模型
        if os.path.exists(self.modelpath):
            self.model = tf.keras.models.load_model(self.modelpath)
            print(f"{self.model} 模型加载成功，继续训练...")
        else:
            self.model = models.Sequential([
                layers.Dense(32, input_dim=4, activation='relu'),
                layers.Dense(20, activation='relu'),
                layers.Dense(2, activation='linear')
            ])
        self.model.summary()

        # 读取数据
        with h5py.File('./data.h5', 'r') as f:
            self.states = f['states'][()]
            self.actions = f['actions'][()]

    def train(self):
        self.model.compile(optimizer='Adam', loss='mse')
        self.model.fit(self.states, self.actions, epochs=10)
        self.model.save(self.modelpath)


if __name__ == "__main__":
    app = Train()
    app.train()
