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
PATHS = config['paths']

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
@bot.command(name='batquote')
async def batman_quote(ctx):
    """Sends a random Batman quote"""
    quote = random.choice(BATMAN_QUOTES)
    await ctx.send(f"🦇 {quote}")


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


FFMPEG_PATH = 'C:\\ProgramData\\chocolatey\\bin\\ffmpeg.exe'

@bot.command(name='batsound')
async def play_sound(ctx, sound_name: str = None):
    """Plays a Batman-related sound effect"""

    #TODO add random config

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
        
        sound_path = os.path.abspath(PATHS['main_path'] + SOUND_EFFECTS[sound_name])
        print(f"Attempting to play: {sound_path}")
        
        # Verify file exists
        if not os.path.exists(sound_path):
            await ctx.send(f"Error: Sound file not found at {sound_path}")
            return
            
        
        if os.path.exists(sound_path):
            voice_client.play(discord.FFmpegPCMAudio(
                executable=FFMPEG_PATH,
                source=sound_path
            ))
            await ctx.send(f"Playing sound: {sound_name}")
            
            # Wait for audio to finish
            while voice_client.is_playing():
                await asyncio.sleep(1)
            
                
        else:
            await ctx.send("Error converting sound file")
            
        await voice_client.disconnect()
        
    except Exception as e:
        print(f"Error playing sound: {e}")
        await ctx.send(f"Error playing sound: {str(e)}")
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()

# Debug command to check sound files
@bot.command(name='checksounds')
async def check_sounds(ctx):
    """Check if sound files exist and are readable"""
    results = []
    for name, path in SOUND_EFFECTS.items():
        abs_path = os.path.abspath(path)
        exists = os.path.exists(abs_path)
        results.append(f"{name}: {'✅' if exists else '❌'} ({abs_path})")
    
    await ctx.send("Sound File Status:\n" + "\n".join(results))

if __name__ == "__main__":

    try:
        bot.run(config['bot']['token'])
    except Exception as e:
        print(f"Error starting bot: {e}")
        print("Please check if your token is correct in config.yaml")