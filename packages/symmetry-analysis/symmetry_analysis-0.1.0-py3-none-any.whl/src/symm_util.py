import numpy as np
import re
from ase.data import covalent_radii, atomic_numbers, atomic_masses, chemical_symbols

import matplotlib.pyplot as plt


pred_pattern = re.compile(r'\s*[A-Z](?P<order>\d?)[A-Z]?[a-z]?')

def bond_angle(v1, v2):
    try:
        theta = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    except Exception as _:
        theta = 0
    return theta


def is_bond_linear(theta, atol=1e-5):
    return (np.isclose(theta, np.pi, atol=atol) or np.isclose(theta, 0.0, atol=1e-5))


def center_of_mass_shift(coordinates, masses, f):
    center_of_mass = np.sum(coordinates * masses[:, None], axis=0) / np.sum(masses)
    if f is not None:
        f.write('Center of mass: {:11.7f} {:11.7f} {:11.7f} Å\n\n'.format(*center_of_mass))
    coordinates -= center_of_mass
    return coordinates


def construct_principal_axes(coordinates, masses):
    inertia_tensor = coordinates.T @ np.diag(masses) @ coordinates
    eval, principal_axes = np.linalg.eigh(inertia_tensor)
    idx = eval.argsort()[::-1]
    # idx = idx[::-1]
    principal_axes = principal_axes[:, idx]
    return principal_axes, inertia_tensor
    


def prepare_structure(symbols, coordinates, f):
    atnums = list(map(atomic_numbers.__getitem__, symbols))
    masses = np.array(list(map(atomic_masses.__getitem__, atnums)))
    u_atnums = np.unique(atnums)
    u_masses = list(map(atomic_masses.__getitem__, u_atnums))
    u_symbols = list(map(chemical_symbols.__getitem__, u_atnums))

    f.write('Atomic Masses\n')
    f.write('-------------\n')
    for s, m in zip(u_symbols, u_masses):
        f.write('{:4} {:7.4f} amu\n'.format(s,m))
    f.write("\n")

    coordinates = center_of_mass_shift(coordinates, masses, f)

    principal_axes, inertia_tensor = construct_principal_axes(coordinates, masses) 

    f.write('Inertia tensor\n')
    f.write('--------------\n')
    for row in inertia_tensor:
        f.write('{:13.7f} {:13.7f} {:13.7f}\n'.format(*row))
    f.write("\n")

    f.write('Principal Axes\n')
    f.write('--------------\n')
    for row in principal_axes:
        f.write('{:11.7f} {:11.7f} {:11.7f}\n'.format(*row))
    f.write("\n")

    rotated_coords = coordinates @ principal_axes

    return rotated_coords


def rotation_matrix(alpha, beta, gamma):

    Rz = np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
        ])

    Ry = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
        ])

    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha), np.cos(alpha)]
        ])

    return Rz @ Ry @ Rx

def axis_rotation_matrix(axis, theta):
    axis = axis / np.linalg.norm(axis)  # Normalize axis
    v_x, v_y, v_z = axis
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    K = np.array([[0, -v_z, v_y], [v_z, 0, -v_x], [-v_y, v_x, 0]])
    R = np.eye(3) + sin_theta * K + (1 - cos_theta) * np.dot(K, K)
    return R


def clean_cn_dict(Cn_dict):

    for rotation_order, axes in Cn_dict.items():

        v = []
        for axis in axes:
            include = True
            for u in v:
                angle = bond_angle(axis, u)
                if np.allclose(axis, u, atol=1) or np.allclose(angle, 0, atol=3) or np.allclose(angle, 180, atol=3):
                    include = False
                
            if include:
                v.append(axis)

        Cn_dict[rotation_order] = np.array(v)

    return Cn_dict


def analyse_pg(prediction):
    match = pred_pattern.match(prediction)
    if match:
        rotation_order = match.group('order')
        return rotation_order
    return None


def resolve_order(point_group):
    order_dict = {'Td': 2,
                  'Oh': 2,
                  'Ih': 5,
                  'Cs': 1,
                  'Ci': 1,
                  'Cinfv': np.inf,
                  'Dinfv': np.inf}
    if point_group not in order_dict:
        return 1
    
    return order_dict[point_group]


def pg_compare(prediction, point_group, tol):
    pred_order = analyse_pg(prediction)
    order = analyse_pg(point_group)

    if order == '':
        order = resolve_order(point_group)

    if pred_order is None or order is None:
        return True, tol

    if int(pred_order) == int(order):
        return True, tol
    elif int(pred_order) > int(order):
        if tol <= 0.1:
            tol *= 5
        else:
            tol *= 1.2
        return False, tol
    elif int(pred_order) < int(order):
        return False, tol / 5


def debug_plot(c1, c2, hsa, axis=None):

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    ax.scatter(c1[:, 0], c1[:, 1], c1[:, 2],  color='r', label="coordinates")
    ax.scatter(c2[:, 0], c2[:, 1], c2[:, 2], color='b', label="trans/rot/mirr coorinates")
    if hsa is not None:
        x = [-hsa[0], 0, hsa[0]]
        y = [-hsa[1], 0, hsa[1]]
        z = [-hsa[2], 0, hsa[2]]
        ax.plot(x, y, z, color='k')
    if axis is not None:
        x = [-axis[0], 0, axis[0]]
        y = [-axis[1], 0, axis[1]]
        z = [-axis[2], 0, axis[2]]
        ax.plot(x, y, z, color='k')
    ax.legend()
    plt.show()
