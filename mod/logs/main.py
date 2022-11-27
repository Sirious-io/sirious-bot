import discord

# Local file imports
from config import config

channelID = config["channels"]["mod_log"]
deleted_messages = []


async def deleted_message(client, author, moderator, channel, message):
    global deleted_messages
    if not message.id in deleted_messages:  
        deleted_messages.append(message.id)
        embed = discord.Embed(title="Message deleted", description="> **Author:** " + author.mention + "\n\n> **Moderator:** " + moderator + "\n\n> **Channel:** <#" + str(channel.id) + ">\n\n> **Content:** " + message.content + "\n\n> **ID:** ``" + str(message.id) + "``", color=0xed5555)
        embed.set_thumbnail(url=author.avatar_url)
        await client.get_channel(channelID).send(embed=embed)

async def edited_message(client, before, after):
    embed = discord.Embed(title="Message edited", description="> **Author:** " + before.author.mention + "\n\n> **Channel:** <#" + str(before.channel.id) + "> \n\n> **Before:** " + before.content + "\n\n> **After:** " + after.content + "\n\n> **ID:** ``" + str(before.id) + "``", color=0xebdb34)
    embed.set_thumbnail(url=before.author.avatar_url)
    await client.get_channel(channelID).send(embed=embed)

async def nickname(client, before, after):
    embed = discord.Embed(title="Nickname change", description="> **Member:** " + before.mention + "\n\n> **Before:** " + str(before.nick) + "\n\n> **After:** " + str(after.nick), color=0x14656b)
    embed.set_thumbnail(url=before.avatar_url)
    await client.get_channel(channelID).send(embed=embed)