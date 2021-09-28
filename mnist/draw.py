#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/28 3:44
# @Author : way
# @Site : 
# @Describe: 画图


import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负

with open('log.csv', 'r', encoding='utf-8') as f:
    train_acc, test_acc = [], []
    for line in f.readlines():
        train_acc.append(float(line.split(',')[1]))
        test_acc.append(float(line.split(',')[-1]))

    best_epoch = test_acc.index(max(test_acc)) + 1

    plt.figure(figsize=(40, 20), dpi=80)
    plt.figure(1)

    ax1 = plt.subplot(221)
    epochs = 3
    ax1.plot(train_acc[:epochs], label='train', color='blue')
    ax1.plot(test_acc[:epochs], label='test', color='red')
    ax1.legend()
    plt.title(f'欠拟合(epochs={epochs},train={train_acc[:epochs][-1]:.2%},test={test_acc[:epochs][-1]:.2%})', fontsize=18)
    plt.xlabel('epochs', fontsize=15)
    plt.ylabel('accuracy', fontsize=15)

    ax2 = plt.subplot(222)
    epochs = best_epoch
    ax2.plot(train_acc[:epochs], label='train', color='blue')
    ax2.plot(test_acc[:epochs], label='test', color='red')
    ax2.legend()
    plt.title(f'拟合(epochs={epochs},train={train_acc[:epochs][-1]:.2%},test={test_acc[:epochs][-1]:.2%})', fontsize=18)
    plt.xlabel('epochs', fontsize=15)
    plt.ylabel('accuracy', fontsize=15)

    ax3 = plt.subplot(223)
    epochs = best_epoch + int((len(train_acc) - best_epoch) / 2)
    ax3.plot(train_acc[:epochs], label='train', color='blue')
    ax3.plot(test_acc[:epochs], label='test', color='red')
    ax3.legend()
    plt.title(f'过拟合(epochs={epochs},train={train_acc[:epochs][-1]:.2%},test={test_acc[:epochs][-1]:.2%})', fontsize=18)
    plt.xlabel('epochs', fontsize=15)
    plt.ylabel('accuracy', fontsize=15)

    ax4 = plt.subplot(224)
    epochs = len(train_acc)
    ax4.plot(train_acc[:epochs], label='train', color='blue')
    ax4.plot(test_acc[:epochs], label='test', color='red')
    ax4.legend()
    plt.title(f'过拟合(epochs={epochs},train={train_acc[:epochs][-1]:.2%},test={test_acc[:epochs][-1]:.2%})', fontsize=18)
    plt.xlabel('epochs', fontsize=15)
    plt.ylabel('accuracy', fontsize=15)

    plt.show()
