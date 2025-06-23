import os
from tqdm import tqdm

import numpy as np

from actGate import *
from readAndWriteBinFIles import *
from ellipGenerator import *
from randomSeed import *
from createHeader import *

NUM_FILES = 500 #it can be changed as you want
VOLUME_SIZE = 64
VOLUME_WIDTH = [1.0, 1.0, 1.0]
OUTPUT_DIR = "./header"


def generate_lung_box(n):
    return np.ones((n, n, n)) * GenRandomLung()

def add_random_ellipsoids(Box, n):
    times = GenRandomInt()
    for _ in range(times):
        Pos = ellip_Pos3d()
        Angle = ellip_Angle3d()
        Radius = ellip_Radius3d()
        Mu = GenRandomMu()
        Box = GenEllipsoid(Pos, Angle, Radius, Mu, Box, n)
    return Box

def generate_actgate(n, output_dir):
    ag = ActGate(n)
    file_name = "ActGate"
    bin_path = os.path.join(output_dir, file_name + ".bin")
    hdr_path = os.path.join(output_dir, file_name + ".h33")

    size = [n, n, n]
    width = [1.0, 1.0, 1.0]

    save_image_bin(ag, bin_path)
    createH33Header(size, width, file_name + ".bin", hdr_path)

def main():
    n = VOLUME_SIZE
    size = [n, n, n]
    width = VOLUME_WIDTH
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for fileNumber in tqdm(range(NUM_FILES), desc="Generating volumes"):
        Box = generate_lung_box(n)
        Box = add_random_ellipsoids(Box, n)

        fileName = f"AtnGate{fileNumber+1}"
        bin_path = os.path.join(OUTPUT_DIR, fileName + ".bin")
        hdr_path = os.path.join(OUTPUT_DIR, fileName + ".h33")

        createH33Header(size, width, fileName + ".bin", hdr_path)
        save_image_bin(Box.astype(np.float32), os.path.join(OUTPUT_DIR, fileName))

    generate_actgate(n, OUTPUT_DIR)

if __name__ == "__main__":
    main()
