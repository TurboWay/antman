#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/9/18 19:35
# @Author : way
# @Site : 
# @Describe:
import time
import gym
import numpy as np
from tensorflow.keras import models

env = gym.make('MountainCar-v0')
model = models.load_model('model.h5')
s = env.reset()
score = 0
while True:
    env.render()
    time.sleep(0.01)
    a = np.argmax(model.predict(np.array([s]))[0])
    s, reward, done, _ = env.step(a)
    score += reward
    if done:
        print('score:', score)
        break
env.close()
