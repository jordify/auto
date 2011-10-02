#!/usr/bin/python2
import sched, time, os, sys, subprocess, pickle

class Experiment(object):
  """Run experiments in HW2"""
  def __init__(self, ex, graph=False):
    self.graph = graph
    self.ex = ex
    self.startTime = time.time()
    self.memFree = []
    self.cpuPercent = []
    self.times = []
    # init the scheduler
    self.s = sched.scheduler(time.time, time.sleep)

  def get_metrics(self):
    """Get the CPU usage and free Mem of VM from xentop and vmstat"""
    ret = os.popen('/usr/bin/sudo /usr/sbin/xentop -b -i2 -d3')
    cpuPercent = ret.readlines()[-3].split()[3]
    ret = os.popen('/usr/bin/ssh acvm-04-1 vmstat -S M')
    memFree = ret.readlines()[-1].split()[3]
    print time.time() - self.startTime, "\tCPU%: ", cpuPercent, "\tFree Mem (MB): ", memFree
    if self.graph:
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
    # Monitor for 5 min with no workload
      for i in xrange(5*6):
        self.s.enter(i*10, 1, self.get_metrics, ())
        self.times.append(i*10)
      self.s.run()
    elif self.ex==2:
    # Monitor for 5 min with workload 40
      self.s.enter(15, 1, self.launchWork, ([40]))
      for i in xrange(5*6):
        self.times.append(i*10)
        self.s.enter(i*10, 1, self.get_metrics, ())
      self.s.run()
    elif self.ex==3:
    # Monitor 5 times for five minutes each with workload {10,20,..,50}
      runEx3()
    elif self.ex==4:
    # Varying cap and mem repeat ex3
      for cap in ['50','75','0']:
        os.popen('/usr/bin/sudo /usr/sbin/xm sched-credit -d acvm-04-1.acis.ufl.edu -c '+cap)
        self.runEx3()
        self.dump()
        os.popen('mv ex4ResDump.pickle ex4ResDump_Cap='+cap+'.pickle')
      for mem in ['128','256','512']:
        os.popen('/usr/bin/sudo /usr/sbin/xm mem-set acvm-04-1.acis.ufl.edu '+mem)
        self.runEx3()
        self.dump()
        os.popen('mv ex4ResDump.pickle ex4ResDump_Mem='+mem+'.pickle')
    else:
      print "Not a valid experiment number!\nTry 1 or 2."

  def runEx3(self):
    for i in xrange(5):
      self.s.enter((i*300)+15, 1, self.launchWork, ([(i+1)*10]))
      for j in xrange(i*30,(i+1)*30):
        self.times.append(i*300+j*10)
        self.s.enter(i*30+j*10, 1, self.get_metrics, ())
    self.s.run()

  def dump(self):
    """No way to install numpy, matplotlib so this just pickles the
    arrays to be graphed on my home machine."""
    dumpFileName = "ex%dResDump.pickle" % (self.ex,)
    dumpFile = open(dumpFileName, 'w')
    pickle.dump({'ex': self.ex, 'times': self.times, 'memFree':
      self.memFree, 'cpuPercent': self.cpuPercent}, dumpFile)
    dumpFile.close()


if __name__=='__main__':
  if (len(sys.argv) < 2):
    print "Please specify experiment as: ", sys.argv[0], "<experment number>"
    sys.exit(1)
  # run the experiment specified on the command line
  if (len(sys.argv) > 2):
    exp = Experiment(int(sys.argv[1]), True)
    exp.loop()
    exp.dump()
  else:
    exp = Experiment(int(sys.argv[1]))
    exp.loop()
