#!/bin/bash

# Script to set up a shared virtual environment for the AI Agents workspace

set -e

echo "Setting up shared virtual environment for AI Agents workspace..."

# Create a shared virtual environment in the workspace root
VENV_DIR="/workspaces/mslearn-ai-agents/.venv"

# Remove existing virtual environment if it exists
if [ -d "$VENV_DIR" ]; then
    echo "Removing existing virtual environment..."
    rm -rf "$VENV_DIR"
fi

# Create virtual environment with system site packages
echo "Creating shared virtual environment..."
if python -m venv "$VENV_DIR" --system-site-packages; then
    echo "Virtual environment created successfully"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    echo "Upgrading pip..."
    python -m pip install --upgrade pip
    
    # Install common packages found in requirements.txt files
    echo "Installing common AI agent packages..."
    pip install python-dotenv azure-identity azure-ai-agents azure-ai-projects uvicorn
    
    # Install from any requirements.txt files found in lab directories
    echo "Installing packages from lab requirements files..."
    find /workspaces/mslearn-ai-agents/Labfiles -name "requirements.txt" -type f | while read -r req_file; do
        echo "Installing from: $req_file"
        pip install -r "$req_file" 2>/dev/null || {
            echo "Warning: Some packages from $req_file failed to install"
        }
    done
    
    # Deactivate virtual environment
    deactivate
    
    echo "✓ Shared virtual environment setup complete at $VENV_DIR"
else
    echo "Failed to create virtual environment with pip, trying without pip..."
    if python -m venv "$VENV_DIR" --without-pip --system-site-packages; then
        echo "✓ Virtual environment created without pip (system packages available)"
        echo "Note: System-wide packages will be used due to --system-site-packages flag"
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To activate the shared virtual environment, run:"
echo "  source /workspaces/ai-agents/.venv/bin/activate"
echo ""
echo "To deactivate the virtual environment, run:"
echo "  deactivate"
echo ""
echo "VS Code should automatically detect and use this virtual environment."
