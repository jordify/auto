#!/usr/bin/python2
import sched, time, os, sys, subprocess, pickle

class Experiment(object):
  """Run experiments in HW2"""
  def __init__(self, ex, cap=0, mins=5):
    self.ex = ex
    self.startTime = time.time()
    self.memFree = []
    self.cpuPercent = []
    self.times = []
    # HW3 experiment parameters
    self.cap = cap
    self.mins = mins
    # init the scheduler
    self.s = sched.scheduler(time.time, time.sleep)

  def get_metrics(self):
    """Get the CPU usage and free Mem of VM from xentop and vmstat"""
    ret = os.popen('/usr/bin/sudo /usr/sbin/xentop -b -i2 -d3')
    cpuPercent = ret.readlines()[-3].split()[3]
    ret = os.popen('/usr/bin/ssh acvm-04-1 vmstat -S M')
    memFree = ret.readlines()[-1].split()[3]
    print time.time() - self.startTime, "\tCPU%: ", cpuPercent, "\tFree Mem (MB): ", memFree
    self.memFree.append(memFree)
    self.cpuPercent.append(cpuPercent)

  def launchWork(self,N):
    """Launch the workload application with N as matrix size"""
    subprocess.Popen('/usr/bin/ssh acvm-04-1 "time ./workload %d"' % (N), shell=True)
    print time.time() - self.startTime, "\tN is %d" % (N)

  def loop(self):
    """Main program loop. Schedules the monitor and workloads."""
    self.startTime = time.time()
    if self.ex==1:
      self.runEx1()
    elif self.ex==2:
      self.runEx2()
    elif self.ex==3:
      self.runEx3()
    elif self.ex==4:
      self.runEx4()
    elif self.ex==5:
      self.runHW3()
    else:
      print "Not a valid experiment number!\nTry 1 or 2."

  def runHW3(self):
    """Gather data for N = 10, 20, ..., 50 for a given cap and monitor
    time"""
    os.popen('/usr/bin/sudo /usr/sbin/xm sched-credit -d acvm-04-1.acis.ufl.edu -c '+str(self.cap))
    for i in xrange(5):
      self.s.enter((i*self.mins*60)+15, 1, self.launchWork, ([(i+1)*10]))
      for j in xrange(self.mins*6):
        self.times.append(i*self.mins*60+j*10)
        self.s.enter(i*self.mins*60+j*10, 1, self.get_metrics, ())
    self.s.run()
    os.popen('/usr/bin/sudo /usr/sbin/xm sched-credit -d acvm-04-1.acis.ufl.edu -c 0')

  def runEx1(self):
    """Monitor for 5 min with no workload"""
    for i in xrange(5*6):
      self.s.enter(i*10, 1, self.get_metrics, ())
      self.times.append(i*10)
    self.s.run()

  def runEx2(self):
    """Monitor for 5 min with workload 40"""
    self.s.enter(15, 1, self.launchWork, ([40]))
    for i in xrange(5*6):
      self.times.append(i*10)
      self.s.enter(i*10, 1, self.get_metrics, ())
    self.s.run()

  def runEx3(self):
    """Monitor varying workload in increments of 10 from 10 to 50"""
    for i in xrange(5):
      self.s.enter((i*300)+15, 1, self.launchWork, ([(i+1)*10]))
      for j in xrange(i*30,(i+1)*30):
        self.times.append(i*300+j*10)
        self.s.enter(i*30+j*10, 1, self.get_metrics, ())
    self.s.run()

  def runEx4(self):
    """Varying cap and mem repeat ex3"""
    for cap in ['50','75','0']:
      os.popen('/usr/bin/sudo /usr/sbin/xm sched-credit -d acvm-04-1.acis.ufl.edu -c '+cap)
      self.runEx3()
      self.dump()
      os.popen('mv ex4ResDump.pickle ex4ResDump_Cap='+cap+'.pickle')
    # Reset Cap
    os.popen('/usr/bin/sudo /usr/sbin/xm sched-credit -d acvm-04-1.acis.ufl.edu -c 0')
    for mem in ['128','256','512']:
      os.popen('/usr/bin/sudo /usr/sbin/xm mem-set acvm-04-1.acis.ufl.edu '+mem)
      self.runEx3()
      self.dump()
      os.popen('mv ex4ResDump.pickle ex4ResDump_Mem='+mem+'.pickle')

  def dump(self):
    """No way to install numpy, matplotlib so this just pickles the
    arrays to be graphed on my home machine."""
    dumpFileName = "ex%dResDump.pickle" % (self.ex,)
    dumpFile = open(dumpFileName, 'w')
    pickle.dump({'ex': self.ex, 'times': self.times, 'memFree':
      self.memFree, 'cpuPercent': self.cpuPercent}, dumpFile)
    dumpFile.close()
    self.times = []
    self.memFree = []
    self.cpuPercent = []


if __name__=='__main__':
  if (len(sys.argv) < 2):
    print "Please specify experiment as: ", sys.argv[0], "<experment number>"
    sys.exit(1)
  # run the experiment specified on the command line
  if len(sys.argv) > 2:
    exp = Experiment(int(sys.argv[1]),cap=int(sys.argv[2]),mins=int(sys.argv[3]))
    exp.loop()
    exp.dump()
  else:
    exp = Experiment(int(sys.argv[1]))
    exp.loop()
    exp.dump()
