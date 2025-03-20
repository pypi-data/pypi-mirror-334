import numpy as np

from .symm_util import bond_angle, is_bond_linear, rotation_matrix, axis_rotation_matrix, center_of_mass_shift, clean_cn_dict, debug_plot
from .write_util import write_symmetry_axes
from ase.data import atomic_numbers, atomic_masses


def is_linear(bond_dict):
    for atom1 in bond_dict:
        for atom2 in bond_dict[atom1]:
            for atom3 in bond_dict[atom2]:
                if not atom1 == atom3:
                    c1 = atom1.coordinate
                    c2 = atom2.coordinate
                    c3 = atom3.coordinate
                    v1 = c2 - c1
                    v2 = c2 - c3
                    theta = bond_angle(v1, v2)
                    if not is_bond_linear(theta):
                        return False
    return True


def inversion_center(symbols, coords, tol=1):
    inversion = False
    inverted_coords = np.array([[-x, -y, -z] for x, y, z in coords])
    for idx1, coord1 in enumerate(coords):
        found = False
        for idx2, coord2 in enumerate(inverted_coords):
            if np.allclose(coord1, coord2, atol=tol) and symbols[idx1] == symbols[idx2]:
                found = True
                break
        inversion = found
    return inversion


def cn_axis(symbols, coords, tol=1):

    atnums = list(map(atomic_numbers.__getitem__, symbols))
    masses = np.array(list(map(atomic_masses.__getitem__, atnums)))
    # check for Cn axis up to n=10
    check_n = np.arange(2, 10)

    Cn_dict = {}

    # Loop over all possible Cn axes
    for n in check_n:
        # compute the angles alpha beta and gamma
        theta = 2 * np.pi / n

        R_x = rotation_matrix(theta, 0, 0)
        R_y = rotation_matrix(0, theta, 0)
        R_z = rotation_matrix(0, 0, theta)

        # rotate the coordinates for each axis

        rot_x = coords @ R_x
        rot_y = coords @ R_y
        rot_z = coords @ R_z
        rot_x = center_of_mass_shift(rot_x, masses, None)
        rot_x = center_of_mass_shift(rot_y, masses, None)
        rot_x = center_of_mass_shift(rot_z, masses, None)

        # check if the rotated coordinates are the same as the original coordinates

        cn_found = True
        for idx1, coord in enumerate(coords):
            found = False
            for idx2, rot_coord in enumerate(rot_x):
                if np.allclose(coord, rot_coord, atol=tol) and symbols[idx1] == symbols[idx2]:
                    found = True
                    break
            cn_found = found
            if cn_found == False:
                break

        if cn_found:
            if n not in Cn_dict:
                Cn_dict[n] = ['z']
            else:
                Cn_dict[n].append('z')

        cn_found = True
        for idx1, coord in enumerate(coords):
            found = False
            for idx2, rot_coord in enumerate(rot_y):
                if np.allclose(coord, rot_coord, atol=tol) and symbols[idx1] == symbols[idx2]:
                    found = True
                    break
            cn_found = found
            if cn_found == False:
                break

        if cn_found:
            if n not in Cn_dict:
                Cn_dict[n] = ['y']
            else:
                Cn_dict[n].append('y')

        cn_found = True
        for idx1, coord in enumerate(coords):
            found = False
            for idx2, rot_coord in enumerate(rot_z):
                if np.allclose(coord, rot_coord, atol=tol) and symbols[idx1] == symbols[idx2]:
                    found = True
                    break
            cn_found = found
            if cn_found == False:
                break

        if cn_found:
            if n not in Cn_dict:
                Cn_dict[n] = ['x']
            else:
                Cn_dict[n].append('x')

    return Cn_dict



def sigma_h(symbols, coords, high_symmetry_axis, tol=1):
    atnums = list(map(atomic_numbers.__getitem__, symbols))
    masses = np.array(list(map(atomic_masses.__getitem__, atnums)))
    mirrored_coords = np.array(list(map(lambda x: x - 2 * (x @ high_symmetry_axis) * high_symmetry_axis, coords)))
    mirrored_coords = center_of_mass_shift(mirrored_coords, masses, None)

    # debug_plot(coords, mirrored_coords, high_symmetry_axis)

    sh_found = True
    for idx1, coord1 in enumerate(coords):
        found = False
        for idx2, coord2 in enumerate(mirrored_coords):
            if np.allclose(coord1, coord2, atol=tol) and symbols[idx1] == symbols[idx2]:
                found = True

        sh_found = found

    return sh_found


def sample_mirror_planes(axis, num_samples=10):
    axis = np.array(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)  # Normalize the axis vector
    
    # Choose two perpendicular vectors in the plane parallel to the axis
    if axis[0] != 0:
        ref_vec = np.array([0, 1, 0])
    else:
        ref_vec = np.array([1, 0, 0])
    
    second_vec = np.cross(axis, ref_vec)
    second_vec /= np.linalg.norm(second_vec)
    
    angles = np.linspace(0, 2 * np.pi, num_samples)

    def normal(angle):
        return np.cos(angle) * ref_vec + np.sin(angle) * second_vec

    normals = list(map(normal, angles))
    
    return normals

def sigma_v(symbols, coords, high_symmetry_axis, tol):
    atnums = list(map(atomic_numbers.__getitem__, symbols))
    masses = np.array(list(map(atomic_masses.__getitem__, atnums)))
    planes = sample_mirror_planes(np.array(high_symmetry_axis), num_samples=100)

    count = 0
    for plane in planes:
        plane /= np.linalg.norm(plane)
        mirrored_coords = np.array(list(map(lambda x: x - 2 * (x @ plane) * plane, coords)))
        mirrored_coords = center_of_mass_shift(coords, masses, None)

        sv_found = True
        for idx1, coord1 in enumerate(coords):
            found = False
            for idx2, coord2 in enumerate(mirrored_coords):
                if np.allclose(coord1, coord2, atol=tol) and symbols[idx1] == symbols[idx2]:
                    found = True
                    break

            sv_found = found
            if not sv_found:
                break

        if sv_found:
            count += 1

    return count > 0


def hemisphere_sample(num_points, hemisphere='upper'):
    theta = np.linspace(0, 2 * np.pi, num_points)
    # phi = np.random.uniform(0, np.pi / 2, num_points) if hemisphere == 'upper' else np.random.uniform(np.pi / 2, np.pi, num_points)
    phi = np.linspace(0, np.pi / 2, num_points) if hemisphere == 'upper' else np.linspace(np.pi / 2, np.pi, num_points)

    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)

    return np.column_stack((x, y, z))


def plane_sampling(normal, position, size=10, resolution=10):
    normal = np.array(normal, dtype=float)
    position = np.array(position, dtype=float)

    # Normalize the normal vector
    normal /= np.linalg.norm(normal)

    # Create two orthogonal vectors to form a basis for the plane
    if np.allclose(normal, [1, 0, 0]):  # Edge case: normal aligns with x-axis
        tangent1 = np.array([0, 1, 0])
    else:
        tangent1 = np.cross(normal, [1, 0, 0])
        tangent1 /= np.linalg.norm(tangent1)

    tangent2 = np.cross(normal, tangent1)

    # Generate a grid of points
    linspace = np.linspace(-size / 2, size / 2, resolution)
    xx, yy = np.meshgrid(linspace, linspace)

    # Compute 3D points on the plane
    points = position + xx[..., None] * tangent1 + yy[..., None] * tangent2
    return points.reshape(-1, 3)


def find_perp_rotation_axis(axis, Cn, symbols, coordinates, tol=1):
    axes = plane_sampling(axis, np.array([0.,0.,0.0]))

    atnums = list(map(atomic_numbers.__getitem__, symbols))
    masses = np.array(list(map(atomic_masses.__getitem__, atnums)))

    if tol < 0.5:
        tol = 0.5

    count = 0
    for ax in axes:
        theta = np.pi

        R = axis_rotation_matrix(ax, theta)

        rotated_coordinates = coordinates @ R
        rotated_coordinates = center_of_mass_shift(rotated_coordinates, masses, None)

        rot_found = True
        for idx1, coord1 in enumerate(coordinates):

            found = False
            for idx2, coord2 in enumerate(rotated_coordinates):

                if np.allclose(coord1, coord2, atol=tol) and symbols[idx1] == symbols[idx2]:
                    found = True
                    break

            rot_found = found
            if not rot_found:
                break
        if rot_found:
            count += 1

    return count >= Cn


def find_high_symmetry_axes(symbols, coordinates, tol):
    cns = np.arange(2, 10)
    axes = hemisphere_sample(361)

    Cn_dict = {}

    rotation_order = 1
    hsa = None

    for axis in axes:
        for n in cns:

            theta = 2 * np.pi / n
            R = axis_rotation_matrix(axis, theta)
            # rotate the coordinates for each axis
            rotated_coordinates = coordinates @ R

            rot_found = True

            for idx1, coord1 in enumerate(coordinates):

                found = False
                for idx2, coord2 in enumerate(rotated_coordinates):

                    if np.allclose(coord1, coord2, atol=tol) and symbols[idx1] == symbols[idx2]:
                        found = True
                        break

                rot_found = found
                if not rot_found:
                    break

            if rot_found:

                if n not in Cn_dict:
                    Cn_dict[n] = [axis]
                else:
                    Cn_dict[n].append(axis)

                if n > rotation_order:
                    rotation_order = n
                    hsa = axis

    return rotation_order, hsa, clean_cn_dict(Cn_dict)


def improper_rotations(Cn, hsa, symbols, coordinates, tol=1):
    # improper rotation i.e. C2 on the hsa and then c2 perpendicular
    # find sample the plane perpendicular and then perform two rotations by 2 * pi / 2 radians
    atnums = list(map(atomic_numbers.__getitem__, symbols))
    masses = np.array(list(map(atomic_masses.__getitem__, atnums)))

    perp_planes = plane_sampling(hsa, np.zeros(3))

    for plane in perp_planes:

        rot1 = axis_rotation_matrix(hsa, np.pi)
        rot2 = axis_rotation_matrix(plane, np.pi)

        rotated_coordinates = coordinates @ rot1 @ rot2
        rotated_coordinates = center_of_mass_shift(rotated_coordinates, masses, None)

        S2n_found = True
        for idx1, atom1 in enumerate(coordinates):
            found = False
            for idx2, atom2 in enumerate(rotated_coordinates):
                if np.allclose(atom1, atom2, atol=tol) and symbols[idx1] == symbols[idx2]:
                    found = True
                    break

            S2n_found = found

            if S2n_found:
                return True
            else:
                break

    return False


def analyse(symbols, coords, bond_dict, tol, f, quiet=False):
    if not quiet:
        f.write('{:-^80}\n\n'.format(' Computing (pseudo)-point group symmetry '))
    if is_linear(bond_dict):
        if not quiet:
            f.write('Linear molecule\n')
        if inversion_center(symbols, coords, tol=tol):
            if not quiet:
                f.write('Inversion center\n')
            return 'Dinfh'
        else:
            if not quiet:
                f.write('No Inversion center\n')
            return 'Cinfh'
    if not quiet:
        f.write("Non-linear molecule\n")

    Cn, hsa, Cn_dict = find_high_symmetry_axes(symbols, coords, tol=tol)
    if hsa is not None:
        if not quiet:
            f.write("High Symmetry Axis found:\n\tRotation order: C{}\n\tHigh symmetry axis: {:11.7f} {:11.7f} {:11.7f} Å\n".format(Cn, *hsa))

    count = 0
    for k, v in Cn_dict.items():
        if k == Cn:
            count += len(v)

    if not quiet:
        write_symmetry_axes(Cn_dict, f)

    if count >= 2:
        if not quiet:
            f.write("Two or more Cn where n > 2\n")
        if inversion_center(symbols, coords, tol=tol):
            if not quiet:
                f.write("Inversion center\n")
            if 5 in Cn_dict:
                if not quiet:
                    f.write("C5 axis found\n")
                return "Ih"
            else:
                return "Oh"
        else:
            return "Td"

    if not quiet:
        f.write("Less than 2 Cn where n > 2\n")

    if len(Cn_dict) == 0:
        if not quiet:
            f.write('No Cn axis found\n')
        if (sigma_h(symbols, coords, np.array([1, 0, 0]), tol=tol) or
                sigma_h(symbols, coords, np.array([0, 1, 0]), tol=tol) or
                sigma_h(symbols, coords, np.array([0, 0, 1]), tol=tol)
            ):
            if not quiet:
                f.write('sigma_h found\n')
            return 'Cs'

        if inversion_center(symbols, coords, tol=tol):
            if not quiet:
                f.write('Inversion center found\n')
            return 'Ci'
        if not quiet:
            f.write('No inversion center\n')
        return 'C1'
    
    # find the perpendicular C2s
    if hsa is not None:
        if find_perp_rotation_axis(hsa, Cn, symbols, coords, tol=tol):
                if not quiet:
                    f.write('More than {} C2 axis found perpendicular to C{}\n'.format(Cn, Cn))
                if sigma_h(symbols, coords, hsa, tol=tol):
                    if not quiet:
                        f.write('Sigma h found\n')
                    return "D{}h".format(Cn)
                if not quiet:
                    f.write('No sigma h\n')
                if sigma_v(symbols, coords, hsa, tol=tol):
                    if not quiet:
                        f.write('{} sigma v found\n'.format(Cn))
                    return 'D{}d'.format(Cn)
                if not quiet:
                    f.write('less than {} sigma v found\n'.format(Cn))
                return 'D{}'.format(Cn)

        if not quiet:
            f.write('Less than {} C2 axis found perpendicular to C{}\n'.format(Cn, Cn))

        if sigma_h(symbols, coords, hsa, tol=tol):
            if not quiet:
                f.write('Sigma h found\n')
            return 'C{}h'.format(Cn)
        if not quiet:
            f.write('No sigma h found\n')

        if sigma_v(symbols, coords, hsa, tol=tol):
            if not quiet:
                f.write('{} sigma v found\n'.format(Cn))
            return 'C{}v'.format(Cn)
        if not quiet:
            f.write('Less than {} sigma v found\n'.format(Cn))

        if improper_rotations(Cn, hsa, symbols, coords, tol=tol):
            if not quiet:
                f.write('S2{} found'.format(Cn))
            return 'S2{}'.format(Cn)

    return 'C{}'.format(Cn)
