import numpy as np
import xyz_py
from vasp_suite.graphs import MolGraph, Node
from ase.data import covalent_radii, atomic_masses, atomic_numbers
import sys
import os
import datetime

from .symm_util import prepare_structure, pg_compare
from .symm import analyse
from .write_util import write_coordinates, write_xyz, write_bonding_environment, write_angles

import argparse

from time import perf_counter


def make_graph(symbols, coordinates):
    graph = MolGraph()
    for idx, (elem, coord) in enumerate(zip(symbols, coordinates)):
        atnum = atomic_numbers[elem]
        radius = covalent_radii[atnum]
        mass = atomic_masses[atnum]
        node = Node(coord, elem, radius, idx, mass)
        graph.add_node(node)

    graph.construct_graph
    return graph


def main():
    args = read_args()

    xyz_file = args.xyz_file
    tol = args.tol
    predict = args.predict
    refine = args.refine_distance
    if refine and not predict:
        raise IOError("--predict is required to use --refine_distance")
    symm_func(xyz_file, tol, predict, args.output, refine, args.refine_tolerance, args.max_iter)


def symm_func(xyz_file, tol, predict, output, refine, convergence_tol, max_iter):

    point_group = None

    full_path = os.path.join(os.getcwd(), xyz_file)
    if not os.path.exists(full_path):
        raise FileExistsError('File does not exist')
    
    output_xyz = ''.join(xyz_file.split(".")[:-1]) + '_symmrot.xyz'

    if output is not None:
        f = open(output, 'w')
    else:
        f = sys.stdout

    start = perf_counter()

    f.write("{:^80}\n".format('Symmetry Analysis'))
    f.write("{:^80}\n".format('-----------------'))
    f.write("{:^80}\n".format("Author: William T. Morrillo"))
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write("{:^80}\n\n".format("Date: {}".format(dt_string)))

    f.write("{:^80}\n".format("symmetry_analysis is a programme to compute the point group symmetry"))
    f.write("{:^80}\n\n".format("of a given molecular structure."))

    # Read the xyz file and prepare the structure for symmetry analysis
    f.write("Input file: {}\n".format(xyz_file))
    f.write("Tolerance : {:.3e} Å\n\n".format(tol))
    symbols, coordinates = xyz_py.load_xyz(xyz_file)
    id = xyz_file.split(".xyz")[0]
    f.write('\n')
    f.write('{:^80}\n'.format(id.upper()))
    f.write('{:^80}\n\n'.format("_"*len(id)))
    write_coordinates(symbols, coordinates, f)
    f.write("{:^80}\n".format("Molecular Parameterisation"))
    f.write("{:^80}\n\n".format("--------------------------"))
    coordinates = prepare_structure(symbols, coordinates, f)
    f.write("Prepared Structure\n")
    f.write("------------------\n")
    write_coordinates(symbols, coordinates, f)
    f.write("\n")
    f.write("{:^80}\n".format("Molecular Graph"))
    f.write("{:^80}\n".format("---------------"))
    graph = make_graph(symbols, coordinates)
    write_bonding_environment(graph.edges, f)
    write_angles(graph.edges, f)
    f.write("Writing prepared structure to {}\n".format(output_xyz))
    write_xyz(symbols, coordinates, output_xyz)
    end_prep = perf_counter()
    f.write("Molecule preparation took {:11.7f} s\n\n".format(end_prep-start))

    if predict is None:
        f.write("{:^80}\n".format("Finding Point Group"))
        f.write("{:^80}\n".format("-------------------"))
        point_group = analyse(symbols, coordinates, graph.edges, tol, f)
    else:
        # analyse the prediction
        # start lowering the tol based off of the analysis
        # write a function to compare the prediction to analysis
        f.write("{:^80}\n".format("Finding Predicted Point Group"))
        f.write("{:^80}\n".format("-----------------------------"))
        tol = 1e-4
        converged = False
        iter = 1
        while not converged:
            f.write('Iteration {} -> Tolerance = {:11.7f} Å\n'.format(iter, tol))
            point_group = analyse(symbols, coordinates, graph.edges, tol, f)
            converged, tol = pg_compare(predict, point_group, tol)

            if iter == 20:
                converged = True

            if converged:
                f.write("\n")
                f.write("{:^80}\n".format(" Point group {} found ".format(point_group)))
                f.write("{:^80}\n".format(" Distance from perfect point group: {} Å ".format(tol)))
            else:
                f.write("\nPredicted point group: {} \t Point group found: {}\n".format(predict, point_group))
                f.write("Adjusting Tolerance to {:11.7f} Å\n".format(tol))
            iter +=1
            f.write("--" + '\n\n')

    end_analysis = perf_counter()

    f.write("\n")
    f.write("{:-^80}\n".format(" Analysis Complete "))

    f.write("Symmetry analysis took {:11.7f} s\n\n".format(end_analysis-end_prep))

    if refine:
        refine_start = perf_counter()
        f.write("{:^80}\n".format("Refining Distance To Point Group {}".format(point_group)))
        f.write("{:^80}\n\n".format("-------------------------------------"))

        if point_group is None:
            f.write("Point group was not found. Unable to refine distance\n")
            f.write("Unexpected termination of symmetry_analysis\n")
            f.write("symmetry analysis took {:11.7f} s".format(perf_counter() - start))
            exit(1)

        dtol = min(1e-3, tol / 20)
        prev_tol = 0
        tol -= dtol

        # finds the base case
        refining=True
        iter = 1
        while refining:

            step_start = perf_counter()
            pg = analyse(symbols, coordinates, graph.edges, tol, f, quiet=True)
            step_end = perf_counter()
            t = step_end - step_start
            f.write("Step: {:<3} point group: {} \t tol = {:11.9f} Å \t dtol = {:11.9f} Å \t time: {:7.4e} s\n".format(iter, pg, tol, dtol, t))

            if point_group == pg and abs(tol - prev_tol) < convergence_tol:
                refining = False

            elif iter > max_iter:
                refining = False
                f.write("Maximum number of iterations reached. Could not converge\n")
                f.write("Unexpected termination of symmetry analysis\n")
                f.write("symmetry analysis took {:11.7f} s".format(perf_counter() - start))
                exit(1)

            elif point_group == pg:
                prev_tol = tol
                tol -= dtol
                assert tol > 0
                iter += 1
            else:
                tol += dtol
                prev_tol = tol
                dtol *= 0.7
                tol -= dtol
                assert tol > 0
                iter += 1

        refine_end = perf_counter()
        f.write("dtol has been converged to {:11.9f} Å\n\n".format(abs(tol - prev_tol)))
        f.write("{:^80}\n\n".format("Distance to {} = {:11.9f} Å".format(point_group, tol)))
        f.write("{:-^80}\n".format(" Refine Complete "))
        f.write("Refine took {:11.7f} s\n\n".format(refine_end - refine_start))

    f.write("{:^80}\n\n".format("Point group: {}".format(point_group)))
    end = perf_counter()
    f.write("Normal termination of symmetry_analysis - programme took {:11.7f} s to complete\n".format(end-start))


    if output is not None:
        f.close()

    return point_group


def read_args():

    parser = argparse.ArgumentParser(
            prog="main",
            description="A tool to compute the (pseudo)-point group of a molecule",
            formatter_class=argparse.RawDescriptionHelpFormatter
            )

    parser.add_argument(
            '--xyz_file',
            '-f',
            help='xyz file of the molecule you want to analyse',
            type=str,
            required=True
            )

    parser.add_argument(
            '--output',
            '-o',
            help='The name of the output file to write the results. (default=stdout)',
            default=None,
            type=str
            )

    method_group = parser.add_argument_group("Methods")

    method_group.add_argument(
            '--tol',
            help='Tolerance of the analysis in Å',
            type=float,
            default=1e-3,
            required=False
            )

    method_group.add_argument(
            '--predict',
            help='Provide a prediction of the point group and the tolerance will be adjusted to find it',
            default=None,
            type=str
            )

    extras = parser.add_argument_group('Extra Arguments')

    extras.add_argument(
            '--refine_distance',
            help='Calculates a more accurate distance from a predicted point group. (--predict) must be used',
            action='store_true',
            required=False
            )

    extras.add_argument(
            '--max_iter',
            help='Set the maximum number of iterations performed by the Refine programme (default: 200)',
            default=200,
            type=int
            )

    extras.add_argument(
            '--refine_tolerance',
            help='Set the convergence tolerance of the refine programme (default: 1e-8)',
            default=1e-8,
            type=float
            )

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    main()
