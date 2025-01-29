#!/bin/bash

# Detect the shell
if [[ $SHELL == *"fish" ]]; then
    SHELL_TYPE="fish"
elif [[ $SHELL == *"bash" ]]; then
    SHELL_TYPE="bash"
else
    echo "Unsupported shell: $SHELL"
    exit 1
fi

# Create and activate virtual environment
python -m venv venv

if [[ $SHELL_TYPE == "fish" ]]; then
    source venv/bin/activate.fish
else
    source venv/bin/activate
fi

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env <<EOF
BOT_TOKEN=YOUR_BOT_TOKEN
CHAT_ID=YOUR_CHAT_ID
EOF

echo "Setup complete! Virtual environment activated for $SHELL_TYPE."
