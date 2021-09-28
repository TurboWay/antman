#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/7 12:25
# @Author : way
# @Site : 
# @Describe: sklearn 模型使用


from sklearn import datasets
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
import joblib

# 加载数据
iris = datasets.load_iris()
iris_X, iris_Y = iris.data, iris.target

# 切分训练集与测试集
X_train, X_test, Y_train, Y_test = train_test_split(iris_X, iris_Y, train_size=0.3, random_state=20)

# 模型使用
models = [
    ['线性回归', LinearRegression()],
    ['逻辑回归', LogisticRegression()],
    ['多项式分布的朴素贝叶斯', MultinomialNB()],
    ['伯努利分布的朴素贝叶斯', BernoulliNB()],
    ['高斯分布的朴素贝叶斯', GaussianNB()],
    ['决策树', DecisionTreeClassifier()],
    ['SVM(支持向量机）', SVC()],
    ['KNN(分类)', KNeighborsClassifier()],
    ['KNN(回归)', KNeighborsRegressor()],
    ['神经网络', MLPClassifier(activation='tanh', solver='adam', alpha=0.0001, learning_rate='adaptive',
                           learning_rate_init=0.001, max_iter=200)],
]

for row in models:
    name, model = row
    model.fit(X_train, Y_train)
    print(f'======================= {name} ============================')
    print('模型评价:', model.score(X_test, Y_test))
    print('预测:', model.predict([X_test[0]]))

# 交叉验证
model = KNeighborsClassifier()
accs = cross_val_score(model, iris_X, iris_Y, cv=10)
print(f'======================= 交叉验证 ============================')
print('交叉验证结果:', accs)

# 模型保存、加载
model = KNeighborsClassifier()
model.fit(X_train, Y_train)
joblib.dump(model, 'model.pickle')  # 保存
print('模型保存成功')
model = joblib.load('model.pickle')  # 载入
print('模型加载成功...')
print('模型预测:', model.predict([X_test[0]]))