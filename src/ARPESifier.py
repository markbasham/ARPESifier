import math
import numpy as np
from scipy.ndimage import zoom
from scipy.stats import norm


def arpesify(a, e, zoom_level=2, scale_level=0.01):
    b = zoom(a, (zoom_level, zoom_level, 1))
    v = np.zeros((b.shape[0], b.shape[1], e.shape[0]))
    for i in range(b.shape[0]):
        print("i is %i" %(i))
        for j in range(b.shape[1]):
            for k in range(b.shape[2]):
                v[i, j, :] = np.maximum(v[i, j, :],
                                        norm.pdf(e, loc=b[i, j, k],
                                                 scale=scale_level))
    padval = int(v.shape[0]/2);
    padtup = (padval, padval)
    return np.pad(v, (padtup, padtup, (0, 0)), "symmetric")


def save(dataset, filename):
    import h5py
    handle = h5py.File(filename, 'w')
    handle.create_dataset("data", data=dataset)
    handle.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str,
                        help="Input filename")
    parser.add_argument("output", type=str,
                        help="Output filename")
    parser.add_argument("-c", "--castep", action="store_true",
                        help="load castep")
    parser.add_argument("-b", "--energy_begin", type=float,
                        help="Energy begin", default=-0.5)
    parser.add_argument("-e", "--energy_end", type=float,
                        help="Energy stop", default=0.5)
    parser.add_argument("-s", "--energy_steps", type=int,
                        help="Energy steps", default=500)
    parser.add_argument("-d", "--energy_spread", type=float,
                        help="Energy Gaussian Spread", default=0.001)
    parser.add_argument("-z", "--zoom", type=int,
                        help="K Zoom", default=1)
    args = parser.parse_args()

    if args.castep:
        import castep_loader as cl
        (kx, ky, kz, en) = cl.load_castep(args.input)
        en = en.reshape(int(math.sqrt(en.shape[0])),
                        int(math.sqrt(en.shape[0])),
                        en.shape[1])
        energies = np.linspace(args.energy_begin,
                               args.energy_end,
                               args.energy_steps)
        result = arpesify(en, energies,
                          zoom_level=args.zoom,
                          scale_level=args.energy_spread)
        save(result, args.output)
