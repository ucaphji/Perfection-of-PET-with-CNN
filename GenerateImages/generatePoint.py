import os
import numpy as np
from tqdm import tqdm
from actGate import *
from readAndWriteBinFIles import *
from ellipGenerator import *
from randomSeed import *
from createHeader import *

n = 64
spacing = [1.0, 1.0, 1.0]
output_dir = "./output"
filename = "pointInLung"

# 创建 Lung box：每个体素值设为一个典型肺密度（例如 0.25），或使用 GenRandomLung()
lung_density = 0.25  # 或 lung_density = GenRandomLung()
image = np.ones((n, n, n), dtype=np.float32) * lung_density

# 设置中间点为 1.0
center = n // 2
image[center, center, center] = 1.0

# 保存图像与头文件
bin_path = os.path.join(output_dir, filename + ".bin")
hdr_path = os.path.join(output_dir, filename + ".h33")

os.makedirs(output_dir, exist_ok=True)
save_image_bin(image, bin_path)
createH33Header([n, n, n], spacing, filename + ".bin", hdr_path)