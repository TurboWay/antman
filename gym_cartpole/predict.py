#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/18 11:22
# @Author : way
# @Site : 
# @Describe:

import gym
import random
import time
import numpy as np
import tensorflow as tf

env = gym.make("CartPole-v0")  # 加载游戏环境

model = tf.keras.models.load_model('./model.h5')
for i in range(10):
    state = env.reset()
    score = 0
    while True:
        # time.sleep(0.1)
        # env.render()  # 显示画面
        action = np.argmax(model.predict(np.array([state]))[0])  # 预测动作
        state, reward, done, _ = env.step(action)  # 执行这个动作
        score += reward  # 每回合的得分
        if done:  # 游戏结束
            print('score: ', score)  # 打印分数
            break
env.close()
