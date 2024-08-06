#!/bin/bash
docker pull fadawar/docker-pyqt5


run_file="testrun.py"
APP_DIR="/home/rosetta/Desktop/code/data_structures/program_Training"

# 检查应用程序源代码文件是否存在
if [ ! -f "$APP_DIR/$run_file" ]; then
    echo "Error: hello_pyqt.py file not found in the $APP_DIR directory."
    exit 1
fi

# 运行 PyQt 应用程序
xhost +local:docker
docker run --rm -it \
    -v "/tmp/.X11-unix:/tmp/.X11-unix" \
    -v "$APP_DIR:/tmp" \
    -w /tmp \
    -e DISPLAY=:0 \
    -e QT_X11_NO_MITSHM=1 \
    fadawar/docker-pyqt5 \
    python3 hello_pyqt.py