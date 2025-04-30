# cosmic_quest_bot.py
# DM-driven trivia bot that runs one session per user
# Final line is exactly: “the answer is tesseract”

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import webserver

# ── 1. TOKEN ──────────────────────────────────────────────────────────────
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is not set in environment variables")

# ── 2. INTENTS ────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True        # the only privileged intent we need

bot = commands.Bot(command_prefix="!", intents=intents)

# ── 3. SESSION STATE ──────────────────────────────────────────────────────
active_sessions: set[int] = set()     # users currently playing
finished_sessions: set[int] = set()   # users who already finished (optional)

# ── 4. QUEST LOGIC ────────────────────────────────────────────────────────
async def cosmic_quest(user: discord.User):
    try:
        await user.send(
            "👋 Welcome, Traveler. You’re about to embark on a cosmic journey through time and space..."
        )

        def check(m: discord.Message):
            return m.author == user and isinstance(m.channel, discord.DMChannel)

        questions = [
            ("…Which galaxy did humanity originate from before the void took them?", ["milky way"]),
            ("…Who first broke the lunar silence?", ["neil armstrong"]),
            ("…Who first launched into the cosmic abyss?", ["voyager 1"]),
            ("…Saturn’s moons are the gateway—how many shadows orbit the giant ring?", ["83"]),
        ]

        for prompt, answers in questions:
            await user.send(prompt)
            while True:
                try:
                    msg = await bot.wait_for("message", check=check, timeout=30)
                except asyncio.TimeoutError:
                    await user.send("⏰ Time’s up! DM me again to restart the quest.")
                    return
                if msg.content.lower().strip() in answers:
                    break
                await user.send("That’s not quite right. Try again!")

        # Final line (per your spec)
        await user.send("the answer is tesseract")
        finished_sessions.add(user.id)

    finally:
        active_sessions.discard(user.id)   # always unlock

# ── 5. EVENTS ─────────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id={bot.user.id})")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    # Run the quest only in DMs
    if isinstance(message.channel, discord.DMChannel):
        uid = message.author.id

        # Block re-runs for users who finished (remove this if you want replay)
        if uid in finished_sessions:
            return

        # Start a new session only if none is active
        if uid not in active_sessions:
            active_sessions.add(uid)
            await cosmic_quest(message.author)

    # Let command processors (if any) work
    await bot.process_commands(message)

# ── 6. START ──────────────────────────────────────────────────────────────
webserver.keep_alive()
bot.run(TOKEN)