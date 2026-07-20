#!/bin/bash

# Crypto Analysis API - Setup Script

echo "🚀 Setting up Crypto Analysis API..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
source venv/bin/activate 2>/dev/null || venv\Scripts\activate.bat

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "🗄️  Initializing database..."
python scripts/init_top_10_cryptos.py

echo "✅ Setup completed!"
echo ""
echo "📝 Next steps:"
echo "1. Update your .env file with API keys"
echo "2. Run: python main.py"
echo "3. Visit: http://localhost:8000/docs"
echo ""
echo "🐳 Or use Docker:"
echo "1. docker-compose up"
echo "2. Visit: http://localhost:8000/docs"
