import numpy as np
from scipy.linalg import qr
from ase.data import atomic_numbers, atomic_masses

from .symm_util import construct_principal_axes, debug_plot
from .symm import analyse


def construct_basis(symbols, coordinates, f):
    atnums = list(map(atomic_numbers.__getitem__, symbols))
    masses = np.array(list(map(atomic_masses.__getitem__, atnums)))

    principal_axes, inertia_tensor = construct_principal_axes(coordinates, masses)

    # construct ridgid body translations
    ridgid_trans_x = np.zeros_like(coordinates)
    ridgid_trans_y = np.zeros_like(coordinates)
    ridgid_trans_z = np.zeros_like(coordinates)

    ridgid_trans_x[:, 0] = 1
    ridgid_trans_y[:, 1] = 1
    ridgid_trans_z[:, 2] = 1

    ridgid_trans_x = ridgid_trans_x.reshape(-1, 1, order='F')
    ridgid_trans_y = ridgid_trans_y.reshape(-1, 1, order='F')
    ridgid_trans_z = ridgid_trans_z.reshape(-1, 1, order='F')

    # construct ridgid body rotations

    ridgid_rot_x = np.array(list(map(lambda x: np.cross(principal_axes[0], x), coordinates))).reshape(-1, 1, order='F')
    ridgid_rot_y = np.array(list(map(lambda x: np.cross(principal_axes[1], x), coordinates))).reshape(-1, 1, order='F')
    ridgid_rot_z = np.array(list(map(lambda x: np.cross(principal_axes[2], x), coordinates))).reshape(-1, 1, order='F')


    ridgid_body = np.hstack((ridgid_trans_x,
                             ridgid_trans_y,
                             ridgid_trans_z,
                             ridgid_rot_x,
                             ridgid_rot_y,
                             ridgid_rot_z
                             ))

    basis, _, _ = qr(ridgid_body, mode='full', pivoting=True)
    basis = basis[6:]
    return basis


def get_distortions(basis, coordinates, symbols, f):

    n = coordinates.shape
    atnums = list(map(atomic_numbers.__getitem__, symbols))
    masses = np.array(list(map(atomic_masses.__getitem__, atnums)))

    coordinates = coordinates.reshape(-1, 1, order='F')


    def distort(coord, dist):
        dist = dist.reshape(-1, 1, order='F')
        assert coord.shape == dist.shape
        distortion = (coord + (dist * 0.1)).reshape(n, order='F')
        principal_axes, _ = construct_principal_axes(distortion, masses)
        return distortion @ principal_axes


    distortions = np.array(list(map(lambda dist: distort(coordinates, dist), basis)))

    return distortions


def assign_basis_irreps(symbols, distortions, bond_dict, basis, point_group, tol, f):
    p = []
    b = []

    for idx, (distortion, basis_vector) in enumerate(zip(distortions, basis)):

        distorted_point_group = analyse(symbols, distortion, bond_dict, tol, f)

        print("Basis vector: {}".format(idx+1))
        print("Equilibrium point group: {}".format(point_group))
        print("Distorted point group: {}".format(distorted_point_group))
        print("")
