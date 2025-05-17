import os
import asyncio
from dotenv import load_dotenv
from discord_bot.discordChannelFetcher import DiscordChannelFetcher

load_dotenv()

async def main():
    print("Starting bot...")
    
    discord_bot_token = os.getenv("BOT_TOKEN")
    server_id = int(os.getenv("SERVER_ID"))
    client_id = os.getenv("CLIENT_ID")
    basic_channel_id = int(os.getenv("BASIC_CHANNEL_ID"))
    channel_one_id = int(os.getenv("CHANNEL_ONE_ID"))
    channel_two_id = int(os.getenv("CHANNEL_TWO_ID"))
    
    discord_fetcher = DiscordChannelFetcher(bot_token=discord_bot_token)
    bot_task = asyncio.create_task(discord_fetcher.start_bot())
    
    try:
        # Wait for bot to connect
        await asyncio.sleep(5)
        
        server_channels = await discord_fetcher.get_guild_channels(server_id)

        channel_id_array = []
        if server_channels:
            channel_id_array = [channel.id for channel in server_channels]
            print(f"Found {len(channel_id_array)} channels in the server.")
        else:
            print("Could not retrieve channels. Check your SERVER_ID and bot permissions.")
        
        for channel_id in [basic_channel_id, channel_one_id, channel_two_id]:
            if channel_id in channel_id_array:
                print(f"Processing channel ID: {channel_id}")

                channel = await discord_fetcher.get_channel(channel_id)
                if channel:
                    print(f"Channel name: {channel.name}")
                
                messages = await discord_fetcher.get_channel_messages(channel_id, limit=10)
                if messages:
                    print(f"Retrieved {len(messages)} messages from {channel.name}")
                    quit()
        
    finally:
        await discord_fetcher.close_bot()
        bot_task.cancel()
        print("Bot shutdown complete.")

if __name__ == "__main__":
    asyncio.run(main())