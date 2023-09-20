#!/bin/bash

VENV_NAME=.venv
PYTHON=python3
echo "[setup][+] Initializing Python virtual environment..."
# Commands to run after creating the virtual environment
COMMANDS=(
    "$PYTHON -m venv $VENV_NAME" # Create the python venv
    "source $VENV_NAME/bin/activate"  # Activate the virtual environment
    "mkdir ./media" # Make the media folder to store streamable media
    "touch .env" # Create .env file
    "echo \"OWNCAST_STREAMKEY=''\" > .env" # Populate .env with variable
    "pip install -r requirements.txt"  # Install python project dependencies
)

# Execute the commands
for cmd in "${COMMANDS[@]}"; do
    echo "[setup][*] Running: $cmd"
    eval "$cmd"
    if [ $? -ne 0 ]; then
        echo "[setup][!] Error: Command failed: $cmd"
        exit 1
    fi
done

echo "[setup][+] Setup completed successfully."
