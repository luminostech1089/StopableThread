import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)
from matplotlib import pyplot as plot


class TwoDPlot:
    def __init__(self, xlabel, ylable):
        self.xlabel = xlabel
        self.ylabel = ylable
        # Format string
        self.fmtStr = "ro"
        self._axis = None

    def axis(self, xmin, xmax, ymin, ymax):
        self._axis = [xmin, xmax, ymin, ymax]

    def plot(self, xlist, ylist):
        plot.plot(xlist, ylist)
        plot.ylabel(self.ylabel)
        plot.xlabel(self.xlabel)
        plot.axis(self._axis)
        plot.show()


if __name__ == "__main__":
    plot2d = TwoDPlot("threads", "time")
    print plot2d
    plot2d.axis(1,5,0,50)
    plot2d.plot(["", "Thread1", "Thread2"], [0, 20,30])
