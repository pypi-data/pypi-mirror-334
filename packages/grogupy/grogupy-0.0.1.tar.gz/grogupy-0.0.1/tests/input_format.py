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
infolder = "/Users/danielpozsar/Downloads/lat3_791"
infile = "Fe3GeTe2.fdf"
# kset should be at leas 100x100 for 2D diatomic systems
kset = [10, 10, 1]
# eset should be 100 for insulators and 1000 for metals
eset = 100
# esetp should be 600 for insulators and 10000 for metals
esetp = 600
# emin None sets the minimum energy to the minimum energy in the eigfile
emin = None
# emax is at the Fermi level at 0
emax = 0
# the bottom of the energy contour should be shifted by -5 eV
emin_shift = -5
# the top of the energy contour can be shifted to the middle of the gap for insulators
emax_shift = -0.22
# usually the DFT calculation axis is [0, 0, 1]
scf_xcf_orientation = [0, 0, 1]
# the reference directions for the energy derivations
ref_xcf_orientations = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
# matlabmode is only for testing purposes
matlabmode = False

# magnetic entities and pairs can be defined manually
"""setup_from_range = False
magnetic_entities = [
    dict(atom=3, l=2),
    dict(atom=4, l=2),
    dict(atom=5, l=2),
]
pairs = [
    dict(ai=0, aj=1, Ruc=[0, 0, 0]),
    dict(ai=0, aj=2, Ruc=[0, 0, 0]),
    dict(ai=1, aj=2, Ruc=[0, 0, 0]),
    dict(ai=0, aj=0, Ruc=[1, 0, 0]),
    dict(ai=0, aj=1, Ruc=[1, 0, 0]),
    dict(ai=0, aj=2, Ruc=[1, 0, 0]),
    dict(ai=0, aj=0, Ruc=[2, 0, 0]),
]"""

# magnetic entities and pairs can be defined automatically from the cutoff radius and magnetic atoms
setup_from_range = True
radius = 10
atomic_subset = "Fe"
kwargs_for_mag_ent = dict(l=2)

# sequential solver is better for large systems
greens_function_solver = "Parallel"
# always use K for now
parallel_mode = "K"
# the calculation of J and K from the energy derivations, either Fit or grogupy
exchange_solver = "Fit"
anisotropy_solver = "Fit"

# save the magnopy file
save_magnopy = True
# precision of numerical values in the magnopy file
magnopy_precision = None
# add the simulation parameters to the magnopy file as comments
magnopy_comments = True

# save the pickle file
save_pickle = True
# add all the arrays to the pickle file, which can be large
pickle_dump_all = False

# output folder, for example the current folder
outfolder = "./"
# outfile name (this produces the format: SYSTEMLABEL_kset[10,10,1]_eset_600.FILE_FORMAT)
outfile = f"{infile.split('.')[0]}_kset_{'_'.join(map(str, kset))}_eset_{eset}"
