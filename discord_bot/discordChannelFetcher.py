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
        self.token = bot_token
        self.bot = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())
        
        # Register event handlers
        @self.bot.event
        async def on_ready():
            print(f"Bot is ready. Logged in as {self.bot.user}")
    
    async def start_bot(self):
        """Start the bot and connect to Discord"""
        await self.bot.start(self.token)
    
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
        guild = self.bot.get_guild(guild_id)
        if not guild:
            try:
                guild = await self.bot.fetch_guild(guild_id)
            except discord.NotFound:
                return None
        
        return guild.channels
    
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