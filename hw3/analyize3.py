#!/usr/bin/python2
import math
import matplotlib.pyplot as plt

data50 = [9.751, 10.018, 9.8446, 9.8354, 8.8594]
data75 = [6.396, 6.4205, 6.4104, 6.4135, 6.4116]
data100 = [4.7661, 4.8723, 4.7789, 4.7776, 4.7811]

operatingPoint = 6.4104

avg50 = sum(data50)/len(data50)
avg75 = sum(data75)/len(data75)
avg100 = sum(data100)/len(data100)

# Get data
us = [-25, 0, 25]
ys = [y-operatingPoint for y in [avg50, data75[4], avg100]]

# Make model
from scipy import stats
b,off, r,p,std_err = stats.linregress(us,ys)
modelYs = [b*u+off for u in us]
print "b=%g, off=%g" % (b,off)
print "Experimental Ys:", ys
print "Model Ys:", modelYs

# Get RMSE
RMSE = math.sqrt(sum([(modelYs[i]-ys[i])**2 for i in xrange(3)])/3.0)
print "RMSE = %g" % (RMSE,)

# Make plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('u[k]')
ax.plot(us, ys, 'r*', label="Observed Output")
ax.plot(us, modelYs, 'b*', label="Modeled Output")
h, l = ax.get_legend_handles_labels()
ax.legend(h,l)
plt.savefig("modelVsOutput.png")
