#!/bin/bash
# Setup script for Training Assistant

echo "🏋️ Setting up Training Assistant..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create data directories
echo "Creating data directories..."
mkdir -p data/sessions data/videos data/exports

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the app: streamlit run src/training_assistant/app.py"
echo ""
echo "🚀 Happy training!"