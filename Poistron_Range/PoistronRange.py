import numpy as np

# order: F18, C11. O15, Ga68, Rb82, Zr89, Cu64, I124
radionuclidelist = ["F18", "C11", "O15", "Ga68", "Rb82", "Zr89", "Cu64", "I124"]
Emax = [[0.635], [0.961], [1.723], [1.899], [2.605, 3.381], [0.902], [0.653], [1.535, 2.138]]
Frac = [[1], [1], [1], [1], [0.138, 0.862], [1], [1], [0.522, 0.478]]
Z = [8, 5, 7, 30, 36, 39, 28, 52]


def find_position(string, stringlist):
    for idx in range(0, len(stringlist)):
        if (stringlist[idx] == string):
            break
    return idx


def extract_Gate_info(filename, columns):
    # ex: [1,2,3] for coordinates, 4 is energy...
    with open(filename, 'r') as f:
        line_content = f.readlines()
    f.close()
    line_content = [x.split() for x in line_content]
    line_content = np.asarray(line_content)
    new_content = []
    if len(columns) == 1:
        for x in line_content:
            new_content.append(type_conversion(x[columns[0]]))
    else:
        new_content = [type_conversion(x[columns]) for x in line_content]
    return new_content


def type_conversion(x):
    xnew = []
    for elem in x:
        try:
            xnew.append(np.float64(elem))
        except ValueError:
            xnew.append(str(elem))
    return xnew


def cleanup_energy_distribution(energylist, coordx='', coordy='', coordz=''):
    energydis = []
    if (coordx == ''):
        for x in energylist:
            energydis.append(x[3])
    else:
        coordx = float(coordx)
        coordy = float(coordy)
        coordz = float(coordz)
        for x in energylist:
            if (x[0] == coordx and x[1] == coordy and x[2] == coordz):
                energydis.append(x[3])
    return energydis


def readGateHistogram(filename, skippedLines):
    with open(filename, 'r') as f:
        line_content = f.readlines()[skippedLines:]
    f.close()
    line_content = [x.split() for x in line_content]
    line_content = np.asarray(line_content)
    [val, nb] = zip(*line_content)
    val = np.float64(val)
    nb = np.float64(nb)
    return [val, nb]


def get_coordmat(coord_list, xpos, ypos, zpos):
    xlist = []
    ylist = []
    zlist = []
    for r in coord_list:
        xlist.append(r[0] - xpos)
        ylist.append(r[1] - ypos)
        zlist.append(r[2] - zpos)
    return [xlist, ylist, zlist]


def sample_coords_distribution(xlist, ylist, zlist, samples=500, tail=0.001):
    newlist = xlist + ylist + zlist
    newlist.sort()
    # Need to remove the tail
    newlist = newlist[int(len(newlist) * tail):int(len(newlist) * (1 - tail))]
    step = np.round((newlist[-1] - newlist[0]) / samples, 4)
    nb, value = np.histogram(newlist, bins=np.arange(newlist[0], newlist[-1], step))
    samplingstep = value[1] - value[0]
    value = value + samplingstep / 2
    value = np.delete(value, -1)
    return [value, nb]


def get_distance_list(coord_list, xpos, ypos, zpos):
    distancelist = []
    for r in coord_list:
        distancelist.append(np.sqrt((r[0] - xpos) ** 2 + (r[1] - xpos) ** 2 + (r[2] - xpos) ** 2))
    return distancelist


def cleanup_distance_list(distancelist):
    for i in range(len(distancelist) - 1):
        if np.abs(distancelist[i] - distancelist[i + 1]) > 10:
            distancelist = distancelist[0:i]
            break
    return distancelist


def sample_distribution(distancelist, samples=500, tail=0.001):
    distancelist.sort()
    # Need to remove the tail
    distancelist = distancelist[int(len(distancelist) * tail):int(len(distancelist) * (1 - tail))]
    step = np.round((distancelist[-1] - distancelist[0]) / samples, 4)
    nb, value = np.histogram(distancelist, bins=np.arange(distancelist[0], distancelist[-1], step))
    print(step)
    samplingstep = value[1] - value[0]
    value = value + samplingstep / 2
    value = np.delete(value, -1)
    return [value, nb]


def plot_cumulated_distribution(value, nb):
    cumulatednb = np.cumsum(nb)
    return cumulatednb


def distribution_energy(Erange, radionuclide):
    N = np.zeros(np.shape(Erange))
    idx = find_position(radionuclide, radionuclidelist)
    Zr = Z[idx]
    transitionNb = 0
    for Emr in Emax[idx]:
        Ntmp = []
        for E in Erange:
            if (E < Emr and E > 0):
                p = np.sqrt((1 + E / 0.511) ** 2 - 1)
                alpha = 1 / 137
                eta = -Zr * alpha / p * (1 + E / 0.511)
                F = 2 * np.pi * eta / (1 - np.exp(-2 * np.pi * eta))
                Ntmp.append(p * F * (1 + E / 0.511) * (Emr - E) ** 2)
            else:
                Ntmp.append(0.)
        N += Frac[idx][transitionNb] * np.asarray(Ntmp)
        transitionNb += 1
    return N / sum(N)


def clean_up_voxelised_data_all_strings(filecontent, lasteventfrompreviouslist=[]):
    newlist = []  # origin coord (x,y,z) annihilation coord (x,y,z)
    if (len(lasteventfrompreviouslist) > 0 and len(filecontent) > 0):
        test_two_elems_list_all_strings(lasteventfrompreviouslist, filecontent[0], newlist)
    for i in range(0, len(filecontent) - 1):
        if (test_two_elems_list_all_strings(filecontent[i], filecontent[i + 1], newlist)):
            i += 1
    return newlist


def clean_up_voxelised_data_one_medium(filecontent, medium, lasteventfrompreviouslist=[]):
    newlist = []  # origin coord (x,y,z) annihilation coord (x,y,z)
    if (len(lasteventfrompreviouslist) > 0 and len(filecontent) > 0):
        test_two_elems_list_one_medium(lasteventfrompreviouslist, filecontent[0], newlist, medium)
    for i in range(0, len(filecontent) - 1):
        if (test_two_elems_list_one_medium(filecontent[i], filecontent[i + 1], newlist, medium)):
            i += 1
    return newlist


def test_two_elems_list_all_strings(elem1, elem2, newlist):
    isAdded = False
    if (elem1[5] == 'initStep' and elem2[5] == 'annihil'):
        newlist.append([elem1[0], elem1[1], elem1[2], elem2[0], elem2[1], elem2[2]])
        isAdded = True
    return isAdded


def test_two_elems_list_one_medium(elem1, elem2, newlist, medium):
    isAdded = False
    if (elem1[5] == 'initStep' and elem1[4] == medium and elem2[5] == 'annihil'):
        newlist.append([elem1[0], elem1[1], elem1[2], elem2[0], elem2[1], elem2[2]])
        isAdded = True
    return isAdded


def find_interval(elemx, elemy, elemz, xs, ys, zs):
    iterx = 0
    for x in xs:
        if (float(elemx) < x):
            break
        else:
            iterx += 1
    itery = 0
    for y in ys:
        if (float(elemy) < y):
            break
        else:
            itery += 1
    iterz = 0
    for z in zs:
        if (float(elemz) < z):
            break
        else:
            iterz += 1
    return [iterx, itery, iterz]


def resample_list_to_grid(filecontent, sizex, sizey, sizez, spacing):
    # Compute lists of coordinate minima
    xs = np.arange(1, sizex + 1) * spacing - (sizex * spacing) / 2 * np.ones(sizex)
    ys = np.arange(1, sizey + 1) * spacing - (sizey * spacing) / 2 * np.ones(sizey)
    zs = np.arange(1, sizez + 1) * spacing - (sizez * spacing) / 2 * np.ones(sizez)
    grid1 = np.zeros([sizex, sizey, sizez])
    grid2 = np.zeros([sizex, sizey, sizez])
    for elem in filecontent:
        [x, y, z] = find_interval(elem[0], elem[1], elem[2], xs, ys, zs)
        try:
            grid1[x, y, z] += 1
        except IndexError:
            print(x, y, z, "out of bounds")
        [x2, y2, z2] = find_interval(elem[3], elem[4], elem[5], xs, ys, zs)
        try:
            grid2[x2, y2, z2] += 1
        except IndexError:
            print(x2, y2, z2, "out of bounds")
    return [grid1, grid2, xs, ys, zs]


# %% Curve fitting functions - check if scipy.optimize can be imported

try:
    from scipy.optimize import curve_fit
except ImportError:
    print("Curve fitting functions cannot be imported because scipy package is missing!")
else:
    # Model: distr(r)=C[(a-r+1)[1-r/r0]^n-eps/r^n]
    def fit_function_positron_range(r, r0, a, n, eps, C):
        ret_func = np.zeros(np.size(r))
        for i in range(np.size(r)):
            if (r[i] <= r0 and r[i] > 0):
                ret_func[i] = C * ((a - r[i] + 1) * (np.power(1 - r[i] / r0, n)) - eps / (np.power(r[i], n)))
            else:
                ret_func[i] = 0
        return ret_func


    def curve_fitting_positron_range(positronrangearray, nbofevents):
        # init_vals=[positronrangearray[100],0.01,2,0.00001,nbofevents.max()]
        init_vals = [positronrangearray[-1], 2, 2, 0.00001, nbofevents.max()]
        theBounds = (0, np.inf)
        params = curve_fit(fit_function_positron_range, positronrangearray, nbofevents, p0=init_vals, bounds=theBounds)
        return [fit_function_positron_range(positronrangearray, params[0][0], params[0][1], params[0][2], params[0][3],
                                            params[0][4]), params[0][0], params[0][1], params[0][2], params[0][3],
                params[0][4]]


    def fitting_function_uniform(x, a0, alpha0, b0, beta0, mu):
        # return 0 + a0*np.exp(-alpha0*np.abs(x))+b0*np.exp(-beta0*np.abs(x))
        return 0 + a0 * np.exp(-alpha0 * np.abs(x)) + (1 - a0) * np.exp(-beta0 * np.abs(x))


    def fitting_function_interface(x, a0, alpha0, b0, beta0, mu, x0, a1, alpha1, b1, beta1):
        return np.piecewise(x, [abs(x) <= x0],
                             [lambda x: mu + a0 * np.exp(-alpha0 * np.abs(x)) + b0 * np.exp(-beta0 * np.abs(x)),
                              lambda x: mu + a1 * np.exp(-alpha1 * np.abs(x)) + b1 * np.exp(-beta1 * np.abs(x))])


    def get_kernel_fit(coordarray, nbofevents, x0=0):
        a0 = npfy.max(nbofevents) / 2
        b0 = a0
        if (x0 == 0):
            params = curve_fit(fitting_function_uniform, np.asarray(coordarray), np.asarray(nbofevents),
                               p0=[a0, 0, b0, 0, 0])
            return [fitting_function_uniform(np.asarray(coordarray), params[0][0], params[0][1], params[0][2],
                                             params[0][3], params[0][4]), params]
        else:
            params = curve_fit(fitting_function_interface, np.asarray(coordarray), np.asarray(nbofevents),
                               p0=[a0, 1, b0, 1, 0, x0, a0, 1, b0, 1])
            return [fitting_function_interface(np.asarray(coordarray), params[0][0], params[0][1], params[0][2],
                                               params[0][3], params[0][4], params[0][5], params[0][6], params[0][7],
                                               params[0][8], params[0][9]), params]
