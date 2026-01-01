#!/bin/bash
# Kiro Bypass Tool - Linux/macOS Setup Script (Conda)

echo "========================================"
echo "Kiro IDE Bypass Tool - Setup (Conda)"
echo "========================================"
echo ""

# Function to install Miniconda
install_miniconda() {
    echo "[INFO] Conda not found, attempting to install Miniconda..."
    echo ""
    
    # Detect OS
    OS="$(uname -s)"
    ARCH="$(uname -m)"
    
    case "$OS" in
        Linux*)
            # Check if Ubuntu/Debian
            if command -v apt-get &> /dev/null; then
                echo "Detected Ubuntu/Debian system"
                echo "Installing Miniconda..."
                
                # Download Miniconda
                if [ "$ARCH" = "x86_64" ]; then
                    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
                elif [ "$ARCH" = "aarch64" ]; then
                    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"
                else
                    echo "[ERROR] Unsupported architecture: $ARCH"
                    exit 1
                fi
                
                # Download and install
                curl -fsSL "$MINICONDA_URL" -o /tmp/miniconda.sh
                if [ $? -ne 0 ]; then
                    wget -q "$MINICONDA_URL" -O /tmp/miniconda.sh
                fi
                
                if [ ! -f /tmp/miniconda.sh ]; then
                    echo "[ERROR] Failed to download Miniconda"
                    exit 1
                fi
                
                bash /tmp/miniconda.sh -b -p "$HOME/miniconda3"
                rm /tmp/miniconda.sh
                
                # Initialize conda
                "$HOME/miniconda3/bin/conda" init bash
                
                echo ""
                echo "[OK] Miniconda installed successfully"
                echo ""
                echo "========================================"
                echo "IMPORTANT: Please restart your terminal"
                echo "and run ./setup.sh again!"
                echo "========================================"
                exit 0
            else
                echo "[ERROR] Unsupported Linux distribution"
                echo "Please install Miniconda manually:"
                echo "https://docs.conda.io/en/latest/miniconda.html"
                exit 1
            fi
            ;;
        Darwin*)
            echo "Detected macOS system"
            echo "Installing Miniconda..."
            
            if [ "$ARCH" = "x86_64" ]; then
                MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
            elif [ "$ARCH" = "arm64" ]; then
                MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
            else
                echo "[ERROR] Unsupported architecture: $ARCH"
                exit 1
            fi
            
            curl -fsSL "$MINICONDA_URL" -o /tmp/miniconda.sh
            
            if [ ! -f /tmp/miniconda.sh ]; then
                echo "[ERROR] Failed to download Miniconda"
                exit 1
            fi
            
            bash /tmp/miniconda.sh -b -p "$HOME/miniconda3"
            rm /tmp/miniconda.sh
            
            # Initialize conda
            "$HOME/miniconda3/bin/conda" init bash zsh
            
            echo ""
            echo "[OK] Miniconda installed successfully"
            echo ""
            echo "========================================"
            echo "IMPORTANT: Please restart your terminal"
            echo "and run ./setup.sh again!"
            echo "========================================"
            exit 0
            ;;
        *)
            echo "[ERROR] Unsupported OS: $OS"
            echo "Please install Miniconda manually:"
            echo "https://docs.conda.io/en/latest/miniconda.html"
            exit 1
            ;;
    esac
}

# Check conda installation
if ! command -v conda &> /dev/null; then
    install_miniconda
fi

echo "[OK] Conda found"
conda --version
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_NAME="kiro_env"
ENV_PATH="$SCRIPT_DIR/$ENV_NAME"

# Check if environment already exists
if [ -d "$ENV_PATH" ]; then
    echo "[INFO] Environment already exists at $ENV_PATH"
    echo "Skipping environment creation..."
else
    echo "Creating conda environment with Python 3.11..."
    conda create -y -p "$ENV_PATH" python=3.11
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create conda environment"
        exit 1
    fi
    echo "[OK] Conda environment created"
fi

echo ""
echo "Activating environment..."

# Initialize conda for shell
eval "$(conda shell.bash hook)"

conda activate "$ENV_PATH"
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate conda environment"
    exit 1
fi

echo "[OK] Environment activated"
python --version
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo ""
echo "[OK] Dependencies installed"
echo ""

# Verify Kiro installation
echo "Verifying Kiro installation..."
python kiro_config.py
if [ $? -ne 0 ]; then
    echo "[WARNING] Kiro verification had issues"
    echo "Please check the output above"
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the tool:"
echo "  ./start.sh"
echo "  or: python kiro_main.py"
echo ""
echo "For help, see docs/QUICKSTART.md"
echo ""
