import matplotlib.pyplot as plt
import timeit
import csv

class Graph:
    xvals = []
    yvals = []

    #initialize function to start our graph
    def __init__(self, xlabel, ylabel):
        self.xlabel = xlabel
        self.ylabel = ylabel

    #add data point for the graph
    def addPoint(self, x, y):
        xvals.append(x)
        yvals.append(y)

    #plot graph when finished
    def plot(self):
        plt.plot(xvals,yvals)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.show()

class Time:
    #initialize function to give label
    def __init__(self, label):
        self.label = label
    
    #start timer
    def startTime(self):
        self.startTime = timeit.timeit()

    #stop timer and add data to csv
    def endTime(self):
        self.endTime = timeit.timeit()
        runData = [self.label, self.startTime, self.endTime, self.endTime - self.startTime]
        with open('benchData/time.csv', 'a') as f:
            writer = csv.writer(f)
            
            writer.writerow(runData)

        
    