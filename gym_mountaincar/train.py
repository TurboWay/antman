#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/18 14:04
# @Author : way
# @Site : 
# @Describe:

import time
import random
import pickle
import gym
import numpy as np
from collections import defaultdict

env = gym.make('MountainCar-v0')
Q = defaultdict(lambda: [0, 0, 0])


def transform_state(state):
    """
    :param state:
    :return: 坐标归一化 映射到 [0, 40]
    """
    pos, v = state
    pos_low, v_low = env.observation_space.low
    pos_high, v_high = env.observation_space.high
    a = 40 * (pos - pos_low) / (pos_high - pos_low)
    b = 40 * (v - v_low) / (v_high - v_low)
    return int(a), int(b)


lr, factor = 0.7, 0.95
episodes = 10000  # 训练10000次
score_list = []  # 记录所有分数
for i in range(episodes):
    s = transform_state(env.reset())
    score = 0
    while True:
        a = np.argmax(Q[s])
        # 训练刚开始，多一点随机性，以便有更多的状态
        if np.random.random() > i * 3 / episodes:
            a = np.random.choice([0, 1, 2])
        # 执行动作
        next_s, reward, done, _ = env.step(a)
        next_s = transform_state(next_s)
        # 根据上面的公式更新Q-Table
        Q[s][a] = (1 - lr) * Q[s][a] + lr * (reward + factor * max(Q[next_s]))
        score += reward
        s = next_s
        if done:
            score_list.append(score)
            print('episode:', i, 'score:', score, 'max:', max(score_list))
            break
env.close()

with open('model.pickle', 'wb') as f:
    pickle.dump(dict(Q), f)
    print('model saved')
