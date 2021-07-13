# imprecise
A look into scheduling for imprecise computation in machine learning...


## 'Scheduling Real-time Deep Learning Services as Imprecise Computations' by Yao et al.
This paper presents an algorithm which I have implemented in 'alg.py'. Here is the output of that script:

0: [None, None, None, None, None, None, None, None, None, None, None, None, 0, None, None, 1, 2, 3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]  
1: [None, None, 0, None, None, None, 1, None, None, None, None, None, None, None, 0, None, None, 0, 1, 0, None, 1, 1, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]  
2: [None, None, None, 0, 2, 0, 2, None, 3, 0, 2, None, 3, None, None, None, None, 0, 2, None, 0, 0, 0, 3, 0, 0, 0, 3, 3, 3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]  
0: ['INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 2, 'INF', 'INF', 3, 5, 7, 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF']  
1: ['INF', 'INF', 3, 'INF', 'INF', 'INF', 4, 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 5, 'INF', 'INF', 6, 6, 10, 'INF', 7, 9, 11, 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF']  
2: ['INF', 'INF', 'INF', 1, 9, 4, 12, 'INF', 15, 5, 13, 'INF', 16, 'INF', 'INF', 'INF', 'INF', 6, 14, 'INF', 7, 7, 11, 18, 8, 10, 12, 19, 21, 23, 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF', 'INF']  

Schedule that achieves reward 29   
[3, 1, 3]  
with corresponding rewards for each task:  
[17, 6, 6]  
