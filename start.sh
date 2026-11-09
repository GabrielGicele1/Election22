
#!/bin/bash

# Stop if a command fails
set -e

# Move to the project directory
cd "$(dirname "$0")"


echo "  BLOCKCHAIN VOTING SYSTEM"


# Check if Ganache is running
if ! curl -fsS http://127.0.0.1:8545 \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}' \
    > /dev/null; then
    echo "ERROR: Ganache is not running."
    echo "Start Ganache before running this script."
    exit 1
fi

echo "Ganache connection successful!"
echo "Starting Python application..."

# Run the Python application
./.venv/Scripts/python.exe python/app.py
