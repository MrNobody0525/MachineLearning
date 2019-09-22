from math import log
import operator
import matplotlib.pyplot as plt
import csv
import random
import numpy as np
import pickle

def creatDataset():
    dataSet = []
    data = np.loadtxt("D:\\\python\\treeplotter\\adult.csv", str, delimiter=",")[random.randint(1,100):random.randint(100,150)]
    data_row = [0, 3, 4, 14]
    data = data[:, data_row]
    labels = ['age', 'education', 'education-num']	
    for x in data:
        x = list(x)
        x[0] = int(x[0])
        if int(x[0])>10 and int(x[0])<=20:
            x[0] = "10~20"
        elif int(x[0])>20 and int(x[0])<=30:
            x[0] = "20~30"
        elif int(x[0])>30 and int(x[0])<=40:
            x[0] = "30~40"
        elif int(x[0])>40 and int(x[0])<=50:
            x[0] = "40~50"
        else:
            x[0] = "50+"
        x[2] = int(x[2])
        if int(x[2])>0 and int(x[2])<=10:
            x[2] = "0~10"
        elif int(x[2])>10 and int(x[2])<=20:
            x[2] = "10~20"
        dataSet.append(x)
    print(dataSet)
    return dataSet, labels


def calcShannonEnt(dataSet):
    numEntries = len(dataSet)                          
    labelCounts = {}
    for featVec in dataSet:                             
        currentLabel = featVec[-1]                     
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:                            #计算香农熵
        prob = float(labelCounts[key])/numEntries      # 计算该类别的概率
        shannonEnt -= prob * log(prob,2)               # 利用公式，计算熵
    return shannonEnt

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:                    ##遍历数据集
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     #删掉axis的特征，保留剩下的特征并存到retDataSet
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
    
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1      #特征数
    baseEntropy = calcShannonEnt(dataSet)  #计算香农熵
    bestInfoGain = 0.0;                 #初始化最大信息增益变量
    bestFeature = -1
    for i in range(numFeatures):        #遍历所有特征
        featList = [example[i] for example in dataSet]#取所有样本的第一个特征
        uniqueVals = set(featList)       #去重复值
        newEntropy = 0.0
        for value in uniqueVals:        #按照第i个特征划分数据下的香农熵，信息增益
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)     
        infoGain = baseEntropy - newEntropy     # 信息增益
        #print("第%d个特征的增益为%.3f" % (i, infoGain))
        if (infoGain > bestInfoGain):       #选择最大增益的特征索引
            bestInfoGain = infoGain         
            bestFeature = i
    return bestFeature                      

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]  #取数据集的类别标签
    if classList.count(classList[0]) == len(classList): 
        return classList[0]   #递归停止条件一：如果类别完全相同则停止继续划分
    if len(dataSet[0]) == 1:   #递归停止条件二：遍历完所有特征时返回出现次数最多的类标签
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet) #选择最优特征
    bestFeatLabel = labels[bestFeat]             # #最优特征的标签
    myTree = {bestFeatLabel:{}}             #根据最优特征的标签生成树
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]       #复制标签，递归创建决策树
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)
    return myTree                            

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#测试该结点是否为字典，如果不是字典，代表此结点为叶子结点
            numLeafs += getNumLeafs(secondDict[key])
        else:   numLeafs +=1
    return numLeafs


def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#测试该结点是否为字典，如果不是字典，代表此结点为叶子结点
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:   thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth
    return maxDepth

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    arrow_args = dict(arrowstyle="<-")        #定义箭头格式
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',
             xytext=centerPt, textcoords='axes fraction',
             va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)
  

def plotTree(myTree, parentPt, nodeTxt):
    decisionNode = dict(boxstyle="sawtooth", fc="0.8")                                        #设置结点格式
    leafNode = dict(boxstyle="round4", fc="0.8")                                            #设置叶结点格式    
    numLeafs = getNumLeafs(myTree) 
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]  
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)  #中心位置
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD             #y偏移
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#测试该结点是否为字典，如果不是字典，代表此结点为叶子结点  
            plotTree(secondDict[key],cntrPt,str(key))       
        else:  
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW  #不是叶结点，递归调用继续绘制
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))#如果是叶结点，绘制叶结点，并标注有向边属性值
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()                                                #清空fig
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops) #去掉x、y轴
    #createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses 
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0
    plotTree(inTree, (0.5,1.0), '')
    plt.show()    

def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]                                                      #获取决策树结点
    secondDict = inputTree[firstStr]                                                        #下一个字典
    featIndex = featLabels.index(firstStr)                                               
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else: classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree, filename):
    with open(filename, 'wb') as fw:
        pickle.dump(inputTree, fw)


def grabTree(filename):
    fr = open(filename, 'rb')
    return pickle.load(fr)    

def run():
    dataSet, labels = creatDataset()
    tree  = createTree(dataSet, labels)
    print(tree)
    createPlot(tree)

run()
