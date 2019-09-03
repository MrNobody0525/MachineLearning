#Logistic回归

涉及的Sigmoid函数以及梯度上升法或梯度下降法的最优化方法不在此处讲解。

##函数介绍

	loadDataSet():
打开文本 文件testSet.txt并逐行读取

	sigmoid():
sigmoid函数

	gradAscent():
梯度上升算法，返回真实类别与预测类别的差值

	plotBestFit():
画出数据集和Logistic回归最佳拟合直线的函数

	stocGradAscent0(dataMatrix,classLabels，numIter = 150):
优化随机梯度上升算法，与梯度上升算法相似但不同

##实例测试算法：从疝气病症预测病马的死亡率 

用Logistic回归进行分类

	classifyVector(inX,weights):

以回归系数和特征向量作为输入来计 算对应的Sigmoid值。如果Sigmoid值大于0.5函数返回1，否则返回0。 

	colicTest():
打开测试集和训练集，并对数据进行格式化处理的 函数

	multiTest():
调用函数colicTest()10次并求结果的平均值。 
