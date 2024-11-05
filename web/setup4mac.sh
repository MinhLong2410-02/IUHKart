#!/bin/bash

# Kiểm tra xem môi trường ảo đã tồn tại hay chưa
if [ ! -d "base" ]; then
    echo "Môi trường ảo không tồn tại. Đang tạo môi trường ảo..."
    python3 -m venv base || { echo "Không thể tạo môi trường ảo"; exit 1; }
fi

# Kích hoạt môi trường ảo
source base/bin/activate || { echo "Không thể kích hoạt môi trường ảo"; exit 1; }

# cài thư viện
pip3 install -r requirements.txt || { echo "Không thể cài thư viện"; exit 1; }

# Deactivate the virtual environment
deactivate || { echo "Không thể tắt môi trường ảo"; exit 1; }