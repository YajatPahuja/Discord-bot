import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_member_join(member):
    try:
        await member.send("👋 Welcome, Traveler. You're about to embark on a cosmic journey through time and space. Answer each question correctly to continue your mission.\nType your answers to proceed through each level. Let’s begin!")

        def check(m):
            return m.author == member and isinstance(m.channel, discord.DMChannel)

        await member.send("The Anomaly\n"
                          "You wake up in a cold pod, suspended in an endless void. Earth is a whisper in your memory, shattered by time. A voice, distorted by static, says: ‘You’ve been asleep for 72 years. The collapse of humanity... it was inevitable. Or was it?’\n\n"
                          "Which galaxy did humanity originate from before the void took them?")
        while True:
            msg = await bot.wait_for('message', check=check, timeout=90)
            if msg.content.lower() == "milky way":
                break
            await member.send("That's not right. Try again!")

        await member.send("Ghost in the Dust\n"
                          "A voice echoes, 'Stay, don’t go.' Books fall, but they are unreadable. A storm rages, not outside — but in time. Past memories shift, rearranged in patterns of light and shadow.\n\n"
                          "Who first broke the lunar silence?")
        while True:
            msg = await bot.wait_for('message', check=check, timeout=90)
            if msg.content.lower() == "neil armstrong":
                break
            await member.send("That's not quite right. Try again!")

        await member.send("Time Dilation\n"
                          "You orbit near a rogue planet, where time fractures like glass. 1 hour on the planet equals 7 years on the ship. You venture down. They stay behind. When you return, they are dust, but their memories linger in the ship’s walls.\n\n"
                          "Who first launched into the cosmic abyss, sending humanity’s call into the unknown?")
        while True:
            msg = await bot.wait_for('message', check=check, timeout=90)
            if msg.content.lower() == "voyager 1" or msg.content == "1977":
                break
            await member.send("That's not quite right. Try again!")

        
        await member.send("The Loop\n"
                          "*The AI glitches and whispers your daughter's name. But you know — you are her. Or were you always? The universe folds inward, pulling you through an event horizon into the heart of darkness.*\n\n"
                          "Saturn’s moons are the gateway, but how many shadows orbit the giant ring?")
        while True:
            msg = await bot.wait_for('message', check=check, timeout=90)
            if msg.content == "83":
                break
            await member.send("That’s not quite right. Try again!")

    
        await member.send("The Tesseract\n"
                          "You float in the kaleidoscope of 5D space, touching past, present, and future in a single breath. You stretch your hand into the past, sending this message back to yourself — the one who will embark on this journey again.\n\n"
                          "You’ve crossed the paradox. Time, space, and identity are your canvas. The question is: Will you ever wake up from this dream?")
        await member.send("Congratulations, Traveler! You've completed the cosmic quest and unlocked the paradox. Welcome to the community!")

    except Exception as e:
        print(f"Error with {member.name}: {e}")
        try:
            await member.send("Something went wrong or timed out. Please contact an admin to try again.")
        except:
            pass

bot.run(TOKEN)
