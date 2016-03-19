__author__ = 'Pride'
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
x1 = [1, 2, 3, 4, 5]# Make x, y arrays for each graph
y1 = [1, 4, 9, 16, 25]
x2 = [1, 2, 4, 6, 8]
y2 = [2, 4, 8, 12, 16]
plot1 = pl.plot(x1, y1, c='red')# use pylab to plot x and y : Give your plots names
plot2 = pl.plot(x2, y2, 'g')
pl.title('Plot of y vs. x')# give plot a title
pl.xlabel('x axis')# make axis labels
pl.ylabel('y axis')
pl.xlim(0.0, 9.0)# set axis limits
pl.ylim(0.0, 30.)
pl.legend([plot1, plot2], ('red line', 'green circles'), 'best', numpoints=1)# make legend
pl.show()# show the plot on the screen
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(x1,y1,c='red')
ax.scatter(x2,y2,s=10,c='g')
#plt.xlim(220,450)
#plt.ylim(0,60000)
#plt.title("tianchi")
plt.grid(True)
#ax.plot(x,y)
plt.xlabel('X1')

plt.ylabel('Y1')
plt.show()



data = np.random.randint(1, 11, 5)
print data
x = np.arange(len(data))
print x
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(x, data, color = 'r')
ax.bar(x, data, alpha = .5, color = 'g')

plt.show()

f1 = pl.figure(1)
pl.subplot(221)
pl.subplot(222)
pl.subplot(212)
plt.show()

f1 = pl.figure(1)
pl.subplot(211)
pl.subplot(212)
plt.show()