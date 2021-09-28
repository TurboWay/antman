#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/28 10:29
# @Author : way
# @Site : 
# @Describe: 线性回归模型做预测

from sklearn.linear_model import LinearRegression

x = [
    [2011], [2012], [2013], [2014], [2015], [2016], [2017], [2018], [2019], [2020]
]
y = [5.7, 9.6, 15.5, 17.9, 20, 25.3, 34, 39, 50.1, 51]

model = LinearRegression()
model.fit(x, y)
print(f'模型评分：{model.score(x, y)}')
predict_y = model.predict([[2021,]])
print(f'2021年预测值：{predict_y[0]}')
print(f'未来十年预测值：{ model.predict([[2021+i] for i in range(10)])}')

# 画图
import matplotlib.pyplot as plt
plt.scatter([i[0] for i in x], y, color='blue')
plt.plot([i[0] for i in x], model.predict(x), color='red')
plt.show()

import joblib
# 模型保存、加载
joblib.dump(model, 'model.pickle')  # 保存
print('模型保存成功')
model = joblib.load('model.pickle')  # 载入
print('模型加载成功...')
print('模型预测:', model.predict([[2021,]]))
