import discord
from discord.ext import commands, tasks
import datetime
import os
import json
from datetime import time
from zoneinfo import ZoneInfo

BIRTHDAY_FILE = "birthdays.json"
REMINDER_CHANNEL_ID = 1363491652064247850 # Discord channel ID
TARGET_TIMEZONE = ZoneInfo("Europe/Vilnius")
CHECK_TIME = time(hour=12, minute=00, second=0, tzinfo=TARGET_TIMEZONE)

def handle_command_errors(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            ctx = args[1]  # args[0] is self, args[1] is ctx
            await ctx.reply("Invalid date format. Please use MM-DD.")
        except Exception as e:
            ctx = args[1]
            await ctx.reply(f"An error occurred: {e}")
    return wrapper

class BirthdayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthdays = self.load_birthdays()
        self.daily_birthday_check.start()
        print("BirthdayCog initialized.")
        
    def load_birthdays(self):
        if os.path.exists(BIRTHDAY_FILE):
            try:
                with open(BIRTHDAY_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Error loading birthdays from JSON file. Starting with an empty list.")
                return {}
            except Exception as e:
                print(f"Unexpected error loading birthdays: {e}")
                return {}
        else:
            return {}
    
    def save_birthdays(self):
        try:
            with open(BIRTHDAY_FILE, "w") as f:
                json.dump(self.birthdays, f, indent=4)
        except Exception as e:
            print(f"Error saving birthdays to JSON file: {e}")
    
    @commands.command(name="add", help="Adds your birthday in the format MM-DD | Ex: !add 04-20")
    @handle_command_errors
    async def add_birthday(self, ctx, birthday_str):
        datetime.datetime.strptime(birthday_str, "%m-%d")
        user_id = str(ctx.author.id)
        
        self.birthdays[user_id] = {
            'birthday': birthday_str,
            'username': str(ctx.author),
        }
        
        self.save_birthdays()
        await ctx.reply(f"Birthday {birthday_str} added for {ctx.author.mention}.")

    @commands.command(name="remove", help="Removes your birthday")
    @handle_command_errors
    async def remove_birthday(self, ctx):
        user_id = str(ctx.author.id)
        if user_id in self.birthdays:
            del self.birthdays[user_id]
            self.save_birthdays()
            await ctx.reply(f"Birthday removed for {ctx.author.mention}.")
        else:
            await ctx.reply("You don't have a birthday set.")

    @commands.command(name="list", help="Lists all birthdays")
    @handle_command_errors
    async def list_birthdays(self, ctx):
        if not self.birthdays:
            await ctx.reply("No birthdays have been saved yet.")
            return
        
        embed = discord.Embed(
            title="🎂 Birthday List",
            description="Here are all the saved birthdays:",
            color=discord.Color.blue()
        )
        
        for user_id, user_data in self.birthdays.items():
            embed.add_field(
                name=user_data['username'],
                value=f"Birthday: {user_data['birthday']}",
                inline=False
            )
        
        await ctx.reply(embed=embed)
        
    @tasks.loop(time=CHECK_TIME)
    async def daily_birthday_check(self):
        now = datetime.datetime.now(tz=TARGET_TIMEZONE)
        today = now.strftime("%m-%d")
        channel = self.bot.get_channel(REMINDER_CHANNEL_ID)
        
        if channel is None:
            print(f"Error: Could not find channel with ID {REMINDER_CHANNEL_ID}.")
            return
        
        birthdays_found = False
        
        for user_id, user_data in self.birthdays.items():
            birthday = user_data['birthday']
            username = user_data['username']
            
            if birthday == today:
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    await channel.send(f"Happy Birthday {username} ({user.mention})! 🎉🎂🥳")
                    birthdays_found = True
                except discord.NotFound:
                    print(f"User with ID {user_id} not found (account may be deleted).")
                except Exception as e:
                    print(f"Error fetching user {user_id}: {e}")
                    
        if not birthdays_found:
            print(f"No birthdays found for today ({today}).")
                
    @daily_birthday_check.before_loop
    async def before_daily_birthday_check(self):
        await self.bot.wait_until_ready()
        print("Daily birthday check is ready to start.")
            

async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))
    print("BirthdayCog loaded successfully.")