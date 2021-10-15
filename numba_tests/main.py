import math
from numba import vectorize
import numpy as np

a = np.arange(4096,dtype=np.float32)
print(a)

@vectorize(['float32(float32)'], target='cuda')
def gpu_sqrt(x):
    return math.sqrt(x)


gpu_sqrt(a)
print(a)
