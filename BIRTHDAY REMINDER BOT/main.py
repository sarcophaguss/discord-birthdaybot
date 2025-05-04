import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load discord token from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Check if the token is loaded correctly
if not DISCORD_TOKEN:
    print("Error: DISCORD_TOKEN not found in .env file.")
    exit(1)

# Set up the bot with intents
intents = discord.Intents.default()
intents.message_content = True # Required for reading message content for prefix commands
intents.members = True # Required to get member details by ID

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Birthday Bot Help",
            description="List of available commands:",
            color=discord.Color.blue()
        )
        
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = []
            
            for cmd in filtered:
                signature = f"`!{cmd.name}`: {cmd.help}" if cmd.help else f"`!{cmd.name}`"
                command_signatures.append(signature)
            
            if command_signatures:
                name = getattr(cog, "qualified_name", "No Category")
                
                if name == "BirthdayCog":
                    name = "Bot Commands"
                    
                embed.add_field(
                    name=name,
                    value="\n".join(command_signatures),
                    inline=False
                )
        
        channel = self.get_destination()
        await channel.send(embed=embed)

# Defining the main bot class
class MyBirthdayBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents, help_command=None)
        print("initializing bot...")
    
    # Defining setup_hook method to load extensions
    async def setup_hook(self):
        print("Running setup_hook...")
        initial_extensions = ['cogs.birthday']
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                print(f"Loaded extension {extension}")
            except Exception as e:
                print(f"Failed to load extension {extension}: {e}")
        print("Setup_hook complete.")
    
    # Defining on_ready event to indicate the bot is ready
    async def on_ready(self):
        print(f"Logged in as {self.user.name} (ID: {self.user.id})")
        print("------")
        print("Bot is ready!")
        
if __name__ == "__main__":
    bot = MyBirthdayBot()
    bot.help_command = HelpCommand()
    bot.run(DISCORD_TOKEN)