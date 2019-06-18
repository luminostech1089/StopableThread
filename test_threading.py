import logging
from pythread import PyThread
from qvsplot import TwoDPlot
from time import sleep
import os
import subprocess

def foo1(num):
    alist = []
    logging.info("ping start")
    op = subprocess.check_output('ping 10.24.143.91 -n {}'.format(num), shell=True)
    logging.info(op)

def foo(num):
    logging.info("ping start sequence")
    op = subprocess.check_output('ping 10.24.143.91 -n {}'.format(num), shell=True)
    op = subprocess.check_output('ping 10.24.143.91 -n {}'.format(num), shell=True)
    logging.info("ping end start sequence")
    logging.info(op)


if __name__ == "__main__":
    # foo1(10)
    # import sys
    # sys.exit(1)
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Logging started")
    t1 = PyThread(target=foo1, args=(10,))
    t2 = PyThread(target=foo1, args=(10,))
    t1.start()
    t2.start()
    sleep(1)
    # t1.stop()
    # t2.stop()
    t1.join()
    t2.join()
    print "Thread1 Is Alive-{}".format(t1.is_alive())
    print "Thread2 Is Alive-{}".format(t2.is_alive())
    plot_2d = TwoDPlot(xlabel="Thread Names", ylable="Time(s)")
    plot_2d.axis(0,5,0,50)
    print t2.executionTime
    import time
    start = time.time()
    foo(10)
    elapsed = time.time() - start
    plot_2d.plot(["Thread1", "Thread2", "Sequential"], [t1.executionTime, t2.executionTime, elapsed])
