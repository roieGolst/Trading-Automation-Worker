#!/usr/bin/env bash

set -e
set -o pipefail
set -u

WORK_DIR="$(dirname "$0")/.."
LIB_DIR="$WORK_DIR/lib"
PROJECT_DIR="$LIB_DIR/auto-rsa"
VENV_DIR=".venv"
REPO_URL="https://github.com/roieGolst/auto-rsa.git"

print_message() {
    echo -e "\n\033[1;32m$1\033[0m\n"
}

error_exit() {
    echo -e "\n\033[1;31m$1\033[0m\n" >&2
    exit 1
}

print_message "Cloning the auto-rsa repository..."
mkdir -p "$LIB_DIR"
if [ -d "$PROJECT_DIR" ]; then
    echo "The project directory already exists. Pulling the latest changes..."
    git -C "$PROJECT_DIR" pull || error_exit "Failed to pull the latest changes."
else
    git clone "$REPO_URL" "$PROJECT_DIR" || error_exit "Failed to clone the repository."
fi

cd "$PROJECT_DIR" || error_exit "Failed to navigate to the project directory."

print_message "Checking required tools..."
REQUIRED_PACKAGES=("openssl" "bash" "python3.12" "git")
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if ! command -v "$pkg" &> /dev/null; then
        error_exit "Error: $pkg is not installed. Please install it and re-run the script."
    fi
done

print_message "Setting up a dedicated virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3.12 -m venv "$VENV_DIR" || error_exit "Failed to create a virtual environment."
else
    print_message "Virtual environment already exists. Skipping creation."
fi

source "$VENV_DIR/bin/activate" || error_exit "Failed to activate the virtual environment."

print_message "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip || error_exit "Failed to upgrade pip."
    pip install -r requirements.txt || error_exit "Failed to install dependencies from requirements.txt."
else
    print_message "No requirements.txt file found. Skipping dependency installation."
fi

print_message "Installing Playwright..."
pip install playwright || error_exit "Failed to install Playwright."
playwright install || error_exit "Failed to install Playwright browsers."


print_message "Change mode for run script"
chmod +x ./scripts/run_autoRSA.sh || error_exit "Cant change file mode"

print_message "Validating the installation..."
if [ -f ./autoRSA.py ]; then
    print_message "Installation complete. You can now use the auto-rsa tool."
else
    error_exit "Error: auto-rsa.py not found. Something went wrong during the setup."
fi