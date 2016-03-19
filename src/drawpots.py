from numpy import *
import operator
from os import listdir
# -*- coding: cp936 -*-

def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file
    returnMat = zeros((numberOfLines,2))        #prepare matrix to return
    
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:2]
        index += 1
    return returnMat


def drawPot1(returnMat):
    import matplotlib
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.scatter(returnMat[:,0],returnMat[:,1])
#    plt.xlabel('x1'); plt.ylabel('x2');
#    plt.show()    
    plot = plt.plot(returnMat[:,0], returnMat[:,1], c='red')# use pylab to plot x and y : Give your plots names    
    plt.title('The Purchase of Result')# give plot a title
    plt.xlabel('x axis')# make axis labels
    plt.ylabel('y axis')
    plt.xlim([0,40])# set axis limits
#    plt.ylim(300000000, 1500000000)
    plt.legend([plot], ('red line', 'green circles'), 'best', numpoints=1)# make legend
    plt.show()# show the plot on the screen




def drawPot(returnMat1,returnMat2,returnMat3,returnMat4,returnMat5):
    import matplotlib
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.scatter(returnMat1[:,0],returnMat1[:,1])
    ax.scatter(returnMat2[:,0],returnMat2[:,1])
    ax.scatter(returnMat3[:,0],returnMat3[:,1])
    ax.scatter(returnMat4[:,0],returnMat4[:,1])
    ax.scatter(returnMat5[:,0],returnMat5[:,1])
    
#    plt.xlabel('x1'); plt.ylabel('x2');
#    plt.show()
    
    plot1 = plt.plot(returnMat1[:,0], returnMat1[:,1], c='red')# use pylab to plot x and y : Give your plots names
    plot2 = plt.plot(returnMat2[:,0], returnMat2[:,1], c='green')# use pylab to plot x and y : Give your plots names
    plot3 = plt.plot(returnMat3[:,0], returnMat3[:,1], c='blue')# use pylab to plot x and y : Give your plots names
    plot4 = plt.plot(returnMat4[:,0], returnMat4[:,1], c='yellow')# use pylab to plot x and y : Give your plots names
    plot5 = plt.plot(returnMat5[:,0], returnMat5[:,1], c='black')# use pylab to plot x and y : Give your plots names
    
#   plt.title('The total_purchase of ' + str(i) + 'month')# give plot a title
    plt.title('The Redeem Comparation of 4,5,6,7,8 month')# give plot a title
    plt.xlabel('x axis')# make axis labels
    plt.ylabel('y axis')
#    plt.xlim([0,40])# set axis limits
#    plt.ylim(300000000, 1500000000)
    plt.legend([plot1,plot2,plot3,plot4,plot5], ('red line', 'green circles'), 'best', numpoints=1)# make legend
    plt.show()# show the plot on the screen
    
    
'''--------------------------------------------main--------------------------------------------------'''
#returnMat = file2matrix("C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table/purchase/"+ str(i)+"month.txt")
#returnMat1 = file2matrix("C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table_noProcessing/redeem/4month.txt")
#returnMat2 = file2matrix("C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table_noProcessing/redeem/5month.txt")
#returnMat3 = file2matrix("C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table_noProcessing/redeem/6month.txt")
#returnMat4 = file2matrix("C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table_noProcessing/redeem/7month.txt")
#returnMat5 = file2matrix("C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table_noProcessing/redeem/8month.txt")
#drawPot(returnMat1,returnMat2,returnMat3,returnMat4,returnMat5) 

#i = 8
#returnMat = file2matrix("C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table/purchase/"+ str(i)+"month.txt")
#drawPot1(returnMat) 

returnMat = file2matrix("C:/Users/Administrator/Desktop/redeem_result.txt")
drawPot1(returnMat)


