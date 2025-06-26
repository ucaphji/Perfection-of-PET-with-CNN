#!/bin/bash

# 镜像名称
IMAGE="opengatecollaboration/gate"

# 本地工程路径（根据实际情况修改）
LOCAL_SIM_DIR="/Users/hr.j/Desktop/GateProject/Perfection-of-PET-with-CNN"

# 输出目录
OUTPUT_DIR="$LOCAL_SIM_DIR/images"

# GATE 宏文件路径
MACRO_FILE="/home/gateuser/sim/main.mac"

# 1. 检查镜像是否存在，如果没有则拉取
if [[ "$(docker images -q $IMAGE 2> /dev/null)" == "" ]]; then
  echo "镜像 $IMAGE 不存在，正在拉取..."
  docker pull $IMAGE
else
  echo "镜像 $IMAGE 已存在。"
fi

# 2. 创建输出目录（如果不存在）
if [ ! -d "$OUTPUT_DIR" ]; then
  echo "创建输出目录 $OUTPUT_DIR"
  mkdir -p "$OUTPUT_DIR"
else
  echo "输出目录 $OUTPUT_DIR 已存在。"
fi

# 3. 运行容器
echo "启动容器运行 GATE..."
docker run --rm -it \
  -e DISPLAY=host.docker.internal:0 \
  -e G4RADIOACTIVEDATA=/home/gateuser/RadioactiveDecay \
  -v "$LOCAL_SIM_DIR":/home/gateuser/sim \
  -v "$LOCAL_SIM_DIR/RadioactiveDecay":/home/gateuser/RadioactiveDecay \
  $IMAGE \
  Gate $MACRO_FILE
