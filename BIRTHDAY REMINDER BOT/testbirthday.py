import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import discord
from discord.ext import commands
import json
import os
from cogs.birthday import BirthdayCog

class TestBirthdayCog(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = MagicMock(spec=commands.Bot)
        self.cog = BirthdayCog(self.bot)
        
    async def test_add_birthday(self):
        # Mock context
        ctx = MagicMock()
        ctx.author.id = "123456789"
        ctx.author.name = "TestUser"
        ctx.reply = AsyncMock()
        
        # Test adding valid birthday
        await self.cog.add_birthday(ctx, "04-20")
        
        self.assertIn("123456789", self.cog.birthdays)
        self.assertEqual(self.cog.birthdays["123456789"]["birthday"], "04-20")
        ctx.reply.assert_called_once()
        
    async def test_remove_birthday(self):
        # Setup test data
        self.cog.birthdays = {"123456789": {"birthday": "04-20", "username": "TestUser"}}
        
        # Mock context
        ctx = MagicMock()
        ctx.author.id = "123456789"
        ctx.reply = AsyncMock()
        
        # Test removing existing birthday
        await self.cog.remove_birthday(ctx)
        
        self.assertNotIn("123456789", self.cog.birthdays)
        ctx.reply.assert_called_once()
        
    async def test_list_birthdays(self):
        # Setup test data
        self.cog.birthdays = {
            "123456789": {"birthday": "04-20", "username": "TestUser1"},
            "987654321": {"birthday": "12-25", "username": "TestUser2"}
        }
        
        # Mock context
        ctx = MagicMock()
        ctx.reply = AsyncMock()
        
        # Test listing birthdays
        await self.cog.list_birthdays(ctx)
        
        ctx.reply.assert_called_once()
        
    async def test_daily_birthday_check(self):
        # Setup test data
        self.cog.birthdays = {
            "123456789": {"birthday": "04-20", "username": "TestUser"}
        }
        
        # Mock channel and user
        channel = MagicMock()
        channel.send = AsyncMock()
        self.bot.get_channel.return_value = channel
        
        test_user = MagicMock()
        self.bot.fetch_user = AsyncMock(return_value=test_user)
        
        # Test birthday check
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "04-20"
            await self.cog.daily_birthday_check()
            
            channel.send.assert_called_once()

    def tearDown(self):
        # Clean up any test files
        if os.path.exists("birthdays.json"):
            os.remove("birthdays.json")

if __name__ == '__main__':
    unittest.main()