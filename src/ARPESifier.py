import numpy as np
from scipy.ndimage import zoom

a = np.random.rand(5, 5, 3)

a[:, :, 1] = a[:, :, 1]+3
a[:, :, 2] = a[:, :, 2]+5

b = zoom(a, (10, 10, 1))

e = np.linspace(0, 10, 200)

v = np.zeros((50, 50, 200))

from scipy.stats import norm

for i in range(b.shape[0]):
    print("i is %i" %(i))
    for j in range(b.shape[1]):
        for k in range(b.shape[2]):
            v[i,j,:] = v[i,j,:] + norm.pdf(e, loc=b[i,j,k], scale=0.1)

import h5py
f = h5py.File("test.h5", 'w')
f.create_dataset("data", data=v)
f.close()

