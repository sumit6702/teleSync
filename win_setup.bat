@echo off

REM Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

# Create env file
echo "BOT_TOKEN=YOUR_BOT_TOKEN" > .env
echo "CHAT_ID=YOUR_CHAT_ID" >> .env

echo Setup complete!
