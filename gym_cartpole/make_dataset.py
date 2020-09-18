#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/18 11:31
# @Author : way
# @Site : 
# @Describe:

import time
import gym
import random
import h5py
import numpy as np

env = gym.make("CartPole-v0")  # 加载游戏环境


def game():
    state = env.reset()
    states, actions, score = [], [], 0
    while True:
        # time.sleep(0.1)
        # env.render()  # 显示画面
        action = random.randint(0, 1)  # 随机选择一个动作 0 或 1
        states.append(state)
        actions.append([1, 0] if action == 0 else [0, 1])
        state, reward, done, _ = env.step(action)  # 执行这个动作
        score += reward  # 每回合的得分
        if done:  # 游戏结束
            return states, actions, score


states_data, actions_data = [], []
for _ in range(50000):
    states, actions, score = game()
    if score > 100:
        states_data += states
        actions_data += actions

print(f"位置数量：{len(states_data)}, 动作数量：{len(actions_data)}")

with h5py.File('./data.h5', 'w') as f:
    f.create_dataset('states', data=np.array(states_data))
    f.create_dataset('actions', data=np.array(actions_data))

env.close()
