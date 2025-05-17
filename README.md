# Discord Channel Fetcher Bot

A powerful Discord bot built with Python that provides comprehensive channel management and message fetching capabilities. This bot allows you to interact with Discord channels, retrieve messages, and perform various operations on channel content.

## Features

- **Channel Management**
  - Fetch channel information
  - Get all channels in a guild/server
  - Retrieve channel messages with customizable limits
  - Access pinned messages

- **Message Operations**
  - Search messages by content
  - Filter messages by user
  - Find messages with attachments
  - Retrieve messages with embeds
  - Get specific messages by ID

- **Advanced Features**
  - Asynchronous operations for better performance
  - Customizable command prefix
  - Comprehensive error handling
  - Support for all Discord channel types

## Prerequisites

- Python 3.12 or higher
- Poetry for dependency management
- Discord Bot Token
- Discord Server ID
- Discord Client ID
- Channel IDs for the channels you want to interact with

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd discord-bot
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file in the root directory with the following variables:
```env
BOT_TOKEN=your_discord_bot_token
SERVER_ID=your_server_id
CLIENT_ID=your_client_id
BASIC_CHANNEL_ID=your_channel_id
CHANNEL_ONE_ID=your_channel_id
CHANNEL_TWO_ID=your_channel_id
```

## Usage

1. Start the bot:
```bash
poetry run python main.py
```

2. The bot will connect to Discord and start processing the specified channels.

## Dependencies

- discord.py (v2.3.2) - Discord API wrapper
- python-dotenv (v1.1.0) - Environment variable management
- requests (v2.32.3) - HTTP library
- asyncio (v3.4.3) - Asynchronous I/O support

## Project Structure

discord-bot/
├── discord_bot/
│ ├── init.py
│ └── discordChannelFetcher.py
├── tests/
├── main.py
├── pyproject.toml
├── poetry.lock
└── README.md


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Author

- husainalltheway <khalidhusain00112@gmail.com>