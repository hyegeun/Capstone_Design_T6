# Start FROM Nvidia PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:pytorch
FROM nvcr.io/nvidia/pytorch:21.10-py3

# Install linux packages
RUN apt update && apt install -y zip htop screen libgl1-mesa-glx

# Install pip packages
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip uninstall -y torch torchvision torchtext Pillow
RUN pip install --no-cache -r requirements.txt albumentations wandb gsutil notebook Pillow>=9.1.0 \
    --extra-index-url https://download.pytorch.org/whl/cu113

# Create working directory
RUN mkdir -p /var/lib/docker/volumes/harbor/yolov5
WORKDIR /var/lib/docker/volumes/harbor/yolov5

# Copy contents
COPY . /var/lib/docker/volumes/harbor/yolov5

# Downloads to user config dir
ADD https://ultralytics.com/assets/Arial.ttf https://ultralytics.com/assets/Arial.Unicode.ttf /root/.config/Ultralytics/

# Set environment variables
ENV OMP_NUM_THREADS=8

