import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

user_data = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

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
            await member.send("❌ Age must be a number. Try again:")
        
        # Store the data (here, just print it, replace with DB save)
        print({
            'user_id': member.id,
            'name': name.content,
            'branch': branch.content,
            'age': int(age.content)
        })

        await member.send("✅ Thanks! Your info has been recorded.")

    except Exception as e:
        print(f"Error with {member.name}: {e}")

bot.run("YOUR_BOT_TOKEN")
