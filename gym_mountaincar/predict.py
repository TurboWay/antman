#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/18 18:12
# @Author : way
# @Site : 
# @Describe:

import time
import pickle
import gym
import numpy as np

env = gym.make('MountainCar-v0')

with open('model.pickle', 'rb') as f:
    Q = pickle.load(f)


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


s = transform_state(env.reset())
score = 0
while True:
    env.render()
    time.sleep(0.02)
    a = np.argmax(Q[s])
    # 执行动作
    next_s, reward, done, _ = env.step(a)
    next_s = transform_state(next_s)
    score += reward
    s = next_s
    if done:
        print('score:', score)
        break
env.close()
