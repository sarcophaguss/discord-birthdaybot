import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import discord
from discord.ext import commands
from main import HelpCommand, MyBirthdayBot

class TestHelpCommand(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.help_command = HelpCommand()
        self.help_command.context = MagicMock()
        self.help_command.get_destination = MagicMock(return_value=AsyncMock())
        
    async def test_send_bot_help(self):
        # Mock cog and commands
        mock_cog = MagicMock()
        mock_cog.qualified_name = "BirthdayCog"
        mock_command = MagicMock()
        mock_command.name = "test"
        mock_command.help = "Test command"
        
        # Create mapping
        mapping = {mock_cog: [mock_command]}
        
        # Mock filter_commands
        self.help_command.filter_commands = AsyncMock(return_value=[mock_command])
        
        # Call the method
        await self.help_command.send_bot_help(mapping)
        
        # Verify channel.send was called with an embed
        channel = self.help_command.get_destination.return_value
        channel.send.assert_called_once()
        
        # Verify the embed contains our command
        call_args = channel.send.call_args
        embed = call_args[1]['embed']
        self.assertIn("Bot Commands", [field.name for field in embed.fields])
        self.assertIn("`!test`: Test command", embed.fields[0].value)

class TestMyBirthdayBot(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = MyBirthdayBot()
        
    @patch('discord.ext.commands.Bot.load_extension')
    async def test_setup_hook(self, mock_load_extension):
        # Test extension loading
        await self.bot.setup_hook()
        mock_load_extension.assert_called_once_with('cogs.birthday')
        
    async def test_on_ready(self):
        # Mock bot user
        self.bot.user = MagicMock()
        self.bot.user.name = "TestBot"
        self.bot.user.id = "123456789"
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            await self.bot.on_ready()
            
            # Verify prints
            mock_print.assert_any_call(f"Logged in as TestBot (ID: 123456789)")
            mock_print.assert_any_call("------")
            mock_print.assert_any_call("Bot is ready!")
            
    def tearDown(self):
        # Clean up
        self.bot.clear()

if __name__ == '__main__':
    unittest.main()