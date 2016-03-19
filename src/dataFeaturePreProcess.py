'''
Created on May 27, 2015
MySQLdb module Test and Data PreProcess
@author: muyanmoyang
@version: 1.0
'''
import MySQLdb
from numpy import *
import time
import datetime
import string
from locale import atoi
from drawpots import drawPot
import numpy as np
    
    
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
    cur=conn.cursor()
     
    conn.select_db('tianchi_data_season2_period2')
 
    count=cur.execute('select report_date,total_redeem_amt from user_profile_purchase_and_redeem_by_day_p2 where report_date>=20140801 and report_date<=20140831')
    print 'there has %s rows record' % count
 
    result=cur.fetchone()
 
    results=cur.fetchmany(count)
#    print results
#    for r in results:
#        print r
    print '=='*10
    cur.scroll(0,mode='absolute')
 
    conn.commit()
    cur.close()
    conn.close()
 
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def transformDateFormat():
    m =  shape(results)[0]
    finalDate = mat(zeros((m+1,1)))
    finalDateStr = range(0,153)
    month = range(0,153)
    day = range(0,153)
    finalDate[0,0] = result[0]
    
    for i in range(m):
        finalDate[i+1,0] = '%d' %array(results)[i][0]
        str = list('%d' %array(finalDate[i,0]))
        month[i] = str[4] + str[5]
        day[i] = str[6] + str[7]
    month[m] = list('%d' %array(finalDate[m,0]))[4] + list('%d' %array(finalDate[m,0]))[5] 
    day[m] = list('%d' %array(finalDate[m,0]))[6] + list('%d' %array(finalDate[m,0]))[7]
        
    return month,day
#    print "-------The Final Date--------","\n",finalDate


def  dayForWeek():
    month , day = transformDateFormat();
    m =  shape(results)[0]
    week = range(0,m+1) 
    for i in range(m+1):
        week[i] = datetime.datetime(2014,atoi(month[i]),atoi(day[i])).strftime("%w")
    for i in range(m+1):
        if(week[i] == '0'):
            week[i] = 7
    return week
 
def dataProProcess():
    m =  shape(results)[0]
    returnMat = zeros((m+1,2)) 
    dateFeature = range(0,m+1)
    total_purchase_amt = range(0,m+1)
    count = 1 
    
    week = dayForWeek() ;
    month ,day = transformDateFormat()
#    for i in range(m+1):
#        dateFeature[i] = string.atof(month[i]) +string.atof(day[i])/100 + string.atof(week[i])/1000
    for i in range(m+1):
        if(string.atof(week[i]) % 7 == 0):
            dateFeature[i] = string.atof(week[i]) + (count-1)*7
            count += 1
            continue
        if(count == 1):
            dateFeature[i] = string.atof(week[i])
        if(count >= 2):
            dateFeature[i] = string.atof(week[i]) + (count-1) * 7
        dateFeature[i] = int(dateFeature[i])
        
    total_purchase_amt[0] = result[1] 
    for i in range(m):
        total_purchase_amt[i+1] = array(results)[i][1]
    for i in range(m+1):
        returnMat[i,0] = int(dateFeature[i]) 
        returnMat[i,1] = total_purchase_amt[i] 
#    for i in range(m+1):
#        returnMat[i,0] = (returnMat[i,0] - min) / (max - min)
    return  mat(returnMat)
    
#------------------------main------------------------------
#dateFeature , total_purchase_amt = dataProProcess()
#for i in range(count):
#    print dateFeature[i],total_purchase_amt[i]
returnMat = dataProProcess()
print returnMat
i = 8
fileName = "C:/Users/Administrator/Desktop/season2/period2/user_purchase_and_redeem_table/redeem/" + str(i) + "month.txt"
np.savetxt(fileName,returnMat,fmt='%s',newline='\n')
#drawPot(returnMat)

