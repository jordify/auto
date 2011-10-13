#!/usr/bin/python2
import sys
import pickle

import numpy as np
import matplotlib.pyplot as plt

def getDict(dumpFileName):
  try:
    dumpFile = open(dumpFileName, 'r')
  except:
    print "Couldn't open "+dumpFileName+" file! Check experiment number."
    sys.exit(1)
  dumpDict =  pickle.load(dumpFile)
  dumpFile.close()
  return dumpDict

def plot(ex):
  if ex>0 and ex<6 and ex!=4:
    # Get data
    dataDict = getDict("ex%dResDump.pickle" % (ex,))
    # Set up figure
    fig = plt.figure()
    # Axis one shows mem
    ax1 = fig.add_subplot(111)
    ax1.plot(dataDict['times'], dataDict['memFree'], 'b-')
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('Free Memory (MB)', color='b')
    for tl in ax1.get_yticklabels():
      tl.set_color('b')
    # Axis two shows cpu
    ax2 = ax1.twinx()
    ax2.plot(dataDict['times'], dataDict['cpuPercent'], 'r-')
    ax2.set_ylabel('CPU Utilization (%)', color='r')
    for tl in ax2.get_yticklabels():
      tl.set_color('r')
    # Plot and save the figure
    plt.savefig('ex%d.png' % (ex,))
    plt.show()
  else:
    print "Not a valid experiment number"

if __name__=='__main__':
  if(len(sys.argv) < 2):
    print "Please specify experiment as: ", sys.argv[0], "<experment number>"
    sys.exit(1)
  else:
    plot(int(sys.argv[1]))
