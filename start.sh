#!/bin/bash
# Kiro Bypass Tool - Linux/macOS Start Script

echo "========================================"
echo "Kiro IDE Bypass Tool"
echo "========================================"
echo

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_PATH="$SCRIPT_DIR/kiro_env"

# Check if environment exists
if [ ! -d "$ENV_PATH" ]; then
    echo "[ERROR] Conda environment not found"
    echo "Please run setup.sh first"
    exit 1
fi

# Initialize conda for shell
eval "$(conda shell.bash hook)"

# Activate conda environment
conda activate "$ENV_PATH"
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate conda environment"
    exit 1
fi

echo "[OK] Environment activated"
python --version
echo

# Run main script
python kiro_main.py

# Deactivate environment on exit
conda deactivate
