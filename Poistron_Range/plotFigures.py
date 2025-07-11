import os
import re
import numpy as np
from matplotlib import pyplot as plt

source = ['ion'] 
physics = ['std'] 
radionuclide = 'Ga68' 

# Ga-68 Parameters
bin_width = 0.05  # unit: mm
max_range = 3.0    
bin_input = np.arange(0, max_range, bin_width)

path = '/Users/hr.j//Desktop/GateProject/Perfection-of-PET-with-CNN'
os.chdir(path)
filename = 'HistogramGa68.txt'

with open(filename) as f:
    data = [re.split('[ ]+|\t', x) for x in f.read().split('\n')]
    data = data[:-1]
E = []; P = []
for i in data:
    data1 = []
    for j in range(len(i)):
        if i[j] == str(''):
            pass
        else:
            data1.append(i[j])
    E.append(float(data1[0]))
    P.append(float(data1[1]))

#####################################
# IMPORT SIMULATED EMISSION DATA #
#####################################

#path = '/Users/francescaleek/OneDrive - University College London/PycharmProjects/PycharmProjects_Data/GATE_lungs_data/XCAT/Data/XCAT_Totman/Full_phantom/XCAT_cluster/VoxelisedSimulation/em_annihil'
os.chdir(path)

r_source = []; energies_all = []
for p in physics:
    path_phys = path + '/' + p
    for s in source:
        #os.chdir(path + '/' + p + '/' + s + '_v9_' + radionuclide)  # + '/378200')
        #emlist_v9 = np.loadtxt('em_' + radionuclide + '_' + s + '_' + p + '.txt')
        emlist_v9 = np.loadtxt('em_' + s + '_' + p + '_annihilenabled.txt')
        em_nonzero_v9 = emlist_v9[emlist_v9[:, 3] != 0.000]
        em_positron_v9 = em_nonzero_v9[em_nonzero_v9[:, 3] != 0.511][:, :]

        em_pos_zero_v9 = em_positron_v9[np.linalg.norm(em_positron_v9[:, :2], axis=1) == 0.00000]
        em_pos_v9 = em_pos_zero_v9[em_pos_zero_v9[:, 3] >= 0.0001]  # greater than 100 eV
        energies_v9 = em_pos_v9[:, 3]
        energies_all.append(energies_v9)

# %%
###################################################################
# PLOT ALL EMISSION DATA AGAINST THE USER-DEFINED HISTOGRAM INPUT #
###################################################################

fig = plt.figure()
ax = fig.add_subplot(111)
n, bins, rectangles = ax.hist(em_positron_v9[:, 3], bins=bin_input, density=True, label='livermore, ion', histtype='step') #bins=100, density=True)

P_normed = [i * (np.max(n) / np.max(P)) for i in P]
plt.scatter(E, P_normed, c='black', s=1, label='histogram input')
plt.legend()
plt.xlim(0, 2.0)
plt.xlabel('E (MeV)')
plt.ylabel('events')
plt.title('Probability density of initSteps vs Elises histogram input \n ' + radionuclide + ' source')

os.chdir(path)
plt.savefig('em_' + radionuclide + '_all_v9')


# %%
#############################################
# IMPORT SINGLE SIMULATED ANNIHILATION DATA #
#############################################

r_source = []
for s in source:
    for p in physics:
        annlist_v9 = np.loadtxt('annihil_' + s + '_' + p + '_annihilenabled.txt')

# %%
#################################
# PLOT SINGLE ANNIHILATION DATA #
#################################

plt.figure(figsize=(10, 6))

max_energy = 1.899      
cutoff_range = 4.0 

ann_removeMax = annlist_v9[annlist_v9[:, 3] < cutoff_range] 

bin_count = 80  # Reduced bin count compared to the F-18 to accommodate longer range
plt.hist(ann_removeMax[:,3], 
         bins=bin_count,
         density=True,  
         alpha=0.7,
         label=f'Ga-68 (E_max={max_energy}MeV)')

plt.xlabel('Positron Range (mm)', fontsize=12)
plt.ylabel('Normalized Counts', fontsize=12)
plt.title(f'Positron Range Distribution in {source[0]}\n(Ga-68, XCAT Phantom)', 
          fontsize=14, pad=20)

plt.xlim(0, cutoff_range)
plt.axvline(x=max_range, color='r', linestyle='--', 
            label=f'Theoretical max ({max_range}mm)')

output_filename = f'annihil_{radionuclide}_{source[0]}_Ga68.png'
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.close()

# %%
##############################
# LOAD ALL ANNIHILATION DATA #
##############################
dist_all = []; annlist_all = []; emlist_all = []
for p in physics:
    path_phys = path + '/' + p
    for s in source:
        os.chdir(path_phys + '/' + s + '_v9_' + radionuclide)
        emlist = np.loadtxt('em_' + radionuclide + '_' + s + '_' + p + '.txt')
        annlist = np.loadtxt('annihil_' + radionuclide + '_' + s + '_' + p + '.txt')
        emlist_all.append(emlist)
        annlist_all.append(annlist)
        dist = np.linalg.norm(annlist, axis=1)
        dist_all.append(dist)

# %%
#############################################
# PLOT ALL ANNIHILATION HISTOGRAMS TOGETHER #
#############################################
bin_width = 0.0499 #0.0499 0.0125
bin_input = np.arange(0, 2.5, bin_width) # F-18 2.5
plt.figure()
n_liv_ion, b_liv_ion, r_liv_ion = plt.hist(dist_all[0], bins=bin_input, label='livermore, ion', histtype='step') #, density=True)
n_liv_e, b_liv_e, r_liv_e = plt.hist(dist_all[1], bins=bin_input, label='livermore, positron', histtype='step') #, density=True)
n_pen_ion, b_pen_ion, r_pen_ion = plt.hist(dist_all[2], bins=bin_input, label='penelope, ion', histtype='step') #, density=True)
n_pen_e, b_pen_e, r_pen_e = plt.hist(dist_all[3], bins=bin_input, label='penelope, positron', histtype='step') #, density=True)
plt.xlabel('range (mm)')
plt.ylabel('events')
plt.title('Distance to annihilation from F18 point source \n located at centre of sphere of water')
plt.xlim(0, 2.5) # F-18 2.5 Rb-82 20
plt.legend()
os.chdir(path)
plt.savefig('annihil_' + radionuclide + '_all_v9')

################################
# CALCULATE EXTRAPOLATED RANGE #
################################
n_all = [n_liv_ion, n_liv_e, n_pen_ion, n_pen_e]
np.savetxt('n_all', n_all)
b_min_all = []; b_max_all = []; n_min_all = []; n_max_all = []
for n in n_all:
    # n_max = np.max(n)
    # n_80perc = n_max * 0.8
    # n_20perc = n_max = 0.2
    n_max_index = np.argmax(n)
    b_min = bin_input[n_max_index + 2]
    b_max = bin_input[n_max_index + 14]
    n_min = n[n_max_index + 2]
    n_max = n[n_max_index + 14]
    b_min_all.append(b_min)
    b_max_all.append(b_max)
    n_min_all.append(n_min)
    n_max_all.append(n_max)


# %%
###############################################
# ABANDONED ATTEMPT TO REPLICATE CAL-GONZALEZ #
###############################################
import PositronRange_FL as pr
annihil_one = annlist_all[0]
#for a in annlist_all[0]:
spacingImage = 0.1
[zdim, ydim, xdim] = [300, 300, 300]  # [2000, 2000, 700] #[202, 202, 201]

eventlist = annihil_one.tolist()

xs = np.arange(1, xdim + 1) * spacingImage - (xdim * spacingImage) / 2 * np.ones(xdim)
ys = np.arange(1, ydim + 1) * spacingImage - (ydim * spacingImage) / 2 * np.ones(ydim)
zs = np.arange(1, zdim + 1) * spacingImage - (zdim * spacingImage) / 2 * np.ones(zdim)

annihilationgrid = np.zeros([zdim, ydim, xdim])

for elem in eventlist:
    elem = np.array(elem)
    [z, y, x] = pr.find_interval(elem[2], elem[1], elem[0], zs, ys, xs)
    try:
        annihilationgrid[z, y, x] += 1
    except IndexError:
        print(z, y, x, "out of bounds")

# %%
annihil_2D = np.sum(annihilationgrid, axis=0)
x_max = 150
x_range = np.arange(x_max - 30), (x_max + 31)
y = annihil_2D[x_range][x_max]
plt.figure()
plt.plot(x_range, y)