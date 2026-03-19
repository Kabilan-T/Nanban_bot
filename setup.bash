#!/bin/bash

# Check if script is run from Nanban_bot directory
if [[ ! $(basename "$(pwd)") == "Nanban_bot" ]]; then
    echo "Please run this script from the Nanban_bot directory."
    exit 1
fi

# Check if runtime.txt file exists
if [ ! -f "runtime.txt" ]; then
    echo "runtime.txt not found. Please create runtime.txt and specify the Python version."
    exit 1
fi

# Read Python version from runtime.txt
python_version=$(cat runtime.txt)

# Check if virtual environment exists
if conda env list | grep -q nanban_bot_env; then
    echo "Virtual environment 'nanban_bot_env' already exists."
else
    echo "Creating virtual environment with Python $python_version..."
    # Create virtual environment with specified Python version
    conda create -n nanban_bot_env python="$python_version"
fi

# Activate virtual environment
eval "$(conda shell.bash hook)"
conda activate nanban_bot_env
echo "Virtual environment 'nanban_bot_env' activated."

# install ffmpeg if not installed
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg not found. Installing ffmpeg..."
    conda install -c conda-forge ffmpeg
fi

# Install dependencies
echo "Updating pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
python -m pip install --no-cache-dir -r requirements.txt --use-deprecated=legacy-resolver

echo "Setup complete. Please fill in your bot tokens in tokens.sh and then run the bot using run.bash."

exit 0