Discord Birthday Bot: Project Report
1. Introduction
1.1. What is your application?
This report details the development of a custom Discord bot using Python and the py-cord library. The primary goal of this project was to create a functional bot that reminds server members about upcoming birthdays, while also demonstrating core Object-Oriented Programming (OOP) principles, a specific design pattern, and composition/aggregation. The bot allows users to add, remove, and list birthdays, and performs an automatic daily check to announce birthdays in a designated channel. The development process focused on creating a structured, maintainable, and extensible codebase.

1.2. How to run the program?
To run the Discord Birthday Bot, the following steps are required:
Prerequisites: Ensure Python (version 3.9 or newer recommended for zoneinfo) and pip are installed.
Clone/Download: Obtain the project files (main.py, cogs/birthday.py, etc.).
Virtual Environment (Recommended):
Navigate to the project directory in a terminal.
Create a virtual environment: python -m venv venv
Activate the environment:
Windows: .\venv\Scripts\activate
Install Dependencies: Install the required libraries using pip:
pip install -U py-cord python-dotenv tzdata
Discord Bot Setup:
Create a Discord Application and Bot via the Discord Developer Portal.
Obtain the bot's Token.
Enable the Server Members Intent and Message Content Intent in the bot's settings on the portal.
Invite the bot to your desired Discord server with the necessary permissions (Send Messages, Read Message History).
Configuration:
Create a .env file in the project's root directory.
Add the bot token to the .env file: DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
In cogs/birthday.py, update the REMINDER_CHANNEL_ID constant with the ID of the channel where birthday announcements should be sent.
Update the TARGET_TIMEZONE constant if a timezone other than "Europe/Vilnius" is desired for the daily check.
Run the Bot: Execute the main script from the terminal (with the virtual environment activated):
python main.py

The bot should connect to Discord and come online.

1.3. How to use the program?
Once the bot is running and added to a Discord server:
Adding a Birthday: Users can save their birthday using the command:
!add MM-DD (e.g., !add 05-04)
Removing a Birthday: Users can remove their saved birthday using:
!remove
Listing Birthdays: Users can see all saved birthdays using:
!list
Getting Help: Users can see the list of commands and their descriptions using:
!help
Automatic Reminders: The bot automatically checks for birthdays every day at the configured time (default: 12:00 PM Europe/Vilnius) and posts a celebratory message in the configured reminder channel if any birthdays match the current date.

2. Body / Analysis
This section analyzes and explains the program's implementation, detailing how it meets its objectives and functional requirements by applying OOP principles and design patterns.

2.1. Functional Requirements Implementation
The core functionalities of the bot are implemented as follows:
Adding/Removing/Listing Birthdays: These user interactions are handled by specific command methods (add_birthday, remove_birthday, list_birthdays) within the BirthdayCog. These methods process user input, interact with the data storage (self.birthdays dictionary and associated load/save methods), and provide feedback to the user via Discord replies.




Daily Birthday Check: This is implemented using a background task (daily_birthday_check) within the BirthdayCog, decorated with @tasks.loop. This task runs automatically at the scheduled time (CHECK_TIME), retrieves the current date, iterates through the stored birthdays, fetches user details, and sends announcement messages to the designated channel (REMINDER_CHANNEL_ID).

Help Command: A custom help command (CustomHelpCommand) provides users with a formatted list of available commands and their usage, improving user experience over the default help message.


2.2. Implementation Details: OOP Principles and Design
The structure and implementation rely heavily on OOP principles and a specific design pattern:

2.2.1. Inheritance
It allows a class to inherit properties/methods from a base class ("is-a" relationship).
Use in Code:
MyBirthdayBot(commands.Bot): Inherits core bot functionality.
BirthdayCog(commands.Cog): Inherits Cog structure for modularity.
CustomHelpCommand(commands.HelpCommand): Inherits help command structure to allow customization.


2.2.2. Encapsulation
What it is: Bundling data and methods operating on that data within a class, often hiding internal details.
Use in Code:
BirthdayCog encapsulates self.birthdays data and methods (load_birthdays, save_birthdays, commands) that manage it. Internal storage (JSON) is hidden.



2.2.3. Abstraction
What it is: Hiding complex implementation details, exposing only essential features.
Use in Code:
The py-cord library abstracts Discord API complexities.
load_birthdays() and save_birthdays() abstract file I/O details.
CustomHelpCommand abstracts embed formatting details.
(Insert code snippet/screenshot of save_birthdays method and a command calling 



2.2.4. Polymorphism
What it is: Allowing objects of different classes to respond to the same method call differently (e.g., method overriding).
Use in Code:
HelpCommand overrides send_bot_help from its parent class to provide a custom embed-based response instead of the default text response.


2.2.5. Design Pattern: Decorator
Pattern Chosen: Decorator
What it is: Adds behavior to objects dynamically without affecting others from the same class, often via wrappers.
Use in Code:
The @handle_command_errors decorator wraps command methods.
It intercepts potential errors (like ValueError, Exception) occurring within the command execution.
It provides centralized error handling and sends user-friendly error messages via ctx.reply(), keeping the command methods cleaner.


Why it was Suitable: Provided a clean way to add the cross-cutting concern of error handling to multiple commands without code duplication, enhancing maintainability.

2.2.6. Composition and Aggregation
What they are: Represent "has-a" relationships where objects are composed of, or use, other objects.
Use in Code:
Bot Composition/Aggregation: MyBirthdayBot has Cogs (BirthdayCog) and a CustomHelpCommand.

Cog Aggregation: BirthdayCog has a reference to the main bot instance (self.bot).

Cog Composition: BirthdayCog has a self.birthdays dictionary as part of its internal state.

3. Results and Summary
3.1. Results and Challenges
The primary result is a functional Discord bot capable of managing and announcing user birthdays as per the functional requirements.
A significant challenge during development involved resolving Python environment and dependency issues, specifically the ModuleNotFoundError: No module named 'audioop' error, which required careful troubleshooting of the Python installation, PATH variables, and virtual environment integrity.
Another challenge was correctly configuring the Windows PowerShell execution policy to allow the virtual environment activation script to run.
Ensuring correct timezone handling required installing the tzdata package and explicitly using zoneinfo for the scheduled task to guarantee accurate timing.
Initial implementation of the task loop starting within the Cog's __init__ led to an AttributeError, which was resolved by understanding the class initialization order and moving the task start logic appropriately (or fixing underlying indentation issues).

3.2. Conclusions
This project successfully achieved its goal of creating a Discord bot for birthday reminders.
The bot implements the core functionalities of adding, removing, listing, and automatically announcing birthdays.
The development process effectively demonstrated the application of key OOP principles (Inheritance, Encapsulation, Abstraction, Polymorphism), a specific design pattern (Decorator), and composition/aggregation, resulting in a structured and maintainable codebase.
The final result is a working Python application that interacts with the Discord API to provide a useful service to a server community.

3.3. Future Prospects
The current bot provides a solid foundation, and several potential extensions could enhance its functionality:
Upcoming Birthdays Command: Implement !upcoming [days] to show birthdays in the near future.
Database Storage: Migrate from JSON to SQLite for more robust data handling, especially if storing more information (like year or timezone).
Admin Commands: Add commands for administrators to manage birthdays for other users.
Slash Commands: Convert existing prefix commands to Discord's modern slash command interface.
User Timezones: Allow users to specify their timezone for more accurate, personalized reminder timing.
DM Reminders: Add an option for users to receive birthday notifications via direct message.
Age Calculation: Optionally store the birth year and display the user's age in announcements.