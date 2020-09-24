#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/12 1:09
# @Author : way
# @Site : 
# @Describe:

import os
import tensorflow as tf
from tensorflow.keras import datasets, layers, models


class CNN(object):
    def __init__(self):
        model = models.Sequential([
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

        model.summary()

        self.model = model


class DataSource(object):
    def __init__(self):
        # mnist数据集存储的位置，如何不存在将自动下载
        data_path = os.path.abspath(os.path.dirname(__file__)) + '/data_source/mnist.npz'
        (train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data(path=data_path)
        # 6万张训练图片，1万张测试图片
        train_images = train_images.reshape((-1, 28, 28, 1))
        test_images = test_images.reshape((-1, 28, 28, 1))
        # 像素值映射到 0 - 1 之间
        train_images, test_images = train_images / 255.0, test_images / 255.0

        self.train_images, self.train_labels = train_images, train_labels
        self.test_images, self.test_labels = test_images, test_labels


class Train:
    def __init__(self):
        self.cnn = CNN()
        self.cnn.model.compile(optimizer='adam',
                               loss='sparse_categorical_crossentropy',
                               metrics=['accuracy'])
        if os.path.exists('./model/checkpoint'):
            latest = tf.train.latest_checkpoint('./model')
            self.cnn.model.load_weights(latest)
            print(f"{self.cnn.model} 模型加载成功，继续训练...")
        self.data = DataSource()

    def train(self, epochs):
        check_path = './model/cp-{epoch:04d}.ckpt'
        Checkpoint = tf.keras.callbacks.ModelCheckpoint(check_path, save_weights_only=True, verbose=1)
        for _ in range(epochs):
            history = self.cnn.model.fit(self.data.train_images, self.data.train_labels, epochs=1,
                                         callbacks=[Checkpoint])
            train_loss, train_acc = history.history['loss'][0], history.history['accuracy'][0]
            test_loss, test_acc = self.cnn.model.evaluate(self.data.test_images, self.data.test_labels)
            with open('log.csv', 'a', encoding='utf-8') as f:
                f.write(f'{train_loss}, {train_acc}, {test_loss}, {test_acc}\n')

    def test(self):
        test_loss, test_acc = self.cnn.model.evaluate(self.data.test_images, self.data.test_labels)
        print("准确率: %.4f，共测试了%d张图片 " % (test_acc, len(self.data.test_labels)))


def draw():
    """
    :return: 画图
    """
    import matplotlib.pyplot as plt
    with open('log.csv', 'r', encoding='utf-8') as f:
        x, train_acc, test_acc = [], [], []
        for line in f.readlines()[1:]:
            train_acc.append(float(line.split(',')[1]))
            test_acc.append(float(line.split(',')[-1]))
        plt.plot(train_acc, label='train', color='green')
        plt.plot(test_acc, label='test', color='yellow', linestyle='--')
        plt.show()


if __name__ == "__main__":
    app = Train()
    # app.train(epochs=10)
    app.test()
    draw()
