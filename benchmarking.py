import matplotlib.pyplot as plt
import timeit
import csv

class Graph:
    #static 2d array to store data
    taskData = [[],[],[],[],[]]

    #initialize function to start our graph
    def __init__(self):
        self.title = 'Tasks per Request vs Average Reward'

    #add data point for the graph. Use x to specify the tasks per request
    def addPoint(self, x, y):
        taskData[x].append(y)

    #plot graph when finished, export to benchData
    def plot(self, numTasks):
        xvals = []
        yvals = []
        for x in range(0, numTasks):
            xvals.append(x)
            yvals.append(sum(taskData(x))/len(taskData(x)))
        plt.plot(xvals,yvals)
        plt.xlabel('Tasks per Request')
        plt.ylabel('Average Reward')
        plt.title(self.title)
        plt.savefig('benchData/taskVreward.png')

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

    #reset CSV file
    def resetCSV(self):
        header = ['Section','Start Time','End Time','Time Elapsed']
        with open('benchData/time.csv' , 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)

        
    