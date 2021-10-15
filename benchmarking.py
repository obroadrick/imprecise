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
    def startClock(self):
        self.startTime = timeit.timeit()

    #stop timer and add data to csv
    def endClock(self):
        self.endTime = timeit.timeit()
        timeElapsed = self.endTime - self.startTime
        runData = [self.label, self.startTime, self.endTime, timeElapsed]
        with open('benchData/time.csv', 'a') as f:
            writer = csv.writer(f)
            
            writer.writerow(runData)

    def resetCSV(self):
        header = ['Section','Start Time','End Time','Time Elapsed']
        with open('benchData/time.csv' , 'w') as f:
            writer = csv.writer(f)
            
            writer.writerow(header)

        
    