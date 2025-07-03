import PositronRange as pr
import numpy as np
import os
radionuclide = 'Ga68'
fileNumber = 1
path = '/Users/hr.j//Desktop/GateProject/Perfection-of-PET-with-CNN'
os.chdir(path)
spacingImage = 3  # each voxel has a side length of 3 mm
[xdim, ydim, zdim] = [500, 500, 500] 

annihil = np.loadtxt('annihil_' + radionuclide + '_' + fileNumber + '.txt')

dist = np.linalg.norm(annihil, axis=1)  # Euclidean distance from the origin to the annihilation point
Rmean = np.mean(dist)  
Rmax = np.max(dist)

annihilList = annihil.tolist()
xs = np.arange(1, xdim + 1) * spacingImage - (xdim * spacingImage) / 2 * np.ones(xdim)
ys = np.arange(1, ydim + 1) * spacingImage - (ydim * spacingImage) / 2 * np.ones(ydim)
zs = np.arange(1, zdim + 1) * spacingImage - (zdim * spacingImage) / 2 * np.ones(zdim)

annihilationgrid = np.zeros([xdim, ydim, zdim])

for elem in annihilList:
    elem = np.array(elem)
    [x, y, z] = pr.find_interval(elem[0], elem[1], elem[2], xs, ys, zs)
    try:
        annihilationgrid[x, y, z] += 1
    except IndexError:
        print(x, y, z, "out of bounds")
