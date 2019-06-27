from numpy import *
import operator 
import sklearn.datasets as datasets
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt

def createDataSet():
    # 创建训练集
    iris = datasets.load_iris()

    group = iris['data']

    labels = iris['target']

    X_train,X_test,y_train,y_test = train_test_split(group,labels,test_size = 0.1)
    
    labels_names = iris['target_names']

    return X_train, X_test,y_train,y_test,labels_names
	
def classify(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    result = []
    # 根据欧式距离计算训练集中每个样本到测试点的距离
    for i in inX:

        diffMat = tile(i, (dataSetSize,1)) - dataSet
        sqDiffMat = diffMat**2

        sqDistances = sqDiffMat.sum(axis=1)
        distances = sqDistances**0.5

        # 计算完所有点的距离后，对数据按照从小到大的次序排序
        sortedDistIndicies = distances.argsort()
        # 确定前k个距离最小的元素所在的主要分类，最后返回发生频率最高的元素类别
        classCount={}
        for i in range(k):
            voteIlabel = labels[sortedDistIndicies[i]]
            classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
        sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
        result.append(int(sortedClassCount[0][0]))
    return result

def score(y_test,result):
    i = 0
    count = 0
    while i < 15:
        if y_test[i] == result[i]:
            count +=1
        i+=1
    return float(count/i)

def matshow(X_train,y_train,X_test,y_test):
    plt.figure()
    plt.subplot(121)
    plt.scatter(X_train[:,0],X_train[:,1],\
    c= y_train.reshape(-1))
    plt.subplot(122)
    plt.scatter(X_test[:,0],X_test[:,1],\
    c = y_test.reshape(-1))
    plt.show()


if __name__ == '__main__':
    X_train,X_test,y_train,y_test,labels_names = createDataSet()
    result = classify(X_test,X_train,y_train,10)
    #计算正确率
    matshow(X_train,y_train,X_test,y_test)
    Score = score(y_test,result)
    print("正确率为：",Score)






