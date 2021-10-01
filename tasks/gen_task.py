import random
import time
import os
import csv

def random_2d():
    n = random.randint(5, 100)
    arr = []
    for i in range (n):
        arr.append([])
        for j in range (n):
            arr[i].append(random.randint(1, 9))
    return arr


random.seed(time.time())
for i in range (5):
    os.mkdir("task" + str(i))
    stageNum = random.randint(5, 10)
    for j in range (stageNum):
        with open("task"+str(i) + "/stage" + str(j), "w+") as stage_csv:
            csv_write = csv.writer(stage_csv, delimiter=',')
            csv_write.writerows(random_2d())
