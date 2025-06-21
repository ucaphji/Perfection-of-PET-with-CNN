import numpy as np
import math

# R(x) -> R(y) -> R(z)
def Rx(phi):  # phi: (-pi, pi)
    return np.matrix([[1, 0, 0],
                      [0, math.cos(phi), -math.sin(phi)],
                      [0, math.sin(phi), math.cos(phi)]])

def Ry(theta):  # theta: (-pi/2,pi/2)
    return np.matrix([[math.cos(theta), 0, math.sin(theta)],
                      [0, 1, 0],
                      [-math.sin(theta), 0, math.cos(theta)]])

def Rz(psi):  # psi: (-pi, pi)
    return np.matrix([[math.cos(psi), -math.sin(psi), 0],
                      [math.sin(psi), math.cos(psi), 0],
                      [0, 0, 1]])

def ellip_Rotation3d(Angle):
    return Rz(Angle[2]) * Ry(Angle[1]) * Rx(Angle[0])

def ellip_trans(R,Coor):
   return R.dot(Coor)