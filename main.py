import os
import asyncio
from dotenv import load_dotenv
from discord_bot.discordChannelFetcher import DiscordChannelFetcher

load_dotenv()

async def get_server_channels(discord_fetcher, server_id):
    """Get all channels in the server"""
    print("\nFetching server channels...")
    server_channels = await discord_fetcher.get_guild_channels(server_id)
    
    if server_channels:
        channel_id_array = [channel.id for channel in server_channels]
        print(f"Found {len(channel_id_array)} channels in the server.")
        return channel_id_array
    else:
        print("Could not retrieve channels. Check your SERVER_ID and bot permissions.")
        return []

async def get_channel_members(discord_fetcher, channel_id):
    """Get all members in a specific channel"""
    print(f"\nFetching members for channel {channel_id}...")
    channel_members = await discord_fetcher.get_channel_users(channel_id)
    
    if channel_members:
        print(f"Found {len(channel_members)} members in the channel.")
        return channel_members
    else:
        print("Could not retrieve channel members.")
        return []

async def get_user_messages(discord_fetcher, channel_id, member):
    """Get messages from a specific user in a channel"""
    print(f"\nFetching messages for user {member.name}...")
    user_messages = await discord_fetcher.get_messages_by_user(channel_id, member.id)
    
    if user_messages:
        print(f"Found {len(user_messages)} messages from {member.name}")
        return user_messages
    else:
        print(f"No messages found from {member.name}")
        return []

async def display_user_info(member):
    """Display user information"""
    print("\nUser Information:")
    print(f"Member ID: {member.id}")
    print(f"Member Name: {member.name}")
    if hasattr(member, 'global_name') and member.global_name:
        print(f"Global Name: {member.global_name}")
    print(f"Is Bot: {member.bot}")

async def display_messages(messages):
    """Display message information"""
    for message in messages:
        print("\nMessage Details:")
        print(f"Content: {message.content}")
        print(f"Sent at: {message.created_at}")
        if message.attachments:
            print(f"Attachments: {len(message.attachments)}")
        if message.embeds:
            print(f"Embeds: {len(message.embeds)}")

async def main():
    print("Starting bot...")
    
    # Load environment variables
    discord_bot_token = os.getenv("BOT_TOKEN")
    server_id = int(os.getenv("SERVER_ID"))
    client_id = os.getenv("CLIENT_ID")
    basic_channel_id = int(os.getenv("BASIC_CHANNEL_ID"))
    channel_one_id = int(os.getenv("CHANNEL_ONE_ID"))
    channel_two_id = int(os.getenv("CHANNEL_TWO_ID"))
    
    # Initialize bot
    discord_fetcher = DiscordChannelFetcher(bot_token=discord_bot_token)
    bot_task = asyncio.create_task(discord_fetcher.start_bot())
    
    try:
        # Wait for bot to connect
        await asyncio.sleep(5)
        
        # Step 1: Get server channels
        channel_id_array = await get_server_channels(discord_fetcher, server_id)
        
        # Step 2: Get channel members
        channel_members = await get_channel_members(discord_fetcher, basic_channel_id)
        
        # Step 3: Process each member
        for member in channel_members:
            # Display user information
            await display_user_info(member)
            
            # Get and display user messages
            user_messages = await get_user_messages(discord_fetcher, basic_channel_id, member)
            if user_messages:
                await display_messages(user_messages)
        
    finally:
        # Cleanup
        await discord_fetcher.close_bot()
        bot_task.cancel()
        print("\nBot shutdown complete.")

if __name__ == "__main__":
    asyncio.run(main())