import numpy as np

def save_image_bin(grid,string,extension='bin'):
    fid = open('{}.{}'.format(string,extension),'wb')
    gridfile = np.transpose(grid, (2,1,0))
    gridfile=gridfile.flatten()
    gridfile = np.float32(gridfile)
    with open(f'{string}.{extension}', 'wb') as fid:
        gridfile.tofile(fid)
    fid.close()

def read_image_bin(string,gridsize,extension='bin'):
    with open(f'{string}.{extension}', 'rb') as fid:
        grid = np.fromfile(fid, dtype='float32')   
    grid = grid.reshape(gridsize)
    grid = np.transpose(grid, (2,1,0))
    return grid