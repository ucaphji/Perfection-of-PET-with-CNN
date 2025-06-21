Below is the explaination of code.

1. Read And Write Bin files.py:
  save_image_bin(grid, string):
Save a 3D numpy array grid (arranged as [z, y, x]) as a .bin file.
The transposed order (2,1,0) turns [z,y,x] into [x,y,z] (i.e. GATE/STIR compatible order).
The data is written as float32, a common type in medical image processing

  read_image_bin(string, gridsize):
Read data from a .bin file
Reverse transpose and restore to a 3D numpy array in [z,y,x] order

2. actGate.py:
  ActGate:
Create a simple "point source image", that is, in a 3D grid, only one voxel at the center has a value of 1, and the rest are all 0

3. rotation.py:
There are three functions: R(x),R(y),R(z). They represent 3D rotation matrices for rotations around the x/y/z axes respectively.
  ellip_Rotation3d(Angle):
This function rotates the angle Angle = [phi, theta, psi] around the x -> y -> z axis in sequence to construct a total 3D rotation matrix.
  ellip_trans(R, Coor):
Apply the rotation matrix R to the 3D coordinate Coor and return the new rotated coordinate.

4. randomSeed.py:
This file is used to generate some random values in medical images. It will ensure the GATE will simulate different images.

5. createHeader.py:
Generate .h33 header file (STIR/GATE format)

6. EllipGenerator.py:
In a three-dimensional phantom (Box), an ellipsoid with arbitrary rotation direction, arbitrary position, arbitrary size, and arbitrary μ value is inserted to simulate a target with specific attenuation characteristics (such as tumors, lesions, artifacts, etc.)