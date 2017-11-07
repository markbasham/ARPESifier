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

    return (kx, ky, kz, e)

if __name__ == "__main__":
    (kx, ky, kz, e) = load_castep("FeSe_64x64x1.bands")

    # hack to pull out a small region for the moment.
    ky = ky[kx > 0]
    e = e[kx > 0]
    kx = kx[kx > 0]

    ky = ky[kx < 0.1]
    e = e[kx < 0.1]
    kx = kx[kx < 0.1]

    kx = kx[ky > -0.2]
    e = e[ky > -0.2]
    ky = ky[ky > -0.2]

    kx = kx[ky < -0.1]
    e = e[ky < -0.1]
    ky = ky[ky < -0.1]

    e = e.reshape(6,7,53)

    import ARPESifier
    result = ARPESifier.arpesify(e, np.linspace(-2.0, 1.0, 400))

    import h5py
    f = h5py.File("test2.h5", 'w')
    f.create_dataset('kx', data=kx)
    f.create_dataset('ky', data=ky)
    f.create_dataset('ARPES', data=result)
    f.create_dataset('e', data=e)
    f.close()