#!/bin/bash

# 设置应用程序源代码目录
APP_DIR="/home/rosetta/Desktop/code/data_structures/program_Training"

# 授权 Docker 容器访问 X11 服务
xhost +local:docker

# 运行 PyQt 应用程序
docker run -it \
    -e DISPLAY=$DISPLAY \
    -e QT_QPA_PLATFORM=xcb \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$APP_DIR:/app" \
    fadawar/docker-pyqt5 \
    bash -c "cd /app "