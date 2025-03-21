# Copyright (c) [2024-2025] [Laszlo Oroszlany, Daniel Pozsar]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os

import grogupy
import numpy as np
import pytest

"""
        (
            [1,1,1],
            10,
            100,
            1000,
            0,
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            [dict(atom=3, l=2), dict(atom=4, l=2), dict(atom=5, l=2)],
            [
                dict(ai=0, aj=1, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=1, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([2, 0, 0])),
            ],
        ),
        (
            [10,10,10],
            -10,
            1000,
            1000,
            1,
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            [dict(atom=3, l=2), dict(atom=4, l=2), dict(atom=5, l=2)],
            [
                dict(ai=0, aj=1, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=1, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([2, 0, 0])),
            ],
        ),
        (
            [10,10,1],
            None,
            100,
            1000,
            -1,
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            [dict(atom=3, l=2), dict(atom=4, l=2), dict(atom=5, l=2)],
            [
                dict(ai=0, aj=1, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=1, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([2, 0, 0])),
            ],
        ),
"""


@pytest.mark.parametrize(
    "kset, emin, eset, esetp, emax, xyz, magnetic_entities, pairs",
    [
        (
            [1, 1, 1],
            1,
            100,
            1000,
            0,
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            [dict(atom=3, l=2), dict(atom=4, l=2), dict(atom=5, l=2)],
            [
                dict(ai=0, aj=1, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=1, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([2, 0, 0])),
            ],
        ),
        (
            [1, 1, 1],
            2,
            100,
            1000,
            0,
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            [dict(atom=3, l=2), dict(atom=4, l=2), dict(atom=5, l=2)],
            [
                dict(ai=0, aj=1, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=1, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([2, 0, 0])),
            ],
        ),
        (
            [2, 2, 2],
            -10,
            300,
            1000,
            1,
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            [dict(atom=3, l=2), dict(atom=4, l=2), dict(atom=5, l=2)],
            [
                dict(ai=0, aj=1, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=1, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([2, 0, 0])),
            ],
        ),
        (
            [2, 2, 1],
            None,
            100,
            1000,
            -1,
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            [dict(atom=3, l=2), dict(atom=4, l=2), dict(atom=5, l=2)],
            [
                dict(ai=0, aj=1, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([0, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=1, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=2, Ruc=np.array([1, 0, 0])),
                dict(ai=0, aj=0, Ruc=np.array([2, 0, 0])),
            ],
        ),
    ],
)
def test_equality_between_solutions(
    kset, emin, eset, esetp, emax, xyz, magnetic_entities, pairs
):
    # matlabmode on
    ################################################################################
    Fe3GeTe2_kspace = grogupy.Kspace(kset)
    print(Fe3GeTe2_kspace)
    Fe3GeTe2_contour = grogupy.Contour(
        eset,
        esetp,
        emin,
        eigfile="/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        emax=emax,
    )
    print(Fe3GeTe2_contour)
    Fe3GeTe2_hamiltonian = grogupy.Hamiltonian(
        "/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        [0, 0, 1],
    )
    print(Fe3GeTe2_hamiltonian)
    Fe3GeTe2 = grogupy.Builder(xyz, matlabmode=False)
    Fe3GeTe2.greens_function_solver = "Sequential"
    Fe3GeTe2.parallel_mode = "K"
    Fe3GeTe2.add_kspace(Fe3GeTe2_kspace)
    Fe3GeTe2.add_contour(Fe3GeTe2_contour)
    Fe3GeTe2.add_hamiltonian(Fe3GeTe2_hamiltonian)
    Fe3GeTe2.add_magnetic_entities(magnetic_entities)
    print(Fe3GeTe2.magnetic_entities)
    Fe3GeTe2.add_pairs(pairs)
    print(Fe3GeTe2.pairs)
    print(Fe3GeTe2.__repr__)
    Fe3GeTe2.solve()
    print(Fe3GeTe2.to_magnopy())
    grogupy.save_magnopy(Fe3GeTe2, "./tests/test_matlab_3_sequential_k")
    grogupy.save(Fe3GeTe2, "./tests/test_matlab_3_sequential_k")
    ################################################################################
    Fe3GeTe2_kspace = grogupy.Kspace(kset)
    print(Fe3GeTe2_kspace)
    Fe3GeTe2_contour = grogupy.Contour(
        eset,
        esetp,
        emin,
        eigfile="/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        emax=emax,
    )
    print(Fe3GeTe2_contour)
    Fe3GeTe2_hamiltonian = grogupy.Hamiltonian(
        "/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        [0, 0, 1],
    )
    print(Fe3GeTe2_hamiltonian)
    Fe3GeTe2 = grogupy.Builder(xyz, matlabmode=False)
    Fe3GeTe2.greens_function_solver = "Parallel"
    Fe3GeTe2.parallel_mode = "K"
    Fe3GeTe2.add_kspace(Fe3GeTe2_kspace)
    Fe3GeTe2.add_contour(Fe3GeTe2_contour)
    Fe3GeTe2.add_hamiltonian(Fe3GeTe2_hamiltonian)
    Fe3GeTe2.add_magnetic_entities(magnetic_entities)
    print(Fe3GeTe2.magnetic_entities)
    Fe3GeTe2.add_pairs(pairs)
    print(Fe3GeTe2.pairs)
    print(Fe3GeTe2.__repr__)
    Fe3GeTe2.solve()
    print(Fe3GeTe2.to_magnopy())
    grogupy.save_magnopy(Fe3GeTe2, "./tests/test_matlab_3_parallel_k")
    grogupy.save(Fe3GeTe2, "./tests/test_matlab_3_parallel_k")
    ################################################################################
    Fe3GeTe2_kspace = grogupy.Kspace(kset)
    print(Fe3GeTe2_kspace)
    Fe3GeTe2_contour = grogupy.Contour(
        eset,
        esetp,
        emin,
        eigfile="/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        emax=emax,
    )
    print(Fe3GeTe2_contour)
    Fe3GeTe2_hamiltonian = grogupy.Hamiltonian(
        "/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        [0, 0, 1],
    )
    print(Fe3GeTe2_hamiltonian)
    Fe3GeTe2 = grogupy.Builder(xyz, matlabmode=False)
    Fe3GeTe2.greens_function_solver = "Sequential"
    Fe3GeTe2.parallel_mode = "All"
    Fe3GeTe2.add_kspace(Fe3GeTe2_kspace)
    Fe3GeTe2.add_contour(Fe3GeTe2_contour)
    Fe3GeTe2.add_hamiltonian(Fe3GeTe2_hamiltonian)
    Fe3GeTe2.add_magnetic_entities(magnetic_entities)
    print(Fe3GeTe2.magnetic_entities)
    Fe3GeTe2.add_pairs(pairs)
    print(Fe3GeTe2.pairs)
    print(Fe3GeTe2.__repr__)
    Fe3GeTe2.solve()
    print(Fe3GeTe2.to_magnopy())
    grogupy.save_magnopy(Fe3GeTe2, "./tests/test_matlab_3_sequential_all")
    grogupy.save(Fe3GeTe2, "./tests/test_matlab_3_sequential_all")
    ################################################################################
    Fe3GeTe2_kspace = grogupy.Kspace(kset)
    print(Fe3GeTe2_kspace)
    Fe3GeTe2_contour = grogupy.Contour(
        eset,
        esetp,
        emin,
        eigfile="/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        emax=emax,
    )
    print(Fe3GeTe2_contour)
    Fe3GeTe2_hamiltonian = grogupy.Hamiltonian(
        "/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        [0, 0, 1],
    )
    print(Fe3GeTe2_hamiltonian)
    Fe3GeTe2 = grogupy.Builder(xyz, matlabmode=False)
    Fe3GeTe2.greens_function_solver = "Parallel"
    Fe3GeTe2.parallel_mode = "All"
    Fe3GeTe2.add_kspace(Fe3GeTe2_kspace)
    Fe3GeTe2.add_contour(Fe3GeTe2_contour)
    Fe3GeTe2.add_hamiltonian(Fe3GeTe2_hamiltonian)
    Fe3GeTe2.add_magnetic_entities(magnetic_entities)
    print(Fe3GeTe2.magnetic_entities)
    Fe3GeTe2.add_pairs(pairs)
    print(Fe3GeTe2.pairs)
    print(Fe3GeTe2.__repr__)
    Fe3GeTe2.solve()
    print(Fe3GeTe2.to_magnopy())
    grogupy.save_magnopy(Fe3GeTe2, "./tests/test_matlab_3_parallel_all")
    grogupy.save(Fe3GeTe2, "./tests/test_matlab_3_parallel_all")
    ################################################################################

    # matlabmode off
    ################################################################################
    Fe3GeTe2_kspace = grogupy.Kspace(kset)
    print(Fe3GeTe2_kspace)
    Fe3GeTe2_contour = grogupy.Contour(
        eset,
        esetp,
        emin,
        eigfile="/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        emax=emax,
    )
    print(Fe3GeTe2_contour)
    Fe3GeTe2_hamiltonian = grogupy.Hamiltonian(
        "/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        [0, 0, 1],
    )
    print(Fe3GeTe2_hamiltonian)
    Fe3GeTe2 = grogupy.Builder(xyz, matlabmode=False)
    Fe3GeTe2.greens_function_solver = "Sequential"
    Fe3GeTe2.parallel_mode = "K"
    Fe3GeTe2.add_kspace(Fe3GeTe2_kspace)
    Fe3GeTe2.add_contour(Fe3GeTe2_contour)
    Fe3GeTe2.add_hamiltonian(Fe3GeTe2_hamiltonian)
    Fe3GeTe2.add_magnetic_entities(magnetic_entities)
    print(Fe3GeTe2.magnetic_entities)
    Fe3GeTe2.add_pairs(pairs)
    print(Fe3GeTe2.pairs)
    print(Fe3GeTe2.__repr__)
    Fe3GeTe2.solve()
    print(Fe3GeTe2.to_magnopy())
    grogupy.save_magnopy(Fe3GeTe2, "./tests/test_3_sequential_k")
    grogupy.save(Fe3GeTe2, "./tests/test_3_sequential_k")
    ################################################################################
    Fe3GeTe2_kspace = grogupy.Kspace(kset)
    print(Fe3GeTe2_kspace)
    Fe3GeTe2_contour = grogupy.Contour(
        eset,
        esetp,
        emin,
        eigfile="/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        emax=emax,
    )
    print(Fe3GeTe2_contour)
    Fe3GeTe2_hamiltonian = grogupy.Hamiltonian(
        "/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        [0, 0, 1],
    )
    print(Fe3GeTe2_hamiltonian)
    Fe3GeTe2 = grogupy.Builder(xyz, matlabmode=False)
    Fe3GeTe2.greens_function_solver = "Parallel"
    Fe3GeTe2.parallel_mode = "K"
    Fe3GeTe2.add_kspace(Fe3GeTe2_kspace)
    Fe3GeTe2.add_contour(Fe3GeTe2_contour)
    Fe3GeTe2.add_hamiltonian(Fe3GeTe2_hamiltonian)
    Fe3GeTe2.add_magnetic_entities(magnetic_entities)
    print(Fe3GeTe2.magnetic_entities)
    Fe3GeTe2.add_pairs(pairs)
    print(Fe3GeTe2.pairs)
    print(Fe3GeTe2.__repr__)
    Fe3GeTe2.solve()
    print(Fe3GeTe2.to_magnopy())
    grogupy.save_magnopy(Fe3GeTe2, "./tests/test_3_parallel_k")
    grogupy.save(Fe3GeTe2, "./tests/test_3_parallel_k")
    ################################################################################
    Fe3GeTe2_kspace = grogupy.Kspace(kset)
    print(Fe3GeTe2_kspace)
    Fe3GeTe2_contour = grogupy.Contour(
        eset,
        esetp,
        emin,
        eigfile="/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        emax=emax,
    )
    print(Fe3GeTe2_contour)
    Fe3GeTe2_hamiltonian = grogupy.Hamiltonian(
        "/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        [0, 0, 1],
    )
    print(Fe3GeTe2_hamiltonian)
    Fe3GeTe2 = grogupy.Builder(xyz, matlabmode=False)
    Fe3GeTe2.greens_function_solver = "Sequential"
    Fe3GeTe2.parallel_mode = "All"
    Fe3GeTe2.add_kspace(Fe3GeTe2_kspace)
    Fe3GeTe2.add_contour(Fe3GeTe2_contour)
    Fe3GeTe2.add_hamiltonian(Fe3GeTe2_hamiltonian)
    Fe3GeTe2.add_magnetic_entities(magnetic_entities)
    print(Fe3GeTe2.magnetic_entities)
    Fe3GeTe2.add_pairs(pairs)
    print(Fe3GeTe2.pairs)
    print(Fe3GeTe2.__repr__)
    Fe3GeTe2.solve()
    print(Fe3GeTe2.to_magnopy())
    grogupy.save_magnopy(Fe3GeTe2, "./tests/test_3_sequential_all")
    grogupy.save(Fe3GeTe2, "./tests/test_3_sequential_all")
    ################################################################################
    Fe3GeTe2_kspace = grogupy.Kspace(kset)
    print(Fe3GeTe2_kspace)
    Fe3GeTe2_contour = grogupy.Contour(
        eset,
        esetp,
        emin,
        eigfile="/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        emax=emax,
    )
    print(Fe3GeTe2_contour)
    Fe3GeTe2_hamiltonian = grogupy.Hamiltonian(
        "/Users/danielpozsar/Downloads/nojij/Fe3GeTe2/monolayer/soc/lat3_791/Fe3GeTe2.fdf",
        [0, 0, 1],
    )
    print(Fe3GeTe2_hamiltonian)
    Fe3GeTe2 = grogupy.Builder(xyz, matlabmode=False)
    Fe3GeTe2.greens_function_solver = "Parallel"
    Fe3GeTe2.parallel_mode = "All"
    Fe3GeTe2.add_kspace(Fe3GeTe2_kspace)
    Fe3GeTe2.add_contour(Fe3GeTe2_contour)
    Fe3GeTe2.add_hamiltonian(Fe3GeTe2_hamiltonian)
    Fe3GeTe2.add_magnetic_entities(magnetic_entities)
    print(Fe3GeTe2.magnetic_entities)
    Fe3GeTe2.add_pairs(pairs)
    print(Fe3GeTe2.pairs)
    print(Fe3GeTe2.__repr__)
    Fe3GeTe2.solve()
    print(Fe3GeTe2.to_magnopy())
    grogupy.save_magnopy(Fe3GeTe2, "./tests/test_3_parallel_all")
    grogupy.save(Fe3GeTe2, "./tests/test_3_parallel_all")
    ################################################################################
    fit1 = grogupy.io.read_magnopy("./tests/test_3_sequential_k.magnopy.txt")
    fit2 = grogupy.io.read_magnopy("./tests/test_3_parallel_k.magnopy.txt")
    fit3 = grogupy.io.read_magnopy("./tests/test_3_sequential_all.magnopy.txt")
    fit4 = grogupy.io.read_magnopy("./tests/test_3_parallel_all.magnopy.txt")
    grogupy1 = grogupy.io.read_magnopy("./tests/test_matlab_3_sequential_k.magnopy.txt")
    grogupy2 = grogupy.io.read_magnopy("./tests/test_matlab_3_parallel_k.magnopy.txt")
    grogupy3 = grogupy.io.read_magnopy(
        "./tests/test_matlab_3_sequential_all.magnopy.txt"
    )
    grogupy4 = grogupy.io.read_magnopy("./tests/test_matlab_3_parallel_all.magnopy.txt")

    simulation_pairs = [
        (fit1, fit2),
        (fit1, fit3),
        (fit1, fit4),
        (fit1, grogupy1),
        (fit1, grogupy2),
        (fit1, grogupy3),
        (fit1, grogupy4),
    ]
    for first, second in simulation_pairs:
        print("first: ", first)
        print("second: ", second)
        for mag0, mag1 in zip(
            first["on-site"]["magnetic_entities"],
            second["on-site"]["magnetic_entities"],
        ):
            print(mag0["tag"], mag1["tag"])
            assert mag0["tag"] == mag1["tag"]
            print(mag0["K"], mag1["K"])
            assert (mag0["K"] == mag1["K"]).all()

        for pair0, pair1 in zip(
            first["exchange"]["pairs"], second["exchange"]["pairs"]
        ):
            print(pair0["iso"], pair1["iso"])
            print(pair0["DM"], pair1["DM"])
            print(pair0["S"], pair1["S"])
            assert pair0["iso"] == pair1["iso"]
            assert (pair0["DM"] == pair1["DM"]).all()
            assert (pair0["S"] == pair1["S"]).all()

    os.remove("./tests/test_3_sequential_k.magnopy.txt")
    os.remove("./tests/test_3_parallel_k.magnopy.txt")
    os.remove("./tests/test_3_sequential_all.magnopy.txt")
    os.remove("./tests/test_3_parallel_all.magnopy.txt")
    os.remove("./tests/test_matlab_3_sequential_k.magnopy.txt")
    os.remove("./tests/test_matlab_3_parallel_k.magnopy.txt")
    os.remove("./tests/test_matlab_3_sequential_all.magnopy.txt")
    os.remove("./tests/test_matlab_3_parallel_all.magnopy.txt")
    os.remove("./tests/test_3_sequential_k.pkl")
    os.remove("./tests/test_3_parallel_k.pkl")
    os.remove("./tests/test_3_sequential_all.pkl")
    os.remove("./tests/test_3_parallel_all.pkl")
    os.remove("./tests/test_matlab_3_sequential_k.pkl")
    os.remove("./tests/test_matlab_3_parallel_k.pkl")
    os.remove("./tests/test_matlab_3_sequential_all.pkl")
    os.remove("./tests/test_matlab_3_parallel_all.pkl")
