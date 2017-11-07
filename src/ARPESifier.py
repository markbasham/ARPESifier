import numpy as np
from scipy.ndimage import zoom
from scipy.stats import norm
from numba import jit
import time

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('function took %0.3f ms' % ((time2-time1)*1000.0))
        return ret
    return wrap

@timing
def arpesify(a,e, zoom_level=10, scale_level=0.01):
    b = zoom(a, (zoom_level, zoom_level, 1))
    v = np.zeros((b.shape[0], b.shape[1], e.shape[0]))
    for i in range(b.shape[0]):
        print("i is %i" %(i))
        for j in range(b.shape[1]):
            for k in range(b.shape[2]):
                v[i,j,:] = np.maximum(v[i,j,:], norm.pdf(e, loc=b[i,j,k], scale=scale_level))

    return v

if __name__ == "__main__":
    a = np.random.rand(25, 25, 3)*3.0
    
    a[:, :, 1] = a[:, :, 1]+3
    a[:, :, 2] = a[:, :, 2]+5
    
    e = np.linspace(0, 10, 200)
    
    v = arpesify(a, e)
    
    import h5py
    f = h5py.File("test.h5", 'w')
    f.create_dataset("data", data=v)
    f.close()

