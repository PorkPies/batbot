import discord
from discord.ext import commands
import random
import os
import asyncio
import yaml
from datetime import datetime

def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

# Load configuration
config = load_config()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config['bot']['prefix'], intents=intents)

# Load resources from config
BATMAN_QUOTES = config['quotes']
SOUND_EFFECTS = config['sounds']
BATMAN_FACTS = config['facts']

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
@bot.command(name='batquote')
async def batman_quote(ctx):
    """Sends a random Batman quote"""
    quote = random.choice(BATMAN_QUOTES)
    await ctx.send(f"🦇 {quote}")

@bot.command(name='batsound')
async def play_sound(ctx, sound_name: str = None):
    """Plays a Batman-related sound effect"""
    if not sound_name:
        await ctx.send("Available sounds: " + ", ".join(SOUND_EFFECTS.keys()))
        return
        
    if sound_name not in SOUND_EFFECTS:
        await ctx.send("Sound not found! Use !batsound to see available sounds.")
        return
        
    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to use this command!")
        return

    try:
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(SOUND_EFFECTS[sound_name]))
        
        while voice_client.is_playing():
            await asyncio.sleep(1)
            
        await voice_client.disconnect()
    except Exception as e:
        print(f"Error playing sound: {e}")
        await ctx.send("There was an error playing the sound.")

@bot.command(name='batfact')
async def batman_fact(ctx):
    """Sends a random Batman fact"""
    await ctx.send(f"🦇 Did you know? {random.choice(BATMAN_FACTS)}")

@bot.command(name='bathelp')
async def help_command(ctx):
    """Shows all available commands"""
    commands_list = """
    🦇 **Batman Bot Commands** 🦇
    `!batquote` - Get a random Batman quote
    `!batsound [sound_name]` - Play a Batman sound effect
    `!batfact` - Learn a random Batman fact
    `!bathelp` - Show this help message
    """
    await ctx.send(commands_list)

if __name__ == "__main__":

    try:
        bot.run(config['bot']['token'])
    except Exception as e:
        print(f"Error starting bot: {e}")
        print("Please check if your token is correct in config.yaml")