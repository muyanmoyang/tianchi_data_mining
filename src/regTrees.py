'''
Created on Feb 4, 2011
Tree-Based Regression Methods
@author: Peter Harrington
'''

# -*- coding:utf-8 -*-


from numpy import *
import numpy as np
from drawpots import drawPot
from dataFeaturePreProcess import dataProProcess

def loadDataSet(fileName):      #general function to parse tab -delimited floats
    dataMat = []                #assume last column is target value
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine) #map all elements to float()
        dataMat.append(fltLine)
    return dataMat

def binSplitDataSet(dataSet, feature, value):
    mat0 = dataSet[nonzero(dataSet[:,feature] > value)[0],:][0]
    mat1 = dataSet[nonzero(dataSet[:,feature] <= value)[0],:][0]
    return mat0,mat1

def regLeaf(dataSet):#returns the value used for each leaf
    return mean(dataSet[:,-1])

def regErr(dataSet):
    return var(dataSet[:,-1]) * shape(dataSet)[0] 

def linearSolve(dataSet):   #helper function used in two places
    m,n = shape(dataSet)
    X = mat(ones((m,n))); Y = mat(ones((m,1)))#create a copy of data with 1 in 0th postion
    X[:,1:n] = dataSet[:,0:n-1]; Y = dataSet[:,-1]#and strip out Y
    xTx = X.T*X
    if linalg.det(xTx) == 0.0:
        raise NameError('This matrix is singular, cannot do inverse,\n\
        try increasing the second value of ops')
    ws = xTx.I * (X.T * Y)
    return ws,X,Y

def modelLeaf(dataSet):#create linear model and return coeficients
    ws,X,Y = linearSolve(dataSet)
    return ws

def modelErr(dataSet):
    ws,X,Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(power(Y - yHat,2))

def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
    tolS = ops[0]; tolN = ops[1]
    #if all the target variables are the same value: quit and return value
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1: #exit cond 1
        return None, leafType(dataSet)
    m,n = shape(dataSet)
    #the choice of the best feature is driven by Reduction in RSS error from mean
    S = errType(dataSet)
    bestS = inf; bestIndex = 0; bestValue = 0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex]):
            mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
            if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): continue
            newS = errType(mat0) + errType(mat1)
            if newS < bestS: 
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    #if the decrease (S-bestS) is less than a threshold don't do the split
    if (S - bestS) < tolS:
        return None, leafType(dataSet) #exit cond 2
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
    if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):  #exit cond 3
        return None, leafType(dataSet)
    return bestIndex,bestValue#returns the best feature to split on
                              #and the value used for that split

def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):#assume dataSet is NumPy Mat so we can array filtering
    feat, val = chooseBestSplit(dataSet, leafType, errType, ops)#choose the best split
    if feat == None: return val #if the splitting hit a stop condition return val
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet, feat, val)
    retTree['left'] = createTree(lSet, leafType, errType, ops)
    retTree['right'] = createTree(rSet, leafType, errType, ops)
    return retTree  

def isTree(obj):
    return (type(obj).__name__=='dict')

def getMean(tree):
    if isTree(tree['right']): tree['right'] = getMean(tree['right'])
    if isTree(tree['left']): tree['left'] = getMean(tree['left'])
    return (tree['left']+tree['right'])/2.0
    
def prune(tree, testData):
    if shape(testData)[0] == 0: return getMean(tree) #if we have no test data collapse the tree
    if (isTree(tree['right']) or isTree(tree['left'])):#if the branches are not trees try to prune them
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
    if isTree(tree['left']): tree['left'] = prune(tree['left'], lSet)
    if isTree(tree['right']): tree['right'] =  prune(tree['right'], rSet)
    #if they are now both leafs, see if we can merge them
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
        errorNoMerge = sum(power(lSet[:,-1] - tree['left'],2)) +\
            sum(power(rSet[:,-1] - tree['right'],2))
        treeMean = (tree['left']+tree['right'])/2.0
        errorMerge = sum(power(testData[:,-1] - treeMean,2))
        if errorMerge < errorNoMerge: 
            print "merging"
            return treeMean
        else: return tree
    else: return tree
    
def regTreeEval(model, inDat):
    return float(model)

def modelTreeEval(model, inDat):
    n = shape(inDat)[1]
    X = mat(ones((1,n+1)))
    X[:,1:n+1]=inDat
    return float(X*model)

def treeForeCast(tree, inData, modelEval=regTreeEval):
    if not isTree(tree): return modelEval(tree, inData)
    if inData[tree['spInd']] > tree['spVal']:
        if isTree(tree['left']): return treeForeCast(tree['left'], inData, modelEval)
        else: return modelEval(tree['left'], inData)
    else:
        if isTree(tree['right']): return treeForeCast(tree['right'], inData, modelEval)
        else: return modelEval(tree['right'], inData)
        
def createForeCast(tree, testData, modelEval=regTreeEval):
    m=len(testData)
    yHat = mat(zeros((m,1)))
    for i in range(m):
        yHat[i,0] = treeForeCast(tree, mat(testData[i]), modelEval)
    return yHat

# --------------------------main------------------------------------

'''
trainMat = mat(loadDataSet("E:/machine learning py/regTrees/bikeSpeedVsIq_train.txt")) 
testMat = mat(loadDataSet("E:/machine learning py/regTrees/bikeSpeedVsIq_test.txt"))
'''
'''
# regTree 
myTree = createTree(trainMat, ops=(1,20))
yHat = createForeCast(myTree,testMat[:,0])
print yHat
print corrcoef(yHat,testMat[:,1],rowvar=0)[0,1]
'''

# modelTree
'''
yHat = createForeCast(myTree,testMat[:,0],modelTreeEval)
print yHat
print corrcoef(yHat,testMat[:,1], rowvar=0)[0,1]
'''
'''
# linearReg
yHat = mat(zeros((len(testMat),1)))
ws , x , y = linearSolve(trainMat)
print ws
for i in range(shape(testMat)[0]):
    yHat[i] = testMat[i,0] * ws[1,0] + ws[0,0] 
print yHat
print corrcoef(yHat,testMat[:,1], rowvar=0)[0,1]
'''
'''
for i in range(4):
    trainMat = mat(loadDataSet("C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table/redeem/" + str(i+4) + "month.txt"))
    testMat = mat(loadDataSet("H:/regTrees/bbb.txt"))
    myTree = createTree(trainMat, modelLeaf,modelErr,(0.1,3))
#   print myTree
    yHat = createForeCast(myTree,testMat[:,0],modelTreeEval)
    fileName = "C:/Users/Administrator/Desktop/season2/period2/results/redeem_small_fit/modelTree/" + str(i+4) + "month.txt"
    np.savetxt(fileName,yHat,fmt='%s',newline='\n')
    print yHat

# --------------------bug-------------------------------------------   
trainMat = mat(loadDataSet("C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table/redeem/8month.txt"))
testMat = mat(loadDataSet("H:/regTrees/bbb.txt"))
myTree = createTree(trainMat, modelLeaf,modelErr,(0.1,3))
#   print myTree
yHat = createForeCast(myTree,testMat[:,0],modelTreeEval)
fileName = "C:/Users/Administrator/Desktop/season2/period2/results/redeem_small_fit/modelTree/8month.txt"
np.savetxt(fileName,yHat,fmt='%s',newline='\n')
print yHat
'''

'''
for i in range(4):
    trainMat = mat(loadDataSet("C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table/redeem/"+str(i+4)+"month.txt"))
    testMat = mat(loadDataSet("H:/regTrees/bbb.txt"))  
    myTree = createTree(trainMat,ops=(0.1,2))
#   print myTree
    yHat = createForeCast(myTree,testMat[:,0])
    fileName = "C:/Users/Administrator/Desktop/season2/period2/results/redeem_small_fit/regTree/" + str(i+4) + "month.txt"
    np.savetxt(fileName,yHat,fmt='%s',newline='\n')
#    print yHat

#--------------------------------------bug----------------------------------------------------------
trainMat = mat(loadDataSet("C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table/redeem/8month.txt"))
testMat = mat(loadDataSet("H:/regTrees/bbb.txt"))  
myTree = createTree(trainMat,ops=(0.1,2))
yHat = createForeCast(myTree,testMat[:,0])
fileName = "C:/Users/Administrator/Desktop/season2/period2/results/redeem_small_fit/regTree/8month.txt"
np.savetxt(fileName,yHat,fmt='%s',newline='\n')
'''

