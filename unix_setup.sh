#!/bin/bash

# Check if Python and pip is installed
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install Python3."
    exit 1
fi

if ! command -v pip3 &>/dev/null; then
    echo "pip3 is not installed. Please install pip3."
    exit 1
fi

# Detect the shell
if [[ $SHELL_TYPE == "fish" ]]; then
    . venv/bin/activate.fish
else
    source venv/bin/activate
fi

# Check if virtual environment directory exists
if [ ! -d "venv" ]; then
    # Create and activate virtual environment
    python -m venv venv || {
        echo "Failed to create virtual environment"
        exit 1
    }

    if [[ $SHELL_TYPE == "fish" ]]; then
        source venv/bin/activate.fish
    else
        source venv/bin/activate
    fi
else
    echo "Virtual environment already exists, skipping creation."
fi

# Install dependencies
./venv/bin/pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    # Create .env file
    cat >.env <<EOF
BOT_TOKEN=YOUR_BOT_TOKEN
CHAT_ID=YOUR_CHAT_ID
EOF
else
    echo ".env file already exists, skipping creation."
fi

echo "Setup complete! Virtual environment activated for $SHELL_TYPE."
