import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import csv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Path to CSV file
CSV_FILE = 'user_data.csv'

# Ensure the CSV file exists with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['user_id', 'name', 'branch', 'age'])

# Bot setup with necessary intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Needed for bot.wait_for to read DM content
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to save user data to CSV
def save_user_data(user_id, name, branch, age):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, name, branch, age])

# Bot event: on_ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Bot event: on_member_join
@bot.event
async def on_member_join(member):
    try:
        await member.send("👋 Welcome! Let's get to know you.")

        def check(m):
            return m.author == member and isinstance(m.channel, discord.DMChannel)

        await member.send("What's your **name**?")
        name = await bot.wait_for('message', check=check, timeout=60)

        await member.send("What's your **branch**?")
        branch = await bot.wait_for('message', check=check, timeout=60)

        await member.send("What's your **age**? (Enter a number)")
        while True:
            age = await bot.wait_for('message', check=check, timeout=60)
            if age.content.isdigit():
                break
            await member.send("Age must be a number. Try again:")

        save_user_data(member.id, name.content, branch.content, int(age.content))
        await member.send("Thanks! Your info has been recorded.")

    except Exception as e:
        print(f"Error with {member.name}: {e}")
        try:
            await member.send("Something went wrong while recording your info.")
        except:
            pass

# Run the bot
bot.run(TOKEN)
