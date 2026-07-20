@echo off
REM Crypto Analysis API - Setup Script for Windows

echo 🚀 Setting up Crypto Analysis API...

REM Check if .env file exists
if not exist .env (
    echo 📋 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please update .env with your configuration
)

REM Create virtual environment
echo 🐍 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Initialize database
echo 🗄️  Initializing database...
python scripts/init_top_10_cryptos.py

echo ✅ Setup completed!
echo.
echo 📝 Next steps:
echo 1. Update your .env file with API keys
echo 2. Run: python main.py
echo 3. Visit: http://localhost:8000/docs
echo.
echo 🐳 Or use Docker:
echo 1. docker-compose up
echo 2. Visit: http://localhost:8000/docs

pause