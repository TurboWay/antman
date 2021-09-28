#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/12 1:09
# @Author : way
# @Site : 
# @Describe:

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import datasets, layers, models


class DataSource(object):
    def __init__(self):
        # mnist数据集存储的位置，如果不存在将自动下载
        # data_path = os.path.abspath(os.path.dirname(__file__)) + '/data_source/mnist.npz'
        # (train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data(path=data_path)

        # 使用自己制作的数据集
        with np.load('./data_source/my_mnist.npz') as f:
            train_images, train_labels = f['train_images'], f['train_labels']
            test_images, test_labels = f['test_images'], f['test_labels']

        # 6万张训练图片，1万张测试图片
        train_images = train_images.reshape((-1, 28, 28, 1))
        test_images = test_images.reshape((-1, 28, 28, 1))
        # 归一化
        train_images, test_images = train_images / 255.0, test_images / 255.0
        # 标签转为独热编码
        train_labels = tf.one_hot(train_labels, 10)
        test_labels = tf.one_hot(test_labels, 10)

        self.train_images, self.train_labels = train_images, train_labels
        self.test_images, self.test_labels = test_images, test_labels


class CNN(object):
    def __init__(self):
        self.model = models.Sequential([
            # 第1层卷积，卷积核大小为3*3，32个，28*28为待训练图片的大小
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
            layers.MaxPooling2D((2, 2)),
            # 第2层卷积，卷积核大小为3*3，64个
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            # 第3层卷积，卷积核大小为3*3，64个
            # layers.Conv2D(64, (3, 3), activation='relu'),
            # layers.MaxPooling2D((2, 2)),

            layers.Flatten(),
            layers.Dense(32, activation='relu'),
            layers.Dense(10, activation='softmax')
        ])
        self.model.summary()
        self.model.compile(optimizer='adam',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])
        if os.path.exists('./model/checkpoint'):
            latest = tf.train.latest_checkpoint('./model')
            self.model.load_weights(latest)
            print(f"{self.model} 模型加载成功")

    def train(self, epochs):
        self.data = DataSource()
        print(f"{self.data} 数据集加载成功，开始训练...")

        check_path = './model/cp-{epoch:04d}.ckpt'
        Checkpoint = tf.keras.callbacks.ModelCheckpoint(check_path, save_weights_only=True, verbose=1)
        for _ in range(epochs):
            history = self.model.fit(self.data.train_images, self.data.train_labels, epochs=1,
                                     callbacks=[Checkpoint])
            train_loss, train_acc = history.history['loss'][0], history.history['accuracy'][0]
            test_loss, test_acc = self.model.evaluate(self.data.test_images, self.data.test_labels)
            with open('log.csv', 'a', encoding='utf-8') as f:
                f.write(f'{train_loss}, {train_acc}, {test_loss}, {test_acc}\n')

    def test(self):
        test_loss, test_acc = self.model.evaluate(self.data.test_images, self.data.test_labels)
        print("准确率: %.4f，共测试了%d张图片 " % (test_acc, len(self.data.test_labels)))


if __name__ == "__main__":
    app = CNN()
    app.train(epochs=97)
    app.test()
