import discord
from discord.ext import commands
import requests
import re

client = commands.Bot(command_prefix = '/')

client.botmode = 'off'
ocrkey = '' # API key for https://ocr.space/ocrapi

@client.event
async def on_ready():
    print('Bot online')

@client.command()
async def emails(ctx, url):
    content = requests.get(url).text
    lst = re.findall('[\w\.-]+@[\w\.-]+', content)
    for a in range(0, len(lst)):
        await ctx.send(str(lst[a]))

@client.command()
async def ocr(ctx, msg):
    if msg == 'on':
        client.botmode = 'on'
        await ctx.send("OCR Bot Activated")
    elif msg == 'off':
        client.botmode = 'off'
        await ctx.send("OCR Bot Deactivated")

@client.event
async def on_message(msg):
    if client.botmode == 'on':
        try:
            chan = msg.channel
            imgurl = str(msg.attachments)[str(msg.attachments).find("url='")+5:-3]
            resp = requests.get('https://api.ocr.space/parse/imageurl?apikey='+ocrkey+'&url='+imgurl).json()
            await chan.send(bytes(resp['ParsedResults'][0]['ParsedText'], "utf-8").decode("unicode_escape"))
        except Exception:
            pass
    await client.process_commands(msg)

client.run('') # Discord bot API key
