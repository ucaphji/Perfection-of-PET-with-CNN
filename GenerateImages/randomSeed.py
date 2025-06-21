import numpy as np
import math

# Generate random int, 1 - 10 --> change to just 1 ellipsoid
def GenRandomInt():
    GenInt = np.random.randint(1, 2)
    return GenInt

# Generate random Position, orientation，scale and Mu for ellipsoid
# random lung:
def GenRandomLung():
    lung = np.random.randint(200,300)
    return lung

# random Mu
def GenRandomMu():
    Mu = np.random.randint(-10, 600)  # -0.01 - 0.6 *1000
    return Mu

def ellip_Pos3d():
    pos_x = np.random.randint(12,52)
    pos_y = np.random.randint(12,52)
    pos_z = np.random.randint(12,52)
    GenPos = [pos_x, pos_y, pos_z]
    return GenPos

def ellip_Radius3d():
    r_x = np.random.randint(1, 32)
    r_y = np.random.randint(1, 32)
    r_z = np.random.randint(1, 32)
    GenScale = [r_x, r_y, r_z]
    return GenScale

# x, y, z rotation

def ellip_Angle3d():
    phi = np.random.uniform(-math.pi, math.pi)
    theta = np.random.uniform(-math.pi / 2, math.pi / 2)
    psi = np.random.uniform(-math.pi, math.pi)
    return [phi, theta, psi]