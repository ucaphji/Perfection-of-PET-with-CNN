import PositronRange as pr
import ImageTools as elise
import numpy as np
import sys
import os
from matplotlib import pyplot as plt
import pSTIR as pet
from sirf.Reg import NiftiImageData3D
from pUtilities import show_3D_array

radionuclide = 'Ga68' 
source = ['ion_liver']

path = '/Users/hr.j//Desktop/GateProject/Perfection-of-PET-with-CNN'
os.chdir(path)

spacingImage = 0.607 #0.78 #0.607 # 0.5 # mm
spacingSlice = 1.5 #1.5 # 0.5
[xdim,ydim,zdim] = [695, 695, 170] #[2000, 2000, 700] #[202, 202, 201]

eventlist = []
events = np.loadtxt('annihils.txt')
eventlist = events.tolist()

xs = np.arange(1, xdim + 1) * spacingImage - (xdim * spacingImage) / 2 * np.ones(xdim)
ys = np.arange(1, ydim + 1) * spacingImage - (ydim * spacingImage) / 2 * np.ones(ydim)
zs = np.arange(1, zdim + 1) * spacingSlice - (zdim * spacingSlice) / 2 * np.ones(zdim)

annihilationgrid = np.zeros([zdim, ydim, xdim])

for elem in eventlist:
    elem = np.array(elem)
    [x, y, z] = pr.find_interval(elem[0], elem[1], elem[2], xs, ys, zs)
    try:
        annihilationgrid[z, y, x] += 1
    except IndexError:
        print(x, y, z, "out of bounds")

emission = pet.ImageData('Phantom1-SourceMap.hdr')
mumap = pet.ImageData('Phantom1-MuMap.hdr')
image_templ = mumap.copy()
image_templ.fill(0)

annihil_ID = image_templ.copy()
annihil_ID.fill(annihilationgrid)
annihil_ID.write('annihil_ID_100.hv')

import uproot


f = uproot.open('range.root')
x = f['Annihilation']['X'].array(library="np")
y = f['Annihilation']['Y'].array(library="np")
z = f['Annihilation']['Z'].array(library="np")

fig = plt.figure(figsize=(8, 8)) # replace with contour plot
ax = fig.add_subplot(111, projection='3d')
for i in range(0, x.shape[0] - 85867):
    ax.scatter(x[i], y[i], z[i], s=0.5)
ax.set_xlabel('x axis [mm]')
ax.set_ylabel('y axis [mm]')
ax.set_zlabel('z axis [mm]')

plt.show()

pos = np.array((x, y, z))
dist = np.linalg.norm(pos, axis=0)
Rmean = np.mean(dist)
Rmax = np.max(dist)

bin_width = 0.499 #0.0249
bin_input = np.arange(0, 270, bin_width) # F-18 1.805; Rb-82 4.405

plt.figure()
n, bins, rectangles = plt.hist(dist, bin_input)