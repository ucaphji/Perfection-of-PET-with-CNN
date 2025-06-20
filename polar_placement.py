import numpy as np

# 参数设置
num_layers = 5                # 极角分层数（从30°到150°均匀分布）
radius = 82.5                 # 球面半径(mm) = (Rmin+Rmax)/2 = (80+85)/2
output_file = "polar_placements.txt"

# 生成极角（θ从30°到150°均匀分布）
theta_angles = np.linspace(30, 150, num_layers)

# 写入文件（格式：phi theta psi x y z）
with open(output_file, "w") as f:
    f.write("Time phi theta x y z\n")  # 必须的首行
    f.write("0 0 30 0 0 71.453\n")  # 时间固定为0（静态排列）
    f.write("0 0 60 0 0 41.250\n")
    for theta in theta_angles:
        # 计算笛卡尔坐标（球面转直角坐标）
        theta_rad = np.radians(theta)
        z = radius * np.cos(theta_rad)
        xy_plane_radius = radius * np.sin(theta_rad)
        
        # 每层固定phi=0（实际phi由ring repeater控制）
        f.write(f"0 {theta:.1f} 0 0 0 {z:.3f}\n")

print(f"已生成 {output_file}，包含 {num_layers} 层极角排列")