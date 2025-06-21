from rotation import *

def GenEllipsoid(Pos,Angle,Radius,Mu,Box,n=64):

    rotation = ellip_Rotation3d(Angle)

    for i in range(n):
        for j in range(n):
            for k in range(n):

                # Normalisation:
                pos3d = np.matrix([[i - Pos[0]], [j - Pos[1]], [k - Pos[2]]])
                pos3d_Rotate = ellip_trans(rotation, pos3d)

                if ((pos3d_Rotate[0, 0]) ** 2) / (Radius[0] ** 2) + ((pos3d_Rotate[1, 0]) ** 2) / (Radius[1] ** 2) + \
                        ((pos3d_Rotate[2, 0]) ** 2) / (Radius[2] ** 2) <= 1:
                    Box[i][j][k] += Mu

    return Box