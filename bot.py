import discord, firebase_admin
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import ContextMenuType
from discord_slash.context import MenuContext
from termcolor import colored
from firebase_admin import credentials, firestore

# File imports, do not touch
import config
import levelsys.main as levelsys
import bankman.main as bank
import fun.main as fun
import mod.main as mod
import mod.logs.main as mod_logs
from exchange.exchange import LinkWallet, LinkedWalletsCheck

prefix = config.config["prefix"]
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# TODO: add above, bellow shit


@client.event
async def on_ready():
    print(colored('Logged in as {0.user}'.format(client), "green"))
    test.start()


# | Random utils
def permission_check(command, user):
    if not config.config["roles"][config.config["permissions"][command]] in [y.id for y in user.roles]:
        output = False, "You must have the <@&" + str(config.config["roles"][config.config["permissions"][command]]) + "> role to execute this command!"
        return output
    
    return True, ""


# | Moderation (Context menu)

@slash.context_menu(target=ContextMenuType.MESSAGE, name="Delete message")
async def delete(ctx: MenuContext):
    perm = permission_check("delete_messages", ctx.author)

    if perm[0]:
        await mod.delete_message_contextMenu(client, ctx)
    else:
        await ctx.reply(perm[1], hidden=True)


# | Moderation (Slash commands)

@slash.subcommand(base="moderation", name="warn", description="Warn a member ⚠")
async def warn(ctx: SlashContext, member: discord.Member, reason: str):
    perm = permission_check("warn_members", ctx.author)

    if perm[0]:
        await mod.warn_member(client, db, ctx, ctx.author, member, reason)
    else:
        await ctx.reply(perm[1], hidden=True)


@slash.subcommand(base="moderation", name="mute", description="Mute a member 🔇")
async def mute_member(ctx: SlashContext, member: discord.Member, reason: str):
    perm = permission_check("mute_members", ctx.author)

    if perm[0]:
        await mod.mute_member(client, db, ctx, ctx.author, member, reason)
    else:
        await ctx.reply(perm[1], hidden=True)

@slash.subcommand(base="moderation", name="ban", description="Ban a member 🔨")
async def mute_member(ctx: SlashContext, member: discord.Member, reason: str):
    perm = permission_check("ban_members", ctx.author)

    if perm[0]:
        await mod.ban_member(client, db, ctx, ctx.author, member, reason)
    else:
        await ctx.reply(perm[1], hidden=True)

@slash.subcommand(base="moderation", name="kick", description="Kick a member 👢")
async def mute_member(ctx: SlashContext, member: discord.Member, reason: str):
    perm = permission_check("ban_members", ctx.author)

    if perm[0]:
        await mod.kick_member(client, db, ctx, ctx.author, member, reason)
    else:
        await ctx.reply(perm[1], hidden=True)



@slash.subcommand(base="moderation", name="background_check", description="Views a members background 🤨")
async def view_warns(ctx: SlashContext, member: discord.Member):
    perm = permission_check("view_background", ctx.author)

    if perm[0]:
        await mod.view_background(client, db, ctx, member)
    else:
        await ctx.reply(perm[1], hidden=True)


@slash.subcommand(base="moderation", name="lock_channel", description="Lock a channel 🔒")
async def view_warns(ctx: SlashContext, reason: str, channel: discord.channel = None):
    perm = permission_check("view_background", ctx.author)

    if perm[0]:
        if not channel: channel = ctx.channel
        await mod.lock_channel(client, ctx, db, reason)
    else:
        await ctx.reply(perm[1], hidden=True)

@slash.subcommand(base="moderation", name="slowmode_channel", description="Edit slowmode for channel 🐌")
async def view_warns(ctx: SlashContext, reason: str, channel: discord.channel = None, delay: int = 10):
    perm = permission_check("view_background", ctx.author)

    if perm[0]:
        if not channel: channel = ctx.channel
        await mod.lock_channel(client, ctx, db, reason)
    else:
        await ctx.reply(perm[1], hidden=True)

# @slash.subcommand(base="moderation", name="purge", description="Purge messages ❌")

# | Moderation (Logging)

@client.event
async def on_message_delete(ctx):
    await mod_logs.deleted_message(client, ctx.author, "*Self ^*", ctx.channel, ctx)

@client.event
async def on_message_edit(before, after):
    await mod_logs.edited_message(client, before, after)

@client.event
async def on_member_update(before, after):
    if before.nick != after.nick:
        await mod_logs.nickname(client, before, after)

# @slash.slash()
# async def echo(ctx, text:str):
#     await ctx.reply(text.replace(r"\n", "\n"))

# @slash.slash()
# async def mute(ctx: SlashContext, member:discord.Member):
#     MuteRole = "Muted"
#     if not discord.utils.get(ctx.guild.roles, name=MuteRole):
#         await ctx.guild.create_role(name=MuteRole, permissions=discord.Permissions(send_messages=False, read_messages=True), colour=discord.Colour(0x808080))

#     if discord.utils.get(member.roles, name=MuteRole):
#         await ctx.send("User: " + member.display_name + " is already muted")
#     else:
#         await member.add_roles(discord.utils.get(ctx.guild.roles, name=MuteRole))
#         await ctx.send("Muted: " + member.display_name)

# @slash.slash()
# async def unmute(ctx, member:discord.Member):
#     MuteRole = "Muted"
#     if not discord.utils.get(ctx.guild.roles, name=MuteRole):
#         await ctx.guild.create_role(name=MuteRole, permissions=discord.Permissions(send_messages=False, read_messages=True), colour=discord.Colour(0x808080))

#     if discord.utils.get(member.roles, name=MuteRole):
#         await member.remove_roles(discord.utils.get(ctx.guild.roles, name=MuteRole))
#         await ctx.send("Unmuted: " + member.display_name)
#     else:
#         await ctx.send("User: " + member.display_name + " is not muted")


    

# | Leveling system
@client.event
async def on_member_join(member):
    await levelsys.memberJoin(member)

@client.event
async def on_message(message):
    if not message.content == "" and not message.channel.type == discord.ChannelType.private:
        await levelsys.onMessage(client, message)
    

@slash.subcommand(base="levels", name="rank", description="View someone's rank 🥇")
async def rank(ctx: SlashContext, member: discord.Member = None):
    if not member:
        member = ctx.author
    await levelsys.rank(ctx, member)

@slash.subcommand(base="levels", name="leaderboard", description="View most active members 📊")
async def leaderboard(ctx: SlashContext):
    await levelsys.leaderBoard(ctx, client)

# | Level sys mod

@client.command()
async def levelup(ctx):
    perm = permission_check("add_level", ctx.author)

    if perm[0]:
        await levelsys.addLevel(ctx)
    else:
        await ctx.reply(perm[1], hidden=True)


@client.command()
async def adxp(ctx, amount: int = 100):
    perm = permission_check("add_xp", ctx.author)

    if perm[0]:
        await levelsys.addExp(ctx, amount)
    else:
        await ctx.reply(perm[1], hidden=True)


# | Money

# @slash.subcommand(base="bank", name="balance", description="View someone's balance 👀")
# async def balance(ctx: SlashContext, member:discord.Member = None):
#     if member == None:
#         member = ctx.author
#     await bank.balance(ctx, member)

# @slash.subcommand(base="casino", name="gamble", description="Gamble your " + config.config["BotCoinName"] + " 🎲")
# async def gamble(ctx: SlashContext, amount: float):
#     perm = permission_check("gamble", ctx.author)

#     if perm[0]:
#         await fun.gamble(ctx, amount)
#     else:
#         await ctx.reply(perm[1], hidden=True)

# @slash.subcommand(base="link", name="wallet")
# async def link(ctx: SlashContext, wallet_address: str):
#     if ctx.channel.type == discord.ChannelType.private:
#         await LinkWallet(ctx, wallet_address)
#     else:
#         embed = discord.Embed(title="❌  Error  ❌")
#         embed.add_field(name="Please use this commands in DM's!", value="Moderators, dissable this command!")
#         await ctx.reply(embed=embed)

# @slash.slash()
# async def addBal(ctx, acc: str, amount: float):
#     await bank.addBal(ctx, acc, amount)

@tasks.loop(seconds=20)
async def test():
    await LinkedWalletsCheck(client)


client.run(config.config["DiscordToken"])