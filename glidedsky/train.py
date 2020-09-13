#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/12 1:09
# @Author : way
# @Site : 
# @Describe:

import h5py
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split


class Train:
    def __init__(self):
        # 定义模型
        self.model = models.Sequential([
            # 第1层卷积，卷积核大小为3*3，32个，28*28为待训练图片的大小
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(20, 20, 1)),
            layers.MaxPooling2D((2, 2)),
            # 第2层卷积，卷积核大小为3*3，64个
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            # 第3层卷积，卷积核大小为3*3，64个
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(10, activation='softmax'),
        ])
        self.model.summary()

        # 读取训练数据
        with h5py.File('./data_source/data.h5', 'r') as f:
            images = f['images'][()]
            labels = f['labels'][()]

        self.train_images, self.test_images, self.train_labels, self.test_labels = train_test_split(images, labels,
                                                                                                    test_size=0.1,
                                                                                                    random_state=0)
        self.train_images = self.train_images[:400000].reshape((400000, 20, 20, 1))
        self.train_labels = self.train_labels[:400000]
        self.test_images = self.test_images[:40000].reshape((40000, 20, 20, 1))
        self.test_labels = self.test_labels[:40000]

    def train(self):
        self.model.compile(optimizer='adam',
                           loss=tf.keras.losses.CategoricalCrossentropy(),
                           metrics=['accuracy'])
        self.model.fit(self.train_images, self.train_labels, epochs=8)
        self.model.save('./model.h5')

    def test(self):
        self.model = tf.keras.models.load_model('./model.h5')
        test_loss, test_acc = self.model.evaluate(self.test_images, self.test_labels)
        print("准确率: %.4f，共测试了%d张图片 " % (test_acc, len(self.test_labels)))


if __name__ == "__main__":
    app = Train()
    # app.train()
    app.test()