import numpy as np
from sympy.physics.quantum.tests.test_sho1d import kz
from astropy.units import kyr

def load_castep(filename):
    f = open(filename, 'r')
    num_kpoints = int(f.readline().strip().split()[-1])
    num_spin_comps = int(f.readline().strip().split()[-1])
    num_electrons = float(f.readline().strip().split()[-1])
    num_eigenvalues = int(f.readline().strip().split()[-1])
    fermi_energy = float(f.readline().strip().split()[-1])

    f.readline().strip()  # Blank line
    f.readline().strip()  # Unit cell
    f.readline().strip()  # Unit cell
    f.readline().strip()  # Unit Cell

    kx = np.zeros(num_kpoints)
    ky = np.zeros(num_kpoints)
    kz = np.zeros(num_kpoints)
    e = np.zeros((num_kpoints, num_eigenvalues))

    for i in range(num_kpoints):
        kpoint = f.readline().strip().split()
        kx[i] = float(kpoint[2])
        ky[i] = float(kpoint[3])
        kz[i] = float(kpoint[4])
        f.readline().strip()  # for spin components ignored for now
        for j in range(num_eigenvalues):
            e[i,j] = float(f.readline().strip())

    # work out grid
    xx, xi = np.unique(kx, return_inverse=True)
    yy, yi = np.unique(ky, return_inverse=True)
    zz, zi = np.unique(kz, return_inverse=True)

    result = np.zeros((xx.shape[0], yy.shape[0], zz.shape[0], e.shape[1]))

    for i in range(e.shape[0]):
        result[xi[i], yi[i], zi[i], :] = e[i, :]

    return (xx, yy, zz, result)
