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
                # 第1层卷积，卷积核大小为3*3，32个，28*28为待训练图片的大小
                layers.Conv2D(32, (3, 3), activation='relu', input_shape=(20, 20, 1)),
                layers.MaxPooling2D((2, 2)),
                # 第2层卷积，卷积核大小为3*3，64个
                layers.Conv2D(64, (3, 3), activation='relu'),
                layers.MaxPooling2D((2, 2)),
                # 第3层卷积，卷积核大小为3*3，64个
                layers.Conv2D(64, (3, 3), activation='relu'),
                layers.MaxPooling2D((2, 2)),
                layers.Flatten(),
                layers.Dense(64, activation='relu'),
                layers.Dense(10, activation='softmax'),
            ])
        self.model.summary()

        # 读取数据
        with h5py.File('./data_source/data.h5', 'r') as f:
            self.train_images = f['train_images'][()]
            self.train_labels = f['train_labels'][()]
            self.test_images = f['test_images'][()]
            self.test_labels = f['test_labels'][()]

        self.train_images = self.train_images.reshape((-1, 20, 20, 1))
        self.train_labels = self.train_labels
        self.test_images = self.test_images.reshape((-1, 20, 20, 1))
        self.test_labels = self.test_labels

        # 数据处理 归一化
        self.train_images = 1 - self.train_images / 255.0
        self.test_images = 1 - self.test_images / 255.0

    def train(self):
        # 可视化 tensorboard --logdir=C:\GitHub\antman\glidedsky\logs
        TensorBoardcallback = tf.keras.callbacks.TensorBoard(
            log_dir='logs',
            histogram_freq=1,
            write_graph=True,
            write_images=True,
            update_freq=10000
        )
        self.model.compile(optimizer='Adam',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])
        self.model.fit(self.train_images, self.train_labels, epochs=10, callbacks=[TensorBoardcallback])
        self.model.save(self.modelpath)

    def test(self):
        test_loss, test_acc = self.model.evaluate(self.test_images, self.test_labels)
        print("准确率: %.4f，共测试了%d张图片 " % (test_acc, len(self.test_labels)))


if __name__ == "__main__":
    app = Train()
    app.train()
    app.test()
