# Telegram Auto-Forwarding Bot

This project implements a Telegram bot using Telethon and FastAPI that automatically forwards messages from specified
source channels to a target channel.

## Repository Structure

The repository is structured as follows:

```
.
└── app
    ├── __init__.py
    ├── api
    │   ├── __init__.py
    │   ├── health_check.py
    │   └── telegram.py
    ├── main.py
    ├── settings.py
    └── telegram
        ├── __init__.py
        ├── client.py
        └── instance.py
```

### Key Files:

- `app/main.py`: The entry point of the FastAPI application.
- `app/api/telegram.py`: Handles message forwarding logic.
- `app/api/health_check.py`: Implements health check endpoint.
- `app/telegram/client.py`: Contains the Telethon client implementation.
- `app/telegram/instance.py`: Manages Telegram client instance.
- `app/settings.py`: Stores configuration settings for the application.

## Usage Instructions

### Installation

1. Ensure you have Python 3.11 or later installed.
2. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```
3. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```
4. Install the required dependencies using uv:
   ```
   uv pip install -r requirements.txt
   ```

### Configuration

1. Create a `.env` file in the root directory with the following variables:
   ```
   # Telegram API credentials
   TELEGRAM__API_ID=your_api_id
   TELEGRAM__API_HASH=your_api_hash
   
   # Channel configuration
   TELEGRAM__CHANNELS=channel1_id,channel2_id,channel3_id  # Source channels to monitor
   TELEGRAM__TARGET_CHANNEL_ID=target_channel_id  # Channel where messages will be forwarded
   ```

2. To obtain your API credentials:
    - Go to https://my.telegram.org/auth
    - Log in with your phone number
    - Go to 'API development tools'
    - Create a new application to get your API_ID and API_HASH

### Running the Application

To start the FastAPI server:

```
uv run fastapi dev app/main.py
```

The server will start, and you can access the API documentation at `http://localhost:8000/docs`.

### How It Works

1. The bot monitors the specified source channels (TELEGRAM__CHANNELS)
2. When a new message is posted in any of the source channels, the bot automatically forwards it to the target channel (
   TELEGRAM__TARGET_CHANNEL_ID)
3. The FastAPI application provides an interface to monitor the bot's status and operations

```
[Source Channels] -> [Telethon Client] -> [Target Channel]
```

### API Endpoints

- `livez`/`redyz`: Health check endpoint to verify the service is running
- `telegram/channels`: Channels CRUD

## Deployment

For deployment, consider using a production-grade ASGI server like Gunicorn with Uvicorn workers:

```
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Ensure to set up proper SSL/TLS for secure communication when deploying to production.

## Important Notes

- Make sure your Telegram account has the necessary permissions to access the source channels and post in the target
  channel
- Be mindful of Telegram's rate limits when configuring multiple source channels
- Keep your API credentials secure and never commit them to version control