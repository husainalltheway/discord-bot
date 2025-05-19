import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

class DiscordChannelFetcher:
    def __init__(self, bot_token, command_prefix="!"):
        """
        Initialize the Discord Channel Fetcher with discord.py
        
        Args:
            bot_token (str): Your Discord bot token
            command_prefix (str): Command prefix for bot commands
        """
        if not bot_token:
            raise ValueError("Bot token cannot be empty")
            
        self.token = bot_token
        intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents)
        
        # Register event handlers
        @self.bot.event
        async def on_ready():
            print(f"Bot is ready. Logged in as {self.bot.user}")
            for guild in self.bot.guilds:
                print(f"- {guild.name} (ID: {guild.id})")
                
        @self.bot.event
        async def on_error(event, *args, **kwargs):
            print(f"Error in {event}:", args, kwargs)
    
    async def start_bot(self):
        """Start the bot and connect to Discord"""
        try:
            print("Attempting to start bot with token...")
            await self.bot.start(self.token)
        except discord.LoginFailure as e:
            print("Failed to login: Invalid token")
            raise
        except Exception as e:
            print(f"Error starting bot: {str(e)}")
            raise
    
    async def close_bot(self):
        """Close the bot connection"""
        await self.bot.close()
    
    async def get_channel(self, channel_id):
        """
        Get information about a specific channel
        
        Args:
            channel_id (int): ID of the channel
            
        Returns:
            discord.abc.GuildChannel: Channel object
        """
        channel = self.bot.get_channel(channel_id)
        if not channel:
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except discord.NotFound:
                return None
        return channel
    
    async def get_channel_messages(self, channel_id, limit=100):
        """
        Get messages from a channel
        
        Args:
            channel_id (int): ID of the channel
            limit (int): Maximum number of messages to retrieve
            
        Returns:
            list: List of message objects
        """
        channel = await self.get_channel(channel_id)
        if not channel:
            return None
        
        messages = []
        async for message in channel.history(limit=limit):
            messages.append(message)
        print("messages: ",messages)
        return messages
    
    async def get_channel_message(self, channel_id, message_id):
        """
        Get a specific message from a channel
        
        Args:
            channel_id (int): ID of the channel
            message_id (int): ID of the message
            
        Returns:
            discord.Message: Message object
        """
        channel = await self.get_channel(channel_id)
        if not channel:
            return None
        
        try:
            return await channel.fetch_message(message_id)
        except discord.NotFound:
            return None
    
    async def get_channel_users(self, channel_id):
        """
        Get all users in a channel
        """
        channel = await self.get_channel(channel_id)
        if not channel:
            return None
        
        return channel.members
    
    async def get_pinned_messages(self, channel_id):
        """
        Get all pinned messages in a channel
        
        Args:
            channel_id (int): ID of the channel
            
        Returns:
            list: List of pinned message objects
        """
        channel = await self.get_channel(channel_id)
        if not channel:
            return None
        
        return await channel.pins()
    
    async def search_messages(self, channel_id, query, limit=100, days=7):
        """
        Search for messages in a channel containing the query
        
        Args:
            channel_id (int): ID of the channel
            query (str): Search query (case-insensitive)
            limit (int): Maximum number of messages to check
            days (int): How many days back to search
            
        Returns:
            list: List of message objects matching the query
        """
        channel = await self.get_channel(channel_id)
        if not channel:
            return None
        
        matching_messages = []
        after_date = datetime.now() - timedelta(days=days)
        
        async for message in channel.history(limit=limit, after=after_date):
            if query.lower() in message.content.lower():
                matching_messages.append(message)
        
        return matching_messages
    
    async def get_guild_channels(self, guild_id):
        """
        Get all channels in a guild/server
        
        Args:
            guild_id (int): ID of the guild
            
        Returns:
            list: List of channel objects
        """
        try:
            print(f"Attempting to fetch guild with ID: {guild_id}")
            guild = self.bot.get_guild(guild_id)
            if not guild:
                print("Guild not found in cache, attempting to fetch...")
                try:
                    guild = await self.bot.fetch_guild(guild_id)
                except discord.NotFound:
                    print(f"Guild with ID {guild_id} not found")
                    return None
                except discord.Forbidden:
                    print(f"Bot doesn't have permission to access guild {guild_id}")
                    return None
                except Exception as e:
                    print(f"Error fetching guild: {str(e)}")
                    return None
            
            print(f"Successfully fetched guild: {guild.name}")
            return guild.channels
        except Exception as e:
            print(f"Unexpected error in get_guild_channels: {str(e)}")
            return None
    
    async def get_messages_by_user(self, channel_id, user_id, limit=100):
        """
        Get messages from a specific user in a channel
        
        Args:
            channel_id (int): ID of the channel
            user_id (int): ID of the user
            limit (int): Maximum number of messages to check
            
        Returns:
            list: List of message objects from the specified user
        """
        channel = await self.get_channel(channel_id)
        if not channel:
            return None
        
        user_messages = []
        async for message in channel.history(limit=limit):
            if message.author.id == user_id:
                user_messages.append(message)
        
        return user_messages
    
    async def get_messages_with_attachments(self, channel_id, limit=100):
        """
        Get messages with attachments from a channel
        
        Args:
            channel_id (int): ID of the channel
            limit (int): Maximum number of messages to check
            
        Returns:
            list: List of message objects with attachments
        """
        channel = await self.get_channel(channel_id)
        if not channel:
            return None
        
        messages_with_attachments = []
        async for message in channel.history(limit=limit):
            if message.attachments:
                messages_with_attachments.append(message)
        
        return messages_with_attachments
    
    async def get_messages_with_embeds(self, channel_id, limit=100):
        """
        Get messages with embeds from a channel
        
        Args:
            channel_id (int): ID of the channel
            limit (int): Maximum number of messages to check
            
        Returns:
            list: List of message objects with embeds
        """
        channel = await self.get_channel(channel_id)
        if not channel:
            return None
        
        messages_with_embeds = []
        async for message in channel.history(limit=limit):
            if message.embeds:
                messages_with_embeds.append(message)
        
        return messages_with_embeds