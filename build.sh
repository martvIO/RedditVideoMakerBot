#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define Python version
PYTHON_VERSION=3.10.6

# Update and install prerequisites
echo "Updating package list and installing prerequisites..."
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y software-properties-common wget build-essential libssl-dev zlib1g-dev \
  libncurses5-dev libnss3-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev \
  yasm libx264-dev libx265-dev libvpx-dev libopus-dev libmp3lame-dev libfdk-aac-dev

# Install ffmpeg
echo "Installing ffmpeg..."
sudo apt install -y ffmpeg
ffmpeg -version

# Download and install Python 3.10.6
echo "Downloading and installing Python $PYTHON_VERSION..."
wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz
tar -xvf Python-$PYTHON_VERSION.tgz
cd Python-$PYTHON_VERSION
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
cd ..
rm -rf Python-$PYTHON_VERSION Python-$PYTHON_VERSION.tgz

# Check Python version
python3.10 --version

# Create and activate a new virtual environment
echo "Creating a new virtual environment..."
python3.10 -m venv venv
source venv/bin/activate

# Install requirements from requirements.txt
if [ -f "requirements.txt" ]; then
  echo "Installing requirements from requirements.txt..."
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "requirements.txt not found! Skipping dependencies installation."
fi

# Finish
echo "Setup complete. Virtual environment is ready and activated."
