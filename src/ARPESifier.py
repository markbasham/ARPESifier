import math
import numpy as np
from scipy.ndimage import zoom
from scipy.stats import norm


def arpesify4D(a, kx, ky, kz, e, zoom_level=2, scale_level=0.01):
    b = zoom(a, (zoom_level, zoom_level, zoom_level, 1))
    xx = zoom(kx, (zoom_level))
    yy = zoom(ky, (zoom_level))
    zz = zoom(kz, (zoom_level))
    v = np.zeros((b.shape[0], b.shape[1], b.shape[2], e.shape[0]))
    for i in range(b.shape[0]):
        print("i is %i" %(i))
        for j in range(b.shape[1]):
            for k in range(b.shape[2]):
                for l in range(b.shape[3]):
                    v[i, j, k, :] = np.maximum(v[i, j, k, :],
                                               norm.pdf(e, loc=b[i, j, k, l],
                                                        scale=scale_level))

    padx = int(v.shape[0] / 2);
    pady = int(v.shape[1] / 2);
    padz = int(v.shape[2] / 2);

    xx = np.pad(xx, ((padx, padx)), "wrap")
    xx[:padx] -= ((xx.max()-xx.min())*(float(xx.shape[0]+1) /float(xx.shape[0])))
    xx[-padx:] += ((xx.max()-xx.min())*(float(xx.shape[0]+1) /float(xx.shape[0])))

    yy = np.pad(yy, ((pady, pady)), "wrap")
    yy[:pady] -= ((yy.max()-yy.min())*(float(yy.shape[0]+1) /float(yy.shape[0])))
    yy[-pady:] += ((yy.max()-yy.min())*(float(yy.shape[0]+1) /float(yy.shape[0])))

    zz = np.pad(zz, ((padz, padz)), "wrap")
    zz[:padz] -= ((zz.max()-zz.min())*(float(zz.shape[0]+1) /float(zz.shape[0])))
    zz[-padz:] += ((zz.max()-zz.min())*(float(zz.shape[0]+1) /float(zz.shape[0])))

    result = np.pad(v, ((padx, padx), (pady, pady), (padz, padz), (0, 0)), "symmetric")
    return xx, yy, zz, result


def arpesify3D(a, kx, ky, e, zoom_level=2, scale_level=0.01):
    b = zoom(a, (zoom_level, zoom_level, 1))
    xx = zoom(kx, (zoom_level))
    yy = zoom(ky, (zoom_level))
    v = np.zeros((b.shape[0], b.shape[1], e.shape[0]))
    for i in range(b.shape[0]):
        print("i is %i" %(i))
        for j in range(b.shape[1]):
            for l in range(b.shape[2]):
                v[i, j, :] = np.maximum(v[i, j, :],
                                        norm.pdf(e, loc=b[i, j, l],
                                                 scale=scale_level))

    padx = int(v.shape[0] / 2);
    pady = int(v.shape[1] / 2);

    xx = np.pad(xx, ((padx, padx)), "wrap")
    xx[:padx] -= ((xx.max()-xx.min())*(float(xx.shape[0]+1) /float(xx.shape[0])))
    xx[-padx:] += ((xx.max()-xx.min())*(float(xx.shape[0]+1) /float(xx.shape[0])))

    yy = np.pad(yy, ((pady, pady)), "wrap")
    yy[:pady] -= ((yy.max()-yy.min())*(float(yy.shape[0]+1) /float(yy.shape[0])))
    yy[-pady:] += ((yy.max()-yy.min())*(float(yy.shape[0]+1) /float(yy.shape[0])))

    result = np.pad(v, ((padx, padx), (pady, pady), (0, 0)), "symmetric")
    return xx, yy, result


def save(dataset, kx, ky, kz, e, filename):
    import h5py
    handle = h5py.File(filename, 'w')
    entry = handle.create_group('entry')
    entry.attrs['NXclass'] = 'NXentry'
    group = handle.create_group('data')
    group.attrs['NXclass'] = 'NXdata'
    group.create_dataset("data", data=dataset)
    group.create_dataset("kx", data=kx)
    group.create_dataset("ky", data=ky)
    if kz:
        group.create_dataset("kz", data=kz)
    group.create_dataset("Energy", data=e)
    group.attrs['signal'] = 'data'
    if kz:
        group.attrs['axes'] = 'kx,ky,kz,Energy'
    else:
        group.attrs['axes'] = 'kx,ky,Energy'
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
    parser.add_argument("-t", "--threeD", action="store_true",
                        help="load castep")
    parser.add_argument("-b", "--energy_begin", type=float,
                        help="Energy begin", default=-0.25)
    parser.add_argument("-e", "--energy_end", type=float,
                        help="Energy stop", default=0.25)
    parser.add_argument("-s", "--energy_steps", type=int,
                        help="Energy steps", default=1000)
    parser.add_argument("-d", "--energy_spread", type=float,
                        help="Energy Gaussian Spread", default=0.001)
    parser.add_argument("-z", "--zoom", type=int,
                        help="K Zoom", default=1)
    args = parser.parse_args()

    if args.castep:
        import castep_loader as cl
        (kx, ky, kz, en) = cl.load_castep(args.input)
        energies = np.linspace(args.energy_end,
                               args.energy_begin,
                               args.energy_steps)

        if args.threeD:
            (kx, ky, result) = arpesify3D(en[:, :, 0, :], kx, ky, energies,
                                          zoom_level=args.zoom,
                                          scale_level=args.energy_spread)
            save(result, kx, ky, None, energies, args.output)
        else:
            (kx, ky, kz, result) = arpesify4D(en, kx, ky, kz, energies,
                                              zoom_level=args.zoom,
                                              scale_level=args.energy_spread)
            save(result, kx, ky, kz, energies, args.output)
