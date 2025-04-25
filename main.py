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
    print(f' Logged in as {bot.user}')

@bot.event
async def on_member_join(member):
    try:
        await member.send("👋 Welcome to the server! You're about to embark on a special quest: **The Digital Chronicles: Rise of ACM**.\nType your answers to proceed through each level. Let’s begin!")

        def check(m):
            return m.author == member and isinstance(m.channel, discord.DMChannel)

        # Level 1
        await member.send("📜 **Level 1: The Origin Spark**\n"
                          "*In**What is the name of this organization they formed?**")
        while True:
            msg = await bot.wait_for('message', check=check, timeout=90)
            if msg.content.lower() in ["acm", "association for computing machinery"]:
                break
            await member.send(" That's not quite right. Try again!")

        # Level 2
        await member.send("📜 **Level 2: The First Flame**\n"
                          "*The early ACM didn't hoard knowledge. They spread it.*\n"
                          " **What did ACM start publishing to spread computer science breakthroughs?**")
        while True:
            msg = await bot.wait_for('message', check=check, timeout=90)
            if msg.content.lower() in ["academic journals", "research papers", "publications"]:
                break
            await member.send("Not the answer we're looking for. Try again!")

        # Level 3
        await member.send("📜 **Level 3: The Vision Ahead**\n"
                          "*ACM grew globally, yet its mission stayed strong.*\n"
                          "**Which of these best represents one of ACM’s current goals?**\n"
                          "(Options: 'advance computing', 'promote education', 'publish research')")
        while True:
            msg = await bot.wait_for('message', check=check, timeout=90)
            if msg.content.lower() in ["advance computing", "promote education", "publish research"]:
                break
            await member.send("That's not quite a goal. Choose one from the options.")

        # Final Level
        await member.send("📜 **Final Level: The Torchbearer**\n"
                          "*As of today, ACM is led by a visionary guiding it through the digital age.*\n"
                          "**Who is the current president of ACM globally?**")
        while True:
            msg = await bot.wait_for('message', check=check, timeout=90)
            if msg.content.lower() == "yannis ioannidis":
                break
            await member.send("Incorrect. Try again! Hint: It starts with 'Y'.")

        await member.send("🎉 **Congratulations, Digital Explorer!** You've completed the ACM quest. Welcome to the community!")

    except Exception as e:
        print(f"Error with {member.name}: {e}")
        try:
            await member.send("Something went wrong or timed out. Please contact an admin to try again.")
        except:
            pass

bot.run(TOKEN)
